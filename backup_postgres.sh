# Ask for the user password
# Script only works if sudo caches the password for a few minutes
sudo true

now="$(date +'%Y%m%d%H%M')"

dir_name="database_snapshots/pgdump_postgres_$now"
mkdir $dir_name

fname="${dir_name}/pgdump_postgres_clean_$now.sql"
echo "Backing up postgres database to file: $fname"
sudo docker-compose exec postgres pg_dump postgres --clean -U postgres > $fname

fname="${dir_name}/pgdump_chp_clean_$now.sql"
echo "Backing up chp database to file: $fname"
sudo docker-compose exec postgres pg_dump chp --clean -U postgres > $fname

fname="${dir_name}/submodule_commit_hash_$now.txt"
git submodule > $fname
