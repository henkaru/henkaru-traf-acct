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


from datetime import date
import sys, subprocess
#import pdb

monthdict = {1:"Январь", 2:"Февраль", 3:"Март",
            4:"Апрель",5:"Май",6:"Июнь",
            7:"Июль",8:"Август",9:"Сентябрь",
            10:"Октябрь",11:"Ноябрь",12:"Декабрь"}


def getusers():
    '''Get user and their IP addresses from mysql database.
    Returns dict{ip:user}'''
    
    import  MySQLdb
    dbhost='localhost'
    dbname='traf'
    dbuser='traf'
    dbpassword=''
    sql = 'select ip, user from `user`'
    try:
        con = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname, passwd=dbpassword)
        cur = con.cursor()
        cur.execute(sql)
        out = cur.fetchall()
    except MySQLdb.Error:
        print(con.error())
    finally:
        con.close()
    return dict(out)

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
    users = getusers()
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
                        out.append([users.get(ip,'служебный'),ip,doctets])
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

def main(month,year):
    '''Monthly incoming report by clients'''

    cost = 0.3
    limit = 500.00
    netprefix='192.168.1.'
    report = getmonthreport(month,year,'in',netprefix,path="/opt/flow")
    for line in report:
        line[-1] = float(line[-1])/2**20  # Convert doctets to megabytes
        if line[-1] > limit:
            line.append(line[-1] - limit) # Add column 'Limit overflow'
        else:
            line.append(0.0)
        line.append(line[-1]*cost)
    report.append(['Итого:',sum(row[2] for row in report)])
    report.insert(0, ['Пользователь','IP-адрес',"Трафик,Мб","Превышение,Мб","Стоимость,руб."])
    report.insert(0, 'Отчет по входящему трафику за %s %d' % (monthdict[month], year))
    return report

def main_csv(month,year):
    '''Monthly incoming report in csv'''
    out = main(month,year)
    csv = str(out[0]) + '\n'
    csv += "{0};{1};{2};{3};{4}\n".format(*out[1])
    for line in out[2:-2]:
        csv += "{0};{1};{2};{3};{4}\n".format(*line) 
    csv += '{0};{1}'.format(*out[-1])
    return csv

def main_stdout(month,year):
    '''Monthly incoming report with alignment columns'''
    out = main(month,year)
    print out[0]
    print str(out[1][0]).decode('utf-8').ljust(25), "{0:<20} {1:<18} {2:<27} {3:<15}".encode('utf-8').format(*out[1][1:])
    print '_'*83
    for line in out[2:-2]:
        print str(line[0]).decode('utf-8').ljust(25), "{0:<15} {1:<10.2f} {2:<15.2f} {3:<10.2f}".format(*line[1:]) 
    print '_'*83
    print '{0:>37}          {1:5.2f}'.format(*out[-1])

if __name__ == "__main__":
    if len(sys.argv) == 3:
        month=int(sys.argv[1])
        year=int(sys.argv[2])
    elif len(sys.argv) == 1:
        month=date.today().month
        year=date.today().year
    else:
        print "Usage: %s M YYYY\nIf no arguments returns report for current month" % sys.argv[0]
        sys.exit(1)
    main_stdout(month,year)
