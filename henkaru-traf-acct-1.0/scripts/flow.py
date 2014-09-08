#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''API for generating internet for  inbound, outbound or both traffic reports.
It is wrapper functions over flow-stat.
Required installed package flow-tools.
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

def getclientbyip(ip):
    '''Get PTR record without domain from local DNS server'''
    import socket

    return socket.gethostbyaddr(ip)[0].split('.',1)[0]

def getmonthreport(month,year,mode,netprefix,path="/opt/flow"):
    '''Get month report of internet traffic for the network or a single ip 
    for `in|out|both` directions. The flows path is an optional argument.
    Returns a list.

    Usage: getmonthreport(4,2014,'in','192.168.1.')'''
    
    # dict with arguments for `flow-stat`
    direction = {'in':'-f8',
            'out':'-f9',
            'both':'-f10'}
    # Save output of `flow-cat ... | flow-stat -fX` to the list
    cmd1 = subprocess.Popen(["flow-cat", '{0}/{1}/{1}-{2:02d}/'.format(path, year, month)],stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(["flow-stat", direction[mode]],stdin=cmd1.stdout,stdout=subprocess.PIPE)
    out = []
    for line in cmd2.communicate()[0].split('\n'):
        # Clean output from comments and empty strings
        if not (line.startswith('#') or len(line) == 0):
            try:
                if mode == 'both':
                    (src,dst,flows,doctets,pkts) = line.split()
                    # add to result list only strings with 'netprefix' pattern
                    if src.startswith(netprefix) or dst.startswith(netprefix):
                        out.append([src,dst,doctets])
                else:
                    (ip,flows,doctets,pkts) = line.split()
                    if ip.startswith(netprefix):
                        out.append([ip,doctets])
            except:
                pass
    return sorted(out, key=lambda x: int(x[-1]), reverse=True)

def getmonthsummary(month,year,netprefix,path="/opt/flow"):
    '''Get summary month report for the network or a single ip. 
    The flows path is an optional argument.
    Returns  the list: [incoming,outcomming,sum]

    Usage: getmonthsummary(4,2014,'192.168.1.')'''

    tmp = getmonthreport(month,year,'both',netprefix,path)
    out = []
    out.append(sum([doctets for src,dst,doctets in tmp if dst.startswith(netprefix)]))
    out.append(sum([doctets for src,dst,doctets in tmp if src.startswith(netprefix)]))
    out.append(out[0]+out[1])
    return out

def main():
    netprefix='192.168.1.'
    if len(sys.argv) == 2:
        getusers()
    else:
        print "Usage: %s [options] <netflow directory>" % sys.argv[0]

if __name__ == "__main__":
    main()
