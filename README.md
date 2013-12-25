sp_migrate
----------
Migrates an old Access MDB database into our new PostgreSQL format.

Directories
-----------
sp_migrate/hunter:	Contains models for the Source (MDB) Hunter database.
sp_migrate/source:	Contains models for the Source (MDB) SmartProg and SmartData databases.
sp_migrate/target:	Contains models for the Target (PostgreSQL) database.
sp_migrate/target/psql:	Contains dumps of the migrated target database.
sp_migrate/mdb:		Contains shells scripts to convert an Access MDB database into PSQL statements.  Uses mdb-tools.
sp_migrate/sp_migrate:	Django Project


HOWTO
-----
The Quick Rundown
1) Use one of the mdber scripts in sp_migrate/mdb to convert .mdb into .psql
2) Create postgres database, import .psql files to create MDB database in PostgreSQL
3) Run sp_migrate/source/id_tables.psql on the SmartProg/SmartData PostgreSQL database to add .id columns for Django
4) Configure 'source_db' in sp_migrate/sp_migrate/settings.py, its the SmartProg/SmartData PostgreSQL database.
5) Configure 'target_db' in sp_migrate/sp_migrate/settings.py, create the database in PostgreSQL.  This is our target migration database.
6) Run 'python manage.py syncdb --database=target_db' to create the target database table structure.
7) Run 'python merge.py' and follow the misleading prompts.


sp_migrate/target/psql:
Dumps here have been created using pg_dump.  To load the database first create the database in postgres (CREATE DATABASE sp_target_migrate) then 'psql sp_target_migrate < in_file.psql'

BUGS
----
Please report bugs to anybody but us.
