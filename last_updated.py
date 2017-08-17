#!/usr/bin/env python

import datetime
import hashlib
import json


class LastUpdated():
    def __init__(self, file='last-updated.json'):
        self.file = file

    def read(self):
        with open(self.file, 'r') as f:
            data = json.load(f)

        return {
            'sha1': data['sha1'],
            'timestamp': datetime.datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f'),
        }

    def read_timestamp(self):
        return self.read()['timestamp']

    def write(self, sha1, timestamp):
        with open(self.file, 'w') as f:
            json.dump({
                'sha1': sha1,
                'timestamp': timestamp.isoformat(),
            }, f, sort_keys=True)

    def hash(self, data):
        return hashlib.sha1(data).hexdigest()

    def update(self, data):
        sha1 = self.hash(data)
        try:
            last_update = self.read()
        except Exception as e:
            print(e)
            last_update = None

        updated = False
        if last_update is None or last_update['sha1'] != sha1:
            last_update = {
                'sha1': sha1,
                'timestamp': datetime.datetime.utcnow(),
            }
            self.write(**last_update)
            updated = True

        return last_update, updated


if __name__ == '__main__':
    last_updater = LastUpdated()
    with open('database/amiibo.json', 'rb') as f:
        last_update, updated = last_updater.update(f.read())

    if updated:
        print('Updated: {}'.format(last_updater.file))

    print('sha1: {}'.format(last_update['sha1']))
    print('timestamp: {}'.format(last_update['timestamp'].isoformat()))
