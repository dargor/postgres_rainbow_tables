# postgres_rainbow_tables

PoC of rainbow tables using PostgreSQL.

# Setup

**Caution:** these commands will *overwrite* any database named `rainbows`, be careful !

```
cd sql/
vim roles.sql # create the user in psql, and add its password to your ~/.pgpass file
./drop_db.sh # if you have a previous rainbows database
./create_db.sh
cd ../
./import.py
```

After some time (OWASP SecLists took 27 minutes for 13M passwords), your database is ready.

# Queries

Use `./query.py -v <<hash>>` to find a password from its hash.

With the test sample, you can do this :

```
cat test.txt
echo -n 123123 | sha224sum -
./query.py -v 23d5c51afade7a8701186250777f3c055c94984ce3d4aaed11438c0c
```

This should give you `123123` back.

# Debug

You might want to run this to get some useful (or not) messages :

```
export DEBUG=Y
```

# License

ISC.
