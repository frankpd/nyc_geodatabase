#Frank Donnelly, Geospatial Data Librarian
#May 22, 2017
#Copies tables and data from a SQLite database and recreates them
#in a PostgreSQL database

#Note - need to test / update this script

import psycopg2, sqlite3, sys

#Change these values as needed

sqdb=r'S:\LibShare\Shared\Divisions\Graduate\GEODATA\nyc_geodatabase\all_dbs\nyc_gdb_jan2019a\nyc_gdb_jan2019a\nyc_gdb_jan2019.sqlite'
sqlike='%metadata%'
pgdb='libpub'
pguser=''
pgpswd=''
pghost='libdata1v.bc.baruch.cuny.edu'
pgport='5432'
pgschema='nyc_gdb'

consq=sqlite3.connect(sqdb)
cursq=consq.cursor()

tabnames=[]

cursq.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%s'" % sqlike)
tabgrab = cursq.fetchall()
for item in tabgrab:
    tabnames.append(item[0])

   
for table in tabnames:
    cursq.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = ?;", (table,))
    create = cursq.fetchone()[0]
    cursq.execute("SELECT * FROM %s;" %table)
    rows=cursq.fetchall()
    colcount=len(rows[0])
    pholder='%s,'*colcount
    newholder=pholder[:-1]
    
    try:
         
        conpg = psycopg2.connect(database=pgdb, user=pguser, password=pgpswd,
                               host=pghost, port=pgport) 
        curpg = conpg.cursor()
        curpg.execute("SET search_path TO %s;" %pgschema)
        curpg.execute("DROP TABLE IF EXISTS %s;" %table)
        curpg.execute(create)
        curpg.executemany("INSERT INTO %s VALUES (%s);" % (table, newholder),rows)
        conpg.commit()
        print('Created', table)
       
    except psycopg2.DatabaseError as e:
        print ('Error %s' % e)    
        sys.exit(1)
          
    finally:
        
        if conpg:
            conpg.close()

consq.close()
