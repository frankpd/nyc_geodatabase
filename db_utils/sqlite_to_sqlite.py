#Copy new tables from temporary SQLite database to permanent one and
#drop old tables from permanent database
#Recreates tables and inserts records to preserve keys and constraints

import sqlite3, os, sys
os.chdir('..')

#MODIFY these values to pull from the right sources
#db1 should be the original db
db1='nyc_gdb_jan2019.sqlite'
tabdrop=['b_zctas_2016biz_emp','b_zctas_2016biz_ind','b_zctas_2016biz_indcodes']

#db2 should be the test database
db2=os.path.join('census_zbp/outputs/testdb.sqlite')
tabadd=['zbp2016emp','zbp2016ind','zbp2016indcodes']

def table_exists(dbalias,dbname,tablist):
    for t in tablist:
        cur.execute("SELECT name FROM {}.sqlite_master WHERE type='table' AND name = '{}'".format(dbalias,t))
        tabgrab = cur.fetchone()
        if tabgrab == None:
            print('There is no table in',dbname,'named',t)
            print('EXITING PROGRAM, no changes made \n')
            con.close()
            sys.exit(0)
        else:
            pass

#Main script begins here
con = sqlite3.connect(db1)
cur = con.cursor()

cur.execute("ATTACH '{}' AS db2;".format(db2))

#Check to make sure tables exist / are spelled correctly in both dbs
table_exists('main',db1,tabdrop)
table_exists('db2',db2,tabadd)

print('You are about to drop the following tables from',db1)
for i in tabdrop:
    print(i) 
print('\nAnd add these tables from',db2)
for j in tabadd:
    print(j) 
answer = input('Are you sure you want to do this? (y/n): ')

if answer=='y':
    for t in tabdrop:
        cur.execute('DROP TABLE {};'.format(t))
        print('Dropped table',t)
    for t in tabadd:
        cur.execute("SELECT sql FROM db2.sqlite_master WHERE type='table' AND name = '{}';".format(t))
        create = cur.fetchone()[0]
        cur.execute("SELECT * FROM db2.{};".format(t))
        rows=cur.fetchall()
        colcount=len(rows[0])
        pholder='?,'*colcount
        newholder=pholder[:-1]
        cur.execute(create)
        cur.executemany("INSERT INTO {} VALUES ({});".format(t, newholder),rows)
        con.commit() 
        print('Added table',t)
else:
    print('\nEXITING PROGRAM, no changes made \n')
    con.close()
    sys.exit(0)
    
con.commit()
con.close()
