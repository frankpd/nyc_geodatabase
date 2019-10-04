#Copy new tables from temporary SQLite database to permanent one, and
#drop old tables from permanent database

#NOTE - need to change method for copying tables, as primary keys are not
#carried over

import sqlite3, os, sys
os.chdir('..')

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
    
#MODIFY these values to pull from the right sources
db1='nyc_gdb_jan2019.sqlite'
tabdrop=['b_zctas_2016biz_emp','b_zctas_2016biz_ind','b_zctas_2016biz_indcodes']

db2=os.path.join('census_zbp/outputs/testdb.sqlite')
tabadd=['zbp2016emp','zbp2016ind','zbp2016indcodes']

#Main script begins here
con = sqlite3.connect(db1)
cur = con.cursor()

cur.execute("ATTACH '{}' AS db2;".format(db2))

table_exists('main',db1,tabdrop)
table_exists('db2',db2,tabadd)

print('You are about to drop the following tables from',db1)
for i in tabdrop:
    print(i) 
print('\nAnd add these tables')
for j in tabadd:
    print(j) 
answer = input('Are you sure you want to do this? (y/n): ')

if answer=='y':
    for t in tabdrop:
        cur.execute('DROP TABLE {};'.format(t))
    print('Tables dropped')
    for t in tabadd:
        cur.execute('''CREATE TABLE {} AS
                    SELECT *
                    FROM db2.{};'''.format(t,t))
    print('Tables added')
else:
    print('\nEXITING PROGRAM, no changes made \n')
    con.close()
    sys.exit(0)
    
con.commit()
con.close()
