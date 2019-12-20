#This script checks a newly generated table in a test database to the previous
#year's data in a permanent database as a quality control measure, to verify
#that there are an equal number of rows and columns in each table and that a
#given attribute's values are not subtantively different. 

import os, sqlite3
os.chdir('..')

#Modify these values to test different sources
#db1 should be the original db
db1='nyc_gdb_jan2019.sqlite' 
tab1='b_zctas_2016biz_ind'
uid1='zcta5'
col1='n00'
#db2 should be the test database
db2=os.path.join('census_zbp/outputs/testdb.sqlite')
tab2='zbp2016ind'
uid2='zcta5'
col2='n00'

def leftjoin(left_id,left_t,right_id,right_t):
    lquery='''SELECT a.{0}
    FROM {1} a
    LEFT JOIN {3} b ON a.{0}=b.{2}
    WHERE b.{2} IS NULL;'''.format(left_id,left_t,right_id,right_t)
    cur.execute(lquery)
    no_ids=cur.fetchall()
    if len(no_ids)>0:
        print('The following IDs from', left_t, 'have no matching records in',right_t)
        for i in no_ids:
            print(i)
    
con = sqlite3.connect(db1)
cur = con.cursor()

cur.execute("ATTACH '{}' AS db2;".format(db2))

#Count and compare columns
cur.execute('PRAGMA table_info({});'.format(tab1))
cols1=len(cur.fetchall())
cur.execute('PRAGMA db2.table_info({});'.format(tab2))
cols2=len(cur.fetchall())

if cols1==cols2:
    print('Both tables have', cols1, 'columns')
else:
    print('WARNING:', tab1, 'has', cols1,'columns but', tab2, 'has',cols2)

#Count and compare rows
cur.execute('SELECT COUNT(*) FROM {};'.format(tab1))
rows1 = cur.fetchone()
cur.execute('SELECT COUNT(*) FROM db2.{};'.format(tab2))
rows2 = cur.fetchone()

#Identify records with no match in opposite table
if rows1[0]==rows2[0]:
    print('Both tables have',rows1[0], 'rows')
else:
    print('WARNING:', tab1, 'has', rows1[0], 'rows but', tab2, 'has', rows2[0],'\n')
    
    leftjoin(uid1,tab1,uid2,tab2)
    leftjoin(uid2,tab2,uid1,tab1)

#Compare current value to previous year    
jquery='''SELECT a.{0},a.{2},b.{3},b.{3}-a.{2} AS diff, 
((CAST (b.{3} AS REAL)-CAST (a.{2} AS REAL)) /CAST (a.{2} AS REAL)) * 100 as pct_chng
FROM {4} a, db2.{5} b
WHERE a.{0}=b.{1}
ORDER BY diff DESC;'''.format(uid1,uid2,col1,col2,tab1,tab2)
cur.execute(jquery)
joined=cur.fetchall()
jrows=len(joined)

print('\n')
print('Top ten records with largest positive difference:')
print(uid1,col1+'_t1',col2+'_t2','diff','pct')
for t in joined[0:10]:
    print(t)

print('\n')  
print('Bottom ten records with largest negative difference:')  
print(uid1,col1+'_t1',col2+'_t2','diff','pct')    
for b in joined[-10:]:
    print(b)
 
print('\n')  
print('You can inspect all', jrows,'records in the list "joined"')
    
con.close()
