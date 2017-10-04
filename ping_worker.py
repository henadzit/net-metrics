import sys
import os
import time

import graphitesend

import ping


INTERVAL = 1  # sec


def main():
    hostname = sys.argv[1]
    print('Starting hostname={}'.format(hostname))

    print('Init graphitesend')
    g = graphitesend.init(graphite_server=os.environ['GRAPHITE_SERVER'],
                          graphite_port=int(os.environ['GRAPHITE_PORT']),
                          prefix='ping.{}'.format(hostname.replace('.', '_')))

    while True:
        start = time.time()
        delay = ping.do_one(hostname, 2)

        if delay:
            print('delay={}'.format(delay))
            g.send('time', delay)
        else:
            print('delay is None')

        end = time.time()
        if end - start < INTERVAL:
            time.sleep(INTERVAL - end + start)


if __name__ == '__main__':
    main()