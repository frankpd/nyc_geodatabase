#Copies tables from a Spatialite database that have geometry stored
#in the final column, drops that geometry, and writes the rest to
#a PostgreSQL database 

import psycopg2, sqlite3, sys, os

os.chdir('..')

#Change these values as needed
sqdb='nyc_gdb_jan2020.sqlite' #sqlite db name
sqlike='%path_stations%' #used to do a pattern search for table names
pgdb='libpub' #postgres db name
pgport='5432'
pgschema='nyc_gdb' #postgres schema

#Get tables from SQLite
consq=sqlite3.connect(sqdb)
cursq=consq.cursor()

tabnames=[]

cursq.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '{}'".format(sqlike))
tabgrab = cursq.fetchall()
for item in tabgrab:
    tabnames.append(item[0])
    
if len(tabnames)==0:
    print('\nPROBLEM: Query returned no tables, exiting program with no changes \n')
    consq.close()
    sys.exit(0)

print('You are about import the following tables to the PostgreSQL DB')
for i in tabnames:
    print(i) 
answer = input('Are you sure you want to do this? (y/n): ')
if answer=='y':
    pass
else:
    print('\nEXITING PROGRAM, no changes made \n')
    consq.close()
    sys.exit(0)
 
pguser=input('Enter PostgreSQL user name: ')
pgpswd=input('Enter PostgreSQL password: ')
pghost=input('Enter PostgreSQL host / server: ')
conpg = None
  
for table in tabnames:
    cursq.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = '{}';".format(table))
    create = cursq.fetchone()[0]
    
    #Break create string to list, delete last item (assumed to be geometry)
    #Recreate string and statement ending
    createlist = create.split(',')
    lastitem=createlist[-1]
    del createlist[-1]
    print("Removed",lastitem)
    newcreate=','.join(createlist)
    newcreate=newcreate+');'
    
    #After grabbing the rows drop the geometry
    cursq.execute("SELECT * FROM {};".format(table))
    rows=cursq.fetchall()
    newrows=[]
    for r in rows:
        newrows.append(r[:-1])
    colcount=len(newrows[0])
    pholder='%s,'*colcount
    newholder=pholder[:-1]

#Write tables to PostgreSQL    
    try:    
        conpg = psycopg2.connect(database=pgdb, user=pguser, password=pgpswd,
                               host=pghost, port=pgport)
        curpg = conpg.cursor()
        curpg.execute("SET search_path TO {};".format(pgschema))
        conpg.commit()
        curpg.execute("DROP TABLE IF EXISTS {};".format(table))
        curpg.execute(newcreate)
        curpg.executemany("INSERT INTO {} VALUES ({});".format(table, newholder),newrows)
        conpg.commit()
        print('Created', table, 'with', curpg.rowcount,'records') 
    except psycopg2.DatabaseError as e:
        print (e)
        pguser=None
        pgpswd=None
        consq.close()
        sys.exit(1)         
    finally:     
        if conpg:
            conpg.close()

pguser=None
pgpswd=None                  
print('\nFinished writing to', pgdb, pgschema)
consq.close()
