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
	git submodule update --recursive --remote
	tar -czf chp_app.tgz ./science_history_institute_chp_app
	scp -i $identity_file chp_app.tgz ubuntu@${remote_addr}:/home/ubuntu/science_history_institute_community_history_platform
	ssh ubuntu@$remote_addr -t -i $identity_file "
		cd science_history_institute_community_history_platform
		tar -xzf chp_app.tgz
		exit
		"
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
