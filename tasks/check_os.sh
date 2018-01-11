#!/bin/bash

#
# Configuration system
#
DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PORT=$1
NAMESPACE=$2
TIMEOUT=$3
ID=$4
ROBOT=$5
PASSWORD=$6
FILE_PID="${DIRECTORY}/${ID}.pid"
FILE_JAR="${DIRECTORY}/${ID}.jar"
FILE_TXT="${DIRECTORY}/${ID}.txt"
URL_DETAIL="http://${ROBOT}:${PASSWORD}@localhost:${PORT}/${NAMESPACE}/task/${ID}/detail.txt"
URL_UPDATE="http://${ROBOT}:${PASSWORD}@localhost:${PORT}/${NAMESPACE}/task/${ID}/update.txt"
URL_POST="http://localhost:${PORT}/${NAMESPACE}/task/${ID}/update.txt"
CAN_RUN=1
INFO="Nothing abnormal"

$(cd $DIRECTORY)
WHOAMI=$(whoami)

DETAIL=$(curl -s $URL_DETAIL > $FILE_TXT)
OLDIFS=$IFS
IFS=$'\n'
for d in $(cat $FILE_TXT)
do
    if [[ $d == *"script"* ]]; then
        TASK=$(echo $d | awk -F " " '{print $3}')
    fi
    if [[ $d == *"default"* ]]; then
        if [[ $TASK == "None" ]]; then
            TASK=$(echo $d | awk -F " " '{print $3}')
        fi
    fi
done
cat $FILE_TXT

UPDATE=$(curl -sc $FILE_JAR $URL_UPDATE > ${FILE_TXT})
for d in $(cat $FILE_TXT)
do
    if [[ $d == *"token"* ]]; then
        TOKEN=$(echo $d | awk -F " " '{print $3}')
    fi
done
IFS=$OLDIFS

if [ -f $FILE_PID ]; then
    CONTENT_FILE_PID=$(cat $FILE_PID)
    PIDPROC=$(ps aux | grep "$CONTENT_FILE_PID" | grep -v "grep" | wc -l)
    if [ $PIDPROC -gt 0 ]; then
        UP_TIME=$(ps -u $WHOAMI -o etimes,cmd | grep "$TASK" | awk '{print $1}' | head -n1)
        if [ $UP_TIME -gt $TIMEOUT ]; then
            $(kill -9 $CONTENT_FILE_PID > /dev/null)
            $(rm $FILE_PID)
            INFO="A task was killed"
        else
            CAN_RUN=0
            ERROR="A task is already progress"
        fi
    fi
fi

if [ $CAN_RUN -eq 1 ] ; then
    SCRIPTPROC=$(ps aux | grep "${TASK}.py" | grep -v "grep" | wc -l)
    if [ $SCRIPTPROC -gt 0 ]; then
        ALLPROC=$(ps -ewo pid,etimes,cmd | grep "${TASK}.py" | grep -v "grep")
        while read pid etimes cmd
        do
            if [ "$etimes" -gt $TIMEOUT ]; then
                if [ $STATUS == 1 ]; then
                    $(kill -9 $pid > /dev/null)
                    if [ $SCRIPTPROC -gt 1 ]; then
                        INFO="${SCRIPTPROC} were killed"
                    else
                        INFO="A task was killed"
                    fi
                fi
            else
                CAN_RUN=0
                ERROR="A task is already progress"
            fi
        done <<< "$(echo -e "$ALLPROC")"
    fi
fi

if [ $CAN_RUN -eq 1 ] ; then
    $(curl -sb $FILE_JAR -d "status=ready&info=Nothing abnormal&error=&csrfmiddlewaretoken=${TOKEN}" ${URL_POST})
else
    $(curl -sb $FILE_JAR $URL_READY -d "status=error&info=&error=${ERROR}&csrfmiddlewaretoken=${TOKEN}")
fi
$(rm $FILE_JAR)
$(rm $FILE_TXT)