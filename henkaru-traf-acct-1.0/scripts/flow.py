#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''API for generating internet for  inbound, outbound or both traffic reports.
It is just wrapper functions over flow-stat.
'''

__author__ = "Alexey Alexashin (alexashin.a.n@yandex.ru)"
__version__ = "$Revision: 1.0 $"
__copyright__ = "Copyright (c) 2014 Alexey Alexashin"
__license__ = "Python"


import sys, subprocess
#import pdb

def getusers():
    '''Get user and their IP addresses from mysql database.
    Returns dict{ip:user}'''
    pass

def getptr():
    '''Get PTR record from local DNS server'''

def getmonthreport(month,year,mode):
    '''Get list of month report for incoming, outcoming or both traffic mode direction.
    Usage: flow_month(4,2014,'in')
    
    Returns list columns for the following modes:
        in   - [dstIP,doctets]
        out  - [srcIP,doctets]
        both - [srcIP,dstIP,doctets]'''
    
    direction = {'in':'-f8',
            'out':'-f9',
            'both':'-f10'}
    path = "/opt/flow"
    cmd1 = subprocess.Popen(["flow-cat", '{0}/{1}/{1}-{2:02d}/'.format(path, year, month)],stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(["flow-stat", direction[mode]],stdin=cmd1.stdout,stdout=subprocess.PIPE)
    out = []
    for line in cmd2.communicate()[0].split('\n'):
        if not (line.startswith('#') or len(line) == 0):
            try:
                if mode == 'both':
                    (src,dst,flows,doctets,pkts) = line.split()
                    out.append([src,dst,doctets])
                else:
                    (ip,flows,doctets,pkts) = line.split()
                    out.append([ip,doctets])
            except:
                pass
    return out

def getmonthreportbyip():
    '''Get list of month report for incoming, outcoming or both traffic mode direction.
    Usage: flow_month(4,2014,'in')
    
    Returns list columns for the following modes:
        in   - [dstIP,doctets]
        out  - [srcIP,doctets]
        both - [srcIP,dstIP,doctets]'''


def main():
    lanprefix='192.168.1.'
    if len(sys.argv) == 2:
        getusers()
    else:
        print "Usage: %s [options] <netflow directory>" % sys.argv[0]

if __name__ == "__main__":
    main()
