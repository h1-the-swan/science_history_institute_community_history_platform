# On AWS EC2 instances, you run python programs with `python3` command (for now, this may change someday)
PYTHON_CMD=python3

# Ask for the user password
# Script only works if sudo caches the password for a few minutes
sudo true

# select the most recent snapshot
SNAPSHOT_DIR=`ls -dr database_snapshots/*/ | head -n 1`
POSTGRES_FILE=`ls $SNAPSHOT_DIR/pgdump_postgres_clean_*.sql | head -n 1`
CHP_FILE=`ls $SNAPSHOT_DIR/pgdump_chp_clean_*.sql | head -n 1`
# This modifies the database snapshot contents for use on this EC2 instance
$PYTHON_CMD modify_postgres_sql.py $POSTGRES_FILE -o $POSTGRES_FILE --ec2

# This restores the snapshot for the backend database
sudo docker-compose exec postgres psql -f $POSTGRES_FILE -U postgres --dbname=postgres

# This restores the snapshot for the frontend database
sudo docker-compose exec postgres psql -f $CHP_FILE -U postgres --dbname=chp

# This is necessary for the changes to be recognized (and used by elastic search)
sudo docker-compose exec hypothesis-h /var/lib/hypothesis/bin/hypothesis search reindex
