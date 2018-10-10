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

### To install on AWS EC2 instance:
- Launch instance (t2.medium Ubuntu instance; 4GiB RAM, 8GiB storage)
  - In Step 6: Configure Security Group, add a rule for HTTP (allow incoming HTTP requests on port 80)
	- You will need to either generate SSH keys or use an existing key pair to access the server via SSH
- Now that the EC2 instance is running, copy the Public DNS address (e.g., `ec2-34-212-224-177.us-west-2.compute.amazonaws.com`). This will be referred to as `<PUBLIC-DNS>` below.
- Zip up the contents of this directory. Make sure before you do this that all files are there, including the git submodule containing the frontend app (`science_history_institute_chp_app/`) and any database snapshots (in `database_snapshots/`)
  - `cd ..`
	- `tar -cvzf science_history_institute_community_history_platform.tgz science_history_institute_community_history_platform`
= Transfer the code to the EC2 instance
  - `scp -i <SSH-PRIVATE-KEY> science_history_institute_community_history_platform.tgz ubuntu@<PUBLIC-DNS>:/home/ubuntu`
- Log into the EC2 instance and unzip the files:
  - `ssh -i <SSH-PRIVATE-KEY> ubuntu@<PUBLIC-DNS>`
	- `tar -xvzf science_history_institute_community_history_platform.tgz`
	- `cd science_history_institute_community_history_platform`
- Install docker-ce and docker-compose on the EC2 instance:
	- `source install-docker.sh`
- Modify some important environment variables:
  - `cd ~/science_history_institute_community_history_platform/`
	- `python3 modify_envfile.py --ec2`
- Run Docker Compose to start all of the components:
  - `sudo docker-compose build && sudo docker-compose up`
- Restore a database snapshot:
	- Press CTRL-Z, then run the command `bg` to move the process to the background
  - `source load_database_snapshot.sh`
	  - (see the comments in `load_database_snapshot.sh` to understand what it does)

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
May need to also run:
`sudo docker-compose exec hypothesis-h /var/lib/hypothesis/bin/hypothesis search reindex`
