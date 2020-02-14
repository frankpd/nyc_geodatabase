# Database Utilities

These scripts are used for QC and transferring tables from one database to another. They're intended for use with attribute tables; they can't be used for copying geometry columns. 

1. compare_tables: after new data is retrieved, processed, and loaded into a SQLite test database, this script evaluates differences between the new tables and existing tables in the nyc_geodatabase. The following comparisons are made to spot potential errors: equal number of columns and rows, matching and missing identifiers, and the difference between a given data value for the most recent and previous year.

2. sqlite_to_sqlite: once data is inspected and verified, this script is used to copy tables from the test database to what will be the next version of the nyc_gdb, rename the tables, and drop the tables from the previous year.

3. sqlite_to_postgres: the final step in the data acquisition, processing, checking, and publishing process is to archive the data on our local network database. This script copies data tables from the SQLite nyc_gdb to PostgreSQL. 

4. sqlite_to_postgres_minus_geometry: a variation of the previous script, used for features that have geometry. We never found a good solution for transferring Spatialite geometry to PostGIS, so instead this script omits the geometry columns when copying the tables. Geometry for point features is created in PostGIS manually after import, using numeric coordinate columns. An important prerequisite: this script assumes that geometry is stored in the last column of the table, and won't work otherwise. 
