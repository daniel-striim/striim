#This program will automatically manage downloading and installation of Striim sample apps
#This can be used in conjunction with local installs or VMs
#The following apps exist:
#  - OBT: Oracle Bank Transcation

downloadprogram="$1"

#if [ -z "$downloadprogram" ]
#then
#      echo "Program must be provided. Available programs are:"
#	  echo "OBT: Oracle Bank Transcation"
#else
      
#fi
# 
# 
echo "Loading $downloadprogram"
	  case $downloadprogram in

	    OracleTransaction | OBT)
	      echo -n "OracleTransaction Found."
		  echo
		  wget -O OBTApp.install https://github.com/daniel-striim/striim/blob/main/Samples/Oracle%20Bank%20Transaction/OBTApp.install?raw=true
		  chmod 777 OBTApp.install
		  ./OBTApp.install
		  rm OBTApp.install
	      ;;

	    PostgresTrx | PostgresCloudTrx)
	      echo -n "PostgresTrx"
	      ;;

	    GoogleCloud | "GoogleCloud" | GoogleCloud | "GoogleCloud")
	      echo -n "GoogleCloud"
	      ;;

	    *)
      	  	echo "Valid program must be provided. Available programs are:"
	  		echo "OBT: Oracle Bank Transcation"
	      ;;
	  esac
	  echo
    
