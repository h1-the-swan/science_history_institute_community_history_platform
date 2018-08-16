Packaging Science History Institute Community History Platform using Docker.

Relies on the Hypothesis service, and the Hypothesis client.

Packaged using Docker Compose.

Uses the Community Science Platform as a submodule.
Use `git submodule init` and `git submodule update`

Need to import oral histories into `community_history_platform/flask/app/static/LSF_oral_histories/`

After that, run:
`sudo docker-compose build`
`sudo docker-compose up`

This will build the images, and then run all of the services concurrently in Docker containers.

### Useful commands

#### To restore from file-system level backup:

Create backup (example):
`sudo docker run --rm --volumes-from science_history_institute_community_history_platform_postgres_1 -v $(pwd)/database_snapshots:/backup busybox tar cfz /backup/backup_postgresdata_01_20180814.tar /var/lib/postgresql/data`

Restore from backup (example):
`sudo docker stop science_history_institute_community_history_platform_postgres_1`
`sudo docker run --rm --volumes-from science_history_institute_community_history_platform_postgres_1 -v $(pwd)/database_snapshots:/backup busybox tar xfz /backup/backup_postgresdata_01_20180814.tar --overwrite`
`sudo docker start science_history_institute_community_history_platform_postgres_1`
(This will cause a SQLalchemy OperationalError when you try to use the web app, but reload and it should work).


#### To restore from SQL dump:

Create backup (example):
Backup `postgres` database:
`sudo docker-compose exec postgres pg_dump postgres --clean -U postgres > database_snapshots/testdump_01_postgres_clean.sql`
Backup chp database:
`sudo docker-compose exec postgres pg_dump chp --clean -U postgres > database_snapshots/testdump_01_chp_clean.sql`

Restore from backup (example):
(With all containers running)
`sudo docker-compose exec postgres psql -f /database_snapshots/testdump_01_postgres_clean.sql -U postgres --dbname=postgres`
`sudo docker-compose exec postgres psql -f /database_snapshots/testdump_01_chp_clean.sql -U postgres --dbname=chp`
