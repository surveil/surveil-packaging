#!/bin/bash

set -e

# Usage function
usage() {
    echo "Usage: $0 -n <package_name> -r <package_repo> [-L <remote_login> -I <remote_host_ip> -F <remote_folder>] -j <joulupukki_url> -k <joulupukki_user> [-b <joulupukki_build_id>] " 1>&2; exit 1; 
}

# Check commands
RPM=`which rpm`
CREATEREPO=`which createrepo`
JSON_PP=`which json_pp`
CURL=`which curl`
RSYNC=`which rsync`

#if [ -z "${RPM}" ]
#then
#    echo "rpm command is missing, please install it"
#fi
if [ -z "${CREATEREPO}" ]
then
    echo "createrepo command is missing, please install it"
fi
if [ -z "${JSON_PP}" ]
then
    echo "json_pp command is missing, please install it"
fi
if [ -z "${CURL}" ]
then
    echo "curl command is missing, please install it"
fi
if [ -z "${RSYNC}" ]
then
    echo "rsync command is missing, please install it"
fi

# Defaults
JLPK_BUILDID=latest

# Get opt
while getopts "L:I:F:r:n:j:k:b:" o; do
    case "${o}" in
        L)
            REMOTE_USER=${OPTARG}
            ;;
        I)
            REMOTE_IP=${OPTARG}
            ;;
        F)
            REMOTE_FOLDER=${OPTARG}
           ;;
        r)
            PACKAGE_REPO=${OPTARG}
           ;;
        n)
            PACKAGE_NAME=${OPTARG}
           ;;
        j)
            JLPK_URL=${OPTARG}
           ;;
        k)
            JLPK_USER=${OPTARG}
           ;;
        b)
            JLPK_BUILDID=${OPTARG}
           ;;
        
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${PACKAGE_REPO}" ] || [ -z "${PACKAGE_NAME}" ] || [ -z "${JLPK_URL}" ] || [ -z "${JLPK_USER}" ]; then
    echo "Missing argument"
    usage
fi



declare -A PACKAGE_REPOS
PACKAGE_REPOS=( ["surveil-packaging"]="https://github.com/surveil/surveil-packaging" ["monitoring-tools"]="https://github.com/savoirfairelinux/monitoring-tools" )
declare -A PACKAGE_NAMES
PACKAGE_NAMES=( ["surveil-packaging"]="surveil-packaging" ["monitoring-tools"]="monitoring-tools" )

START_DATE=`date +%s`
YUM_DISTROS="centos_7"

CURRENT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
LOCAL_FOLDER=${CURRENT_DIR}/tmp_repos
LOCAL_DDL_FOLDER=${LOCAL_FOLDER}/repos/
LOCAL_REPO_FOLDER=${LOCAL_DDL_FOLDER}/surveil/
#KEYID=
#GPGPASSWORD=""
# Time to wait builds (7200s = 2h)
TIMEOUT=7200
WAITING_STEP=300

 

# Overrides for tests
#TIMEOUT=10
#WAITING_STEP=1

TIME_OUT_DATE=$(( ${START_DATE} + ${TIMEOUT} ))



function sign_rpm
{
cat << End-of-text
spawn rpm --resign $1
expect -exact "Enter pass phrase: "
send -- "${GPGPASSWORD}\r"
expect eof
exit
End-of-text
}


function sign_deb
{
cat << End-of-text
spawn dpkg-sig -k ${KEYID} --sign builder $1
expect -exact "Enter passphrase: "
send -- "${GPGPASSWORD}\r"
expect eof
exit
End-of-text
}


# RPM macros
if [ ! -f ~/.rpmmacros ];
then
    echo "%_signature gpg" > ~/.rpmmacros
    echo "%_gpg_name ${KEYID}" >> ~/.rpmmacros
fi




