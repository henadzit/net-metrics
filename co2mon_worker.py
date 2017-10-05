"""
A tool for monitoring CO2 and temperature using CO2 monitor and https://github.com/dmage/co2mon.
"""

import os
import subprocess
import sys
import time

import graphitesend


def main():
    co2mon_cmd = sys.argv[1]
    print('Starting co2mon_cmd={}'.format(co2mon_cmd))

    print('Init graphitesend')
    g = graphitesend.init(graphite_server=os.environ['GRAPHITE_SERVER'],
                          graphite_port=int(os.environ['GRAPHITE_PORT']),
                          prefix='co2mon')

    p = subprocess.Popen(co2mon_cmd, stdout=subprocess.PIPE)
    while True:
        retcode = p.poll()
        line = p.stdout.readline()

        if line.startswith('Tamb'):
            _, temp = line.split()
            g.send('temp', float(temp))
        elif line.startswith('CntR'):
            _, co2 = line.split()
            g.send('co2', float(co2))

        if retcode is not None:
            print('co2mon process failed with {}'.format(retcode))
            sys.exit(retcode)

        time.sleep(0.1)


if __name__ == '__main__':
    main()
