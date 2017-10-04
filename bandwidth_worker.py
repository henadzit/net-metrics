import multiprocessing
import os
import urllib
import random
import time

import graphitesend


# pick something in close proximity
DOWNLOAD_URL = 'http://ftp.byfly.by/debian-cd/9.1.0/i386/iso-dvd/debian-9.1.0-i386-DVD-1.iso'
INTERVAL = 3.0
PERIOD = 10.0


def main():
    print('Starting download_url={}'.format(DOWNLOAD_URL))

    print('Init graphitesend')
    g = graphitesend.init(graphite_server=os.environ['GRAPHITE_SERVER'],
                          graphite_port=int(os.environ['GRAPHITE_PORT']),
                          prefix='bandwidth')

    while True:
        start = time.time()

        filename = 'download{0:07d}'.format(random.randint(0, 1000000))
        p = multiprocessing.Process(target=_download, args=(filename,))
        p.start()
        time.sleep(INTERVAL)
        p.terminate()

        size = os.path.getsize(filename)
        bandwidth = size / INTERVAL
        print('bandwidth={}'.format(bandwidth))
        g.send('time', bandwidth)

        os.remove(filename)

        end = time.time()
        if end - start < PERIOD:
            time.sleep(PERIOD - end + start)


def _download(filename):
    urllib.urlretrieve(DOWNLOAD_URL, filename)


if __name__ == '__main__':
    main()