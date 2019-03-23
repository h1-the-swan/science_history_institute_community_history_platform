#!/usr/bin/env bash

function usage ()
{
	echo "Usage :  remote-server-addr $0 [options] [--]

    Options:
    -h|help       Display this message
    -r|remote-addr    remote address for ssh (e.g., 'ubuntu@<public-ec2-dns>')
    -i|identity-file    ssh identity file"

}    # ----------  end of function usage  ----------

function main() {
	ssh $remote_addr -t -i $identity_file "
		cd science_history_institute_community_history_platform
		source backup_postgres.sh
		tar -czf database_snapshots_${now}.tgz database_snapshots
		exit
		"
	scp -i $identity_file ${remote_addr}:/home/ubuntu/science_history_institute_community_history_platform/database_snapshots_${now}.tgz .
}

#-----------------------------------------------------------------------
#  Handle command line arguments
#-----------------------------------------------------------------------

now="$(date +'%Y%m%d%H%M')"

while getopts ":hr:i:" opt
do
  case $opt in

	h|help     )  usage; exit 0   ;;

	r|remote-addr  )  
		remote_addr=$OPTARG
		;;

	i|identity-file  )  
		identity_file=$OPTARG
		;;

	* )  echo -e "\n  Option does not exist : $OPTARG\n"
		  usage; exit 1   ;;

  esac    # --- end of case ---
done
shift $(($OPTIND-1))

main
