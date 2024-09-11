#!/usr/bin/env python3

import argparse
import csv
import hashlib
import minorimpact
import minorimpact.config
import os
import os.path
import pickle
import pika
import re
import shutil
import subprocess
import sys
from threading import Thread, Event
import time

__version__ = "0.0.9"

def main():
    parser = argparse.ArgumentParser(description="Synkler")
    parser.add_argument('-c', '--config', help = "Read configuration options from CONFIG")
    parser.add_argument('-v', '--verbose', help = "extra loud output", action='store_true')
    parser.add_argument('-d', '--debug', help = "debugging output", action='store_true')
    #parser.add_argument('--id', nargs='?', help = "id of a specific synkler group", default='default')
    args = parser.parse_args()
    args.id = "default"
    if (args.debug): args.verbose = True

    config = minorimpact.config.getConfig(config = args.config)
    cleanup_script = config['default']['cleanup_script'] if ('cleanup_script' in config['default']) else None
    file_dir = config['default']['file_dir']
    keep_minutes = int(config['default']['keep_minutes']) if ('keep_minutes' in config['default']) else 30
    mode = config['default']['mode'] if ('mode' in config['default']) and config['default']['mode'] is not None else 'central'
    pidfile = config['default']['pidfile'] if ('pidfile' in config['default']) and config['default']['pidfile'] is not None else "/tmp/synkler.pid"
    rsync = config['default']['rsync'] if ('rsync' in config['default']) else None
    rsync_opts = config['default']['rsync_opts'] if ('rsync_opts' in config['default']) else ''
    rsync_opts = list(csv.reader([rsync_opts]))[0]
    if ('--checksum' not in rsync_opts): rsync_opts.append('--checksum')
    if ('--partial' not in rsync_opts): rsync_opts.append('--partial')
    if ('--delete-before' not in rsync_opts): rsync_opts.append('--delete-before')
    synkler_server = config['default']['synkler_server'] if ('synkler_server' in config['default']) else None

    if (file_dir is None):
        sys.exit("'file_dir' is not set")
    if (os.path.exists(file_dir) is False):
        sys.exit("'{}' does not exist.".format(file_dir))
    if (synkler_server is None):
        sys.exit("'synkler_server' is not set")
    if (rsync is None and mode != 'central'):
        sys.exit("'rsync' is not set")

    if (pidfile is not None and minorimpact.checkforduplicates(pidfile)):
        # TODO: if we run it from the command line, we want some indicator as to why it didn't run, but as a cron
        #   it fills up the log.  We really should use a logging module rather than STDOUT.
        if (args.verbose): sys.exit() #sys.exit('already running')
        else: sys.exit()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=synkler_server))
    channel = connection.channel()

    channel.exchange_declare(exchange='synkler', exchange_type='topic')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    if mode == 'central':
        channel.queue_bind(exchange='synkler', queue=queue_name, routing_key='done.' + args.id)
        channel.queue_bind(exchange='synkler', queue=queue_name, routing_key='new.' + args.id)
        file_dir = file_dir + '/' + args.id
        os.makedirs(file_dir, exist_ok=True)
    elif mode == 'download':
        channel.queue_bind(exchange='synkler', queue=queue_name, routing_key='download.' + args.id)
        channel.queue_bind(exchange='synkler', queue=queue_name, routing_key='new.' + args.id)
    elif mode == 'upload':
        channel.queue_bind(exchange='synkler', queue=queue_name, routing_key='done.' + args.id)
        channel.queue_bind(exchange='synkler', queue=queue_name, routing_key='upload.' + args.id)
    else:
        sys.exit("'mode' must be 'upload','central', or 'download'")

    files = {}
    kill = Event()
    scan_folder_thread = None
    try:
        scan_folder_thread = Thread(target=scan_folder, name='scan_folder', args=[file_dir, mode, files, keep_minutes, kill], kwargs={'verbose':args.verbose, 'debug':args.debug})
        scan_folder_thread.start()
    except:
        sys.exit("Error starting threads")

    transfer = None
    while (True):
        method, properties, body = channel.basic_get(queue = queue_name, auto_ack = True)
        while body != None:
            routing_key = method.routing_key
            file_data = pickle.loads(body)
            f = file_data['filename']
            md5 = file_data['md5']
            mtime = file_data['mtime']
            size = file_data['size']
            if (mode == 'central'):
                if (re.match('new', routing_key)):
                    if (f not in files):
                        # Figure out out if there's enough space left on '/' to take the file and still have the specified reserve.
                        # TODO: This doesn't take into account the size of any files currently being transfered.  "free" really needs to represent the amount of free
                        #   space + the total size of everything in where state == 'upload' -- not just the file we're evaluating.
                        free_percent = 5
                        if ( 'free_percent' in config['default']):
                            free_percent = int(config['default']['free_percent'])
                        # TODO: The disk we check needs to be based on 'file_dir', which is probably someplace other than '/'.
                        total, used, free = shutil.disk_usage('/')
                        target_free = total * (free_percent/100)
                        if ((free - size) > target_free):
                            if (args.verbose): minorimpact.fprint("{} ready for upload ({} remaining)".format(f, minorimpact.filesize(free - size)))
                            files[f] = {'filename':f, 'dir':file_dir, 'size':0, 'mtime':None, 'md5':None, 'state':'upload'}
                        else:
                            if (args.verbose): minorimpact.fprint("Not enough free space to receive {} ({} < {} remaining)".format(f, minorimpact.filesize(free - size), minorimpact.filesize(target_free)))
                    elif (files[f]['size'] == size and files[f]['mtime'] == mtime and files[f]['md5'] == md5):
                        if (files[f]['state'] == 'upload'):
                            if (args.verbose): minorimpact.fprint("{} ready for download".format(f))
                            files[f]['state'] = 'download'

                    if (f in files):
                        files[f]['mod_date'] = int(time.time())
                elif (re.match('done', routing_key)):
                    if (f in files):
                        if (files[f]['state'] != 'done'):
                            files[f]['state'] = 'done'
                            files[f]['mod_date'] = int(time.time())
                            if (args.verbose): minorimpact.fprint("{} done".format(f))
            elif (mode == 'upload' and f in files):
                if (re.match('upload', routing_key)):
                    if (args.debug): minorimpact.fprint("{} upload requested".format(f))
                    if (transfer is None):
                        if (files[f]['state'] == 'new' or (files[f]['state'] == 'uploaded' and int(time.time()) - files[f]['mod_date'] > 60)):
                            dest_dir = file_data['dir']
                            if (dest_dir is None):
                                minorimpact.fprintf("{f} upload failed:  destination directory is not set by central")
                            else:
                                # Start the transfer for new files, or files that we finished transferring more than a minute ago.
                                if (files[f]['state'] == 'uploaded'):
                                    # It looks like we can sometimes get a bogus md5 when the file is first read, so if we're
                                    #   re-uploading a file, let's confirm it.
                                    files[f]['md5'] = minorimpact.md5dir('{}/{}'.format(file_dir, f))
                                    files[f]['state'] = 'new'
                                    if (args.verbose): minorimpact.fprint("{} upload re-starting".format(f))
                                else:
                                    if (args.verbose): minorimpact.fprint("{} upload starting".format(f))
                                rsync_command = [rsync, '--archive', '--partial', *rsync_opts, '{}/{}'.format(file_dir, f), '{}:{}/'.format(synkler_server, dest_dir)]
                                if (args.debug): minorimpact.fprint(' '.join(rsync_command))
                                transfer = { 'file':f, 'command': rsync_command }
                                transfer['proc'] = subprocess.Popen(rsync_command)
                                files[f]['mod_date'] = int(time.time())
                        else:
                            if (args.debug): minorimpact.fprint("{} not ready to upload".format(f))
                    elif ('file' in transfer and transfer['file'] == f):
                        if (transfer['proc'].poll() is not None):
                            if (transfer['proc'].returncode != 0):
                                minorimpact.fprint("{} upload failed, return code: {}".format(f, transfer['proc'].returncode))
                                files[f]['state'] = 'churn'
                                files[f]['mod_date'] = int(time.time())
                            else:
                                files[f]['state'] = 'uploaded'
                                files[f]['mod_date'] = int(time.time())
                                if (args.verbose): minorimpact.fprint("{} upload completed".format(f))
                            transfer = None
                        elif (transfer['proc'].poll() is None):
                            if (args.debug): minorimpact.fprint("{} upload in progress".format(f))
                    else:
                        if (args.debug): minorimpact.fprint("waiting on another transfer: {}".format(transfer['file']))
                elif (re.match('done', routing_key)):
                    if (f in files):
                        files[f]['mod_date'] = int(time.time())
                        if (files[f]['state'] != 'done'):
                            if files[f]['md5'] == md5 and files[f]['size'] == size and files[f]["mtime"] == mtime:
                                files[f]['state'] = 'done'
                                if (args.verbose): minorimpact.fprint("{} done".format(f))
                            else:
                                if (args.verbose): minorimpact.fprint("ERROR: {} on final destination doesn't match, resetting state.".format(f))
                                files[f]['state'] = 'churn'
                    if (transfer is not None and 'file' in transfer and transfer['file'] == f):
                        transfer = None
            elif (mode == 'download'):
                 if (re.match('download', routing_key)):
                    file_data = pickle.loads(body)
                    f = file_data['filename']
                    dir = file_data['dir']
                    md5 = file_data['md5']
                    size = file_data['size']
                    mtime = file_data['mtime']

                    if (args.debug): minorimpact.fprint("{} download requested".format(f))
                    if (f not in files):
                        if (args.debug): minorimpact.fprint(file_data)
                        files[f]  = {'filename':f, 'size':0, 'md5':None, 'mtime':0, 'dir':file_dir, 'state':'download', 'mod_date':int(time.time()) }

                    if (files[f]['size'] != size or md5 != files[f]['md5'] or files[f]['mtime'] != mtime):
                        if (transfer is None):
                            rsync_command = [rsync, '--archive', '--partial', *rsync_opts, '{}:{}/{}'.format(synkler_server, dir, f), file_dir + '/']
                            if (args.verbose): minorimpact.fprint("{} download starting".format(f))
                            if (args.debug): minorimpact.fprint(' '.join(rsync_command))
                            transfer = { 'file': f, 'command': rsync_command }
                            transfer['proc'] = subprocess.Popen(rsync_command)
                            files[f]['mod_date'] = int(time.time())
                        elif ('file' in transfer and transfer['file'] == f):
                            if (transfer['proc'].poll() is not None):
                                return_code = transfer['proc'].returncode
                                if (return_code != 0):
                                    if (args.verbose): minorimpact.fprint("{} download failed, return code: {}".format(f, return_code))
                                    if (args.debug): minorimpact.fprint(transfer['proc'].args)
                                    files[f]['mod_date'] = int(time.time())
                                else:
                                    files[f]['size'] = minorimpact.dirsize(file_dir + '/' + f)
                                    files[f]['mtime'] = os.path.getmtime(file_dir + '/' + f)
                                    files[f]['md5'] = minorimpact.md5dir(file_dir + '/' + f)
                                    files[f]['mod_date'] = int(time.time())
                                    if (args.verbose): minorimpact.fprint("{} download complete".format(f))
                                transfer = None
                            elif (transfer['proc'].poll() is None):
                                if (args.debug): minorimpact.fprint("{} download in progress".format(f))
                        else:
                            if (args.debug): minorimpact.fprint("waiting on another transfer {}".format(transfer['file']))
                    else:
                        if (files[f]['state'] != 'done'):
                            if (args.verbose): minorimpact.fprint("{} done".format(f))
                            files[f]['state'] = 'done'
                            files[f]['mod_date'] = int(time.time())
                        if (transfer is not None and 'file' in transfer and transfer['file'] == f):
                            transfer = None
                 elif (re.match('new', routing_key)):
                    if (args.debug): minorimpact.fprint("{} available".format(f))
                    if (f in files):
                        files[f]['mod_date'] = int(time.time())
                        if (files[f]['state'] == 'done' and (files[f]['size'] != size or md5 != files[f]['md5'] or files[f]['mtime'] != mtime)):
                            del files[f]
                            os.remove(file_dir + '/' + f)

            # Get the next item from queue.
            method, properties, body = channel.basic_get(queue = queue_name, auto_ack = True)

        if (transfer is not None and 'file' in transfer and transfer['file'] not in files):
            transfer = None

        # Go through all the items in our internal status array and do what needs doing.
        filenames = [key for key in files]
        for f in filenames:
            if (mode == 'central'):
                if ((int(time.time()) - files[f]['mod_date'] > 300)):
                    # Regardless of the state, clear the array if we haven't heard from anyone about this file in the last
                    #   five minutes
                    if (args.debug): minorimpact.fprint(f"clearing {f}")
                    del files[f]
                elif (int(time.time()) - files[f]['mod_date'] < 30):
                    if (files[f]['state'] == 'upload'):
                        if (args.debug): minorimpact.fprint(f"write {f} to channel upload.{args.id}")
                        channel.basic_publish(exchange='synkler', routing_key='upload.' + args.id, body=pickle.dumps(files[f], protocol=4))
                    elif (files[f]['state'] == 'download'):
                        if (args.debug): minorimpact.fprint(f"write {f} to channel download.{args.id}")
                        channel.basic_publish(exchange='synkler', routing_key='download.' + args.id, body=pickle.dumps(files[f], protocol=4))
            elif (mode == 'upload'):
                if (files[f]['state'] in ('new', 'uploaded')):
                    if (args.debug): minorimpact.fprint(f"write {f} to channel new.{args.id}")
                    channel.basic_publish(exchange='synkler', routing_key='new.' + args.id, body=pickle.dumps(files[f]))
                elif (files[f]['state'] == 'done'):
                    if (cleanup_script is not None):
                        command = cleanup_script.split(' ')
                        for i in range(len(command)):
                            if command[i] == '%f':
                                command[i] = f'{f}'
                            elif command[i] == '%F':
                                command[i] = f'{file_dir}/{f}'
                        if (args.verbose): minorimpact.fprint("running cleanup script:" + ' '.join(command))
                        return_code = subprocess.call(command)
                        if (return_code != 0):
                            minorimpact.fprint(f"{f} cleanup script failed: {return_code}")
                        else:
                            if (args.verbose): minorimpact.fprint(" ... done")
                            # Since the file no longer lives in the download directory, delete it from the internal
                            #   dict.
                            del files[f]
                else:
                    # The file just lives here, so we just... ignore it, I guess
                    pass
            elif (mode == 'download'):
                if (files[f]['state'] == 'done'):
                    if ((int(time.time()) - files[f]['mod_date']) < 30):
                        # Keep sending the 'done' signal until we haven't heard from the upload server for a full 30 seconds.
                        if (args.debug): minorimpact.fprint("write {} to channel done.{}".format(f, args.id))
                        channel.basic_publish(exchange='synkler', routing_key='done.' + args.id, body=pickle.dumps(files[f]))
                    else:
                        # Once we're sure the upload server has done its thing, run the cleanup script and delete the file from the array.
                        if (cleanup_script is not None):
                            command = cleanup_script.split(' ')
                            for i in range(len(command)):
                                if command[i] == '%f':
                                    command[i] = f
                                elif command[i] == '%F':
                                    command[i] = file_dir + '/' + f
                            if (args.verbose): minorimpact.fprint("running cleanup script:" + ' '.join(command))
                            return_code = subprocess.call(command)
                            if (return_code == 0):
                                if (args.verbose): minorimpact.fprint(" ... done")
                            else:
                                minorimpact.fprint("{} cleanup script failed: {}".format(f, return_code))
                        del files[f]

        time.sleep(5)

    # TODO: Figure out a way to make sure these get called, or get rid of them.
    connection.close()
    # We don't strictly need to do this, but it's nice.
    os.remove(pidfile)

