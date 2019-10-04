#This script checks a newly generated table in a test database to the previous
#year's data in a permanent database as a quality control measure, to verify
#that there are an equal number of rows and columns in each table and that data
#values are not subtantively different. 

#NOTE - need to update, make the left join queries into one function

import os, sqlite3

os.chdir('..')

#Modify these values to test different sources
db1='nyc_gdb_jan2019.sqlite'
tab1='b_zctas_2016biz_ind'
uid1='zcta5'
col1='n00'

db2=os.path.join('census_zbp/outputs/testdb.sqlite')
tab2='zbp2016ind'
uid2='zcta5'
col2='n00'

con = sqlite3.connect(db1)
cur = con.cursor()

cur.execute("ATTACH '{}' AS db2;".format(db2))

#Count and compare columns
cur.execute('PRAGMA table_info({});'.format(tab1))
cols1=len(cur.fetchall())
cur.execute('PRAGMA table_info({});'.format(tab2))
cols2=len(cur.fetchall())

if cols1==cols2:
    print('Both tables have', cols1, 'columns')
else:
    print('WARNING: table 1 has', cols1,'columns but table 2 has',cols2)

#Count and compare rows
cur.execute('SELECT COUNT(*) FROM {};'.format(tab1))
rows1 = cur.fetchone()
cur.execute('SELECT COUNT(*) FROM db2.{};'.format(tab2))
rows2 = cur.fetchone()

if rows1[0]==rows2[0]:
    print('Both tables have',rows1[0], 'rows')
else:
    print('WARNING: table 1 has',rows1[0],'rows but table 2 has',rows2[0],'\n')
    
    lquery1='''SELECT a.{0}
    FROM {2} a
    LEFT JOIN {3} b ON a.{0}=b.{1}
    WHERE b.{1} IS NULL;'''.format(uid1,uid2,tab1,tab2)
    cur.execute(lquery1)
    left_ids=cur.fetchall()
    if len(left_ids)>0:
        print('The following IDs from', tab1, 'have no matching records in',tab2)
        for i in left_ids:
            print(i)
    
    lquery2='''SELECT b.{1}
    FROM {3} b
    LEFT JOIN {2} a ON a.{0}=b.{1}
    WHERE a.{0} IS NULL;'''.format(uid1,uid2,tab1,tab2)
    cur.execute(lquery2)
    right_ids=cur.fetchall()
    if len(right_ids)>0:
        print('The following IDs from', tab2, 'have no matching records in',tab1)
        for j in right_ids:
            print(j)
    
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
print(uid1,col1,col2,'diff','pct')
for t in joined[0:10]:
    print(t)

print('\n')  
print('Bottom ten records with largest negative difference:')  
print(uid1,col1,col2,'diff','pct')    
for b in joined[-10:]:
    print(b)
 
print('\n')  
print('You can inspect all', jrows,'records in the list "joined"')
    
con.close()
