#! /usr/bin/env python3

import sqlite3,os

addrP=[]

def get_addr():
	f = open("addrbook")
	line = f.readline()
	while line:
		_line=line.split()
		if _line:
			addrP.append(_line)
		line = f.readline()
	f.close()
	# print(addrP)

def write_sql():
	conn = sqlite3.connect('bshn.db')
	cur = conn.cursor()
	cur.execute("""DROP TABLE IF EXISTS addr;""")
	cur.execute("""CREATE TABLE IF NOT EXISTS addr (addr_xch varchar(1000), addr_number INTEGER);""")
	for i in range(0,len(addrP)):
		cur.execute("""INSERT INTO addr VALUES(?,?);""",(addrP[i][0],addrP[i][1]))
	get=cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()

def get_sql():
	conn = sqlite3.connect('bshn.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM addr") 
	get=cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()
	print(get)
	print(len(get))

def get_sql_bshn():
	conn = sqlite3.connect('bshn.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM bshn") 
	get=cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()
	for i in get:
		print(i)

get_addr()
write_sql()

get_sql()

# get_sql_bshn()