def scan_folder(file_dir, mode, files, keep_minutes, kill, verbose = False, debug = False):
    start_time = int(time.time())
    if (verbose): print("scan_folders thread: started")
    while(kill.is_set() is False):
        # Look at any local files and do what needs doing.
        for f in os.listdir(file_dir):
            if (re.search('^\\.', f)):
                continue

            mtime = os.path.getmtime(file_dir + '/' + f)
            size = minorimpact.dirsize(file_dir + '/' + f)
            if (f in files):
                if (size == files[f]['size'] and files[f]['mtime'] == mtime):
                    # The file has stopped changing, we can assume it's no longer being written to -- grab the md5sum.
                    if (files[f]['md5'] is None or files[f]['state'] == 'upload'):
                        if (verbose): print(f"collecting md5 of {f}")
                        md5 = minorimpact.md5dir(f'{file_dir}/{f}')
                        files[f]['md5'] = md5
                        if (debug): minorimpact.fprint(f"{f} md5:{md5}")
                        if (mode == 'upload'):
                            if (verbose): minorimpact.fprint(f"new file: {f}")
                            files[f]['state'] = 'new'
                else:
                    files[f]['size'] = size
                    files[f]['mtime'] = mtime
                    #files[f]['mod_date'] = int(time.time())
            else:
                if (mode == 'central'):
                    # These files are more than 30 minutes old and haven't been reported in, they can be
                    #   axed.
                    if (int(time.time()) - start_time > (keep_minutes * 60) and int(time.time()) - mtime > (keep_minutes * 60)):
                        if (verbose): minorimpact.fprint(f"deleting {file_dir}/{f}")
                        if (os.path.isdir(file_dir + '/' + f)):
                            shutil.rmtree(file_dir + '/' + f)
                        else:
                            os.remove(file_dir + '/' + f)
                elif (mode == 'upload'):
                    files[f] = {'filename':f, 'pickle_protocol':4, 'mtime':mtime, 'size':size, 'state':'churn', 'md5':None, 'dir':file_dir, 'mod_date':int(time.time()) }

        time.sleep(5)

    if (verbose): print("scan_folders thread: stopped")

if __name__ == '__main__':
    main()

