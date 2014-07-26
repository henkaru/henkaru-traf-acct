#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''Rotate script converts binary netwflow files to human readable data
and exports them to database.
It`s used by flow-capture

rotate.py <netflow file> -> return csv and load it to traf.traf database
'''

__author__ = "Alexey Alexashin (alexashin.a.n@yandex.ru)"
__version__ = "$Revision: 1.0 $"
__copyright__ = "Copyright (c) 2014 Alexey Alexashin"
__license__ = "Python"


import sys
import pdb

def flow2csv(flowname=sys.argv[1],file2db='/opt/flow/traf.csv'):
    '''Create csv with src, dst, doctets columns from netflow flie'''
    
    import  subprocess
    from datetime import datetime
    from os.path import getmtime, basename
    
    
    timestamp = basename(flowname).split('.')[1:]        # Extract from filename timestamp string
    tmp = timestamp[1].split('+')[0]                     # and format it
    tmp = ':'.join((tmp[:2],tmp[2:4],tmp[4:]))           # to something like
    timestamp = "'" + timestamp[0] + ' ' + tmp + "'"     # 'YYYY-MM-DD hh:mm:ss'
    
    f = open(flowname)
    todb = open(file2db,'w')
    flow_cmd = subprocess.Popen(["flow-stat","-f10"],stdin=f,stdout=subprocess.PIPE)
    out = flow_cmd.communicate()[0].split('\n')
    f.close()
    for line in out:
        if not (line.startswith('#') or len(line) == 0):
            try:
                (src,dst,flows,doctets,pkts) = line.split()
                src = "'" + src + "'"
                dst = "'" + dst + "'"
                todb.write(','.join((timestamp,src,dst,doctets)) + '\n')
            except:
                pass
    todb.close()

def load2db(dbhost='localhost',dbname='traf',dbuser='traf',dbpassword='',file2db='/opt/flow/traf.csv'):
    '''Load  data from csv to database `traf`'''
    import  MySQLdb
    
    f = open(file2db)
    sql_data = ','.join([ '(%s)' % line for line in f.readlines()])
    f.close()
    sql = 'insert into `traf` (timestamp,src,dst,bytes) values %s' % sql_data
    
    try:
        con = MySQLdb.connect(host=dbhost, user=dbuser, db=dbname, passwd=dbpassword)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
    except MySQLdb.Error:
        print(con.error())
    finally:
        con.close()

def main():
    if len(sys.argv) == 2:
        flow2csv()
        load2db()
    else:
        print "Usage: %s <netflow file>" % sys.argv[0]

if __name__ == "__main__":
    main()