function build
{
    PACKAGE=$1
    echo
    echo
    echo "============================================================="
    echo "============================================================="
    echo "                       $PACKAGE"
    echo "============================================================="
    echo "============================================================="
    PACKAGE_NAME=${PACKAGE_NAMES["$PACKAGE"]}
    PACKAGE_REPO=${PACKAGE_REPOS["$PACKAGE"]}
    LOCAL_TMP_FOLDER=${LOCAL_FOLDER}/tmp/packages_folder_nightly_${PACKAGE_NAME}/
    rm -rf ${LOCAL_TMP_FOLDER}
    mkdir -p ${LOCAL_TMP_FOLDER}
    # Launch build
    # build_id=$(${CURL} -s -X POST -H "Content-Type: application/json" -i  -d "{ \"source_url\": \"${PACKAGE_REPO}\", \"source_type\": \"git\", \"branch\": \"packaging\", \"snapshot\": true}" ${JLPK_URL}/v3/users/${JLPK_USER}/${PACKAGE_NAME}/build | grep result  | json_pp  | grep "build" | awk '{ print $NF }')

    build_id=latest
    # Wait builds
    WAITING=1
    while [ $(date +%s) -lt ${TIME_OUT_DATE} ] && [ ${WAITING} == 1 ]
    do
        # Check status
        status=$(${CURL} ${JLPK_URL}/v3/users/${JLPK_USER}/${PACKAGE_NAME}/builds/${build_id} 2> /dev/null| ${JSON_PP}| python -c 'import json,sys;obj=json.load(sys.stdin);print obj["status"]')
        if [ "${status}" == "failed" ] || [ "${status}" == "succeeded" ]
        then
            WAITING=0
        else
            echo "WAITING"
            sleep ${WAITING_STEP}
        fi
    done
    
    if [ "${status}" == "succeeded" ]
    then
        echo Packages built
    else
        echo Packages NOT built
    fi

    
    # Download builds
    rm -rf ${LOCAL_TMP_FOLDER}
    mkdir -p ${LOCAL_TMP_FOLDER}/downloads
    mkdir -p ${LOCAL_TMP_FOLDER}/packages
    wget ${JLPK_URL}/v3/users/${JLPK_USER}/${PACKAGE_NAME}/builds/${build_id}/download/archive -O ${LOCAL_TMP_FOLDER}/downloads/${PACKAGE_NAME}.tar.gz
    tar -xf ${LOCAL_TMP_FOLDER}/downloads/${PACKAGE_NAME}.tar.gz -C /${LOCAL_TMP_FOLDER}/packages
    
    echo
    echo
    echo
    echo "============================================================="
    echo "==                           RPMS                          =="
    echo "============================================================="
    # RPM
    for DISTRO in ${YUM_DISTROS}
    do
    
        echo
        echo
        echo "=================="
        echo "   $DISTRO"
        echo "=================="
        echo   
    
        DISTRO_FOLDER="${LOCAL_REPO_FOLDER}/${DISTRO}"
     
        # Create distro folder
        if [ ! -d "${DISTRO_FOLDER}" ]
        then
            mkdir -p ${DISTRO_FOLDER}
            ${CREATEREPO} ${DISTRO_FOLDER}
        fi
    
        rmdir ${LOCAL_TMP_FOLDER}/packages/${DISTRO}/ || true
        if [ -d ${LOCAL_TMP_FOLDER}/packages/${DISTRO} ]
        then
            # delete src.rpm files
            rm -f ${LOCAL_TMP_FOLDER}/packages/${DISTRO}/*.src.rpm
            # Add rpm files
            for file in ${LOCAL_TMP_FOLDER}/packages/${DISTRO}/*.rpm
            do
        
                echo
                echo $(basename ${file})
                echo "==========================================================================================="
                echo
                # RPM sign
                echo "Signing package"
                #sign_rpm ${file} | /usr/bin/expect -f -
        
                cp ${file} ${DISTRO_FOLDER}
            done
        fi

    # Download extra packages
    wget -O ${DISTRO_FOLDER}/influxdb-0.9.2-1.x86_64.rpm https://s3.amazonaws.com/influxdb/influxdb-0.9.2-1.x86_64.rpm
    wget -O ${DISTRO_FOLDER}/grafana-2.1.2-1.x86_64.rpm https://grafanarel.s3.amazonaws.com/builds/grafana-2.1.2-1.x86_64.rpm
    wget -O ${DISTRO_FOLDER}/python-pika-0.9.5-7.fc21.noarch.rpm http://dl.fedoraproject.org/pub/fedora/linux/releases/22/Everything/i386/os/Packages/p/python-pika-0.9.5-7.fc21.noarch.rpm

    # Update repo
    ${CREATEREPO} --update ${DISTRO_FOLDER}
    
    done
} 



if [ "$1" != "" ]
then
    PACKAGE_NAME=${PACKAGE_NAMES["$1"]}
    if [ "$PACKAGE_NAME" != "" ]
    then
        build $1
    fi
else
    for package in  "${!PACKAGE_NAMES[@]}"
    do
        pushd $PWD
	build $package
	popd
    done
fi


echo
echo
echo
echo "============================================================="
echo "==                Transfert to remote server               =="
echo "============================================================="
echo
echo


if [ "${REMOTE_USER}" ] && [ "${REMOTE_IP}" ] && [ "${REMOTE_FOLDER}" ]
then
    echo Send repository on remote host
    rsync -arv --delete --exclude="surveil.pub.key" ${LOCAL_DDL_FOLDER}/surveil/* ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_FOLDER}
else
    echo Repository NOT sent on remote host
fi
