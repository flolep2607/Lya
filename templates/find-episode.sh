#!/bin/bash
query=$1
#echo "query: $query" TVSHOW=$(echo "$query" | awk -F ' ' '{print $1}')
NUM=$(echo "$query" | awk -F ' ' '{print $NF}') TVSHOW=${query::-${#NUM}}
#echo "NUM: $NUM"
EPISODE=$(echo "$NUM" | sed 's/.*\(..\)/\1/') SEASON=$(echo "$NUM" | sed 's/\(.\{1,2\}\)../\1/') if [ "$SEASON" -lt 10 ];then
    echo "IN"
    SEASON="0$SEASON" fi PATH="/var/media/krokodin/Serie/" echo "Episode: $EPISODE -- Season: $SEASON -- TVShow: $TVSHOW" urlencode() {
    # urlencode <string>
    local length="${#1}"
    for (( i = 0; i < length; i++ )); do
        local c="${1:i:1}"
        case $c in
            [a-zA-Z0-9.~_-]) printf "$c" ;;
            *) printf '%%%02X' "'$c"
        esac
    done
}
RETURN=$(/usr/bin/ssh -T root@192.168.1.25 'find '"$PATH"' -iname "*'"$TVSHOW"'*" -type f | grep -i "S'"$SEASON"'" | grep "E[P]*'"$EPISODE"'" | grep -v ".srt"') echo "return: $RETURN"
# REMOVE the /var
FILEPATH=${RETURN:4} result_string="$FILEPATH" result_string=$(urlencode "$result_string")
#echo "result: $result_string"
if [ ! -z "$RETURN" ]; then
  C=$(/usr/bin/curl -g 'http://kodi/jsonrpc?request={"jsonrpc":"2.0","id":"1","method":"Player.Open","params":{"item":{"file":"'"$result_string"'"}}}') 
else
  echo "IN ELSE"
  RETURN=$(/usr/bin/ssh -T root@192.168.1.25 'find '"$PATH"' -iname "*'"$TVSHOW"'*" -type f | grep -i '$NUM' | grep -v ".srt"')
  echo "return: $RETURN"
  # REMOVE the /var
  FILEPATH=${RETURN:4}
  result_string="$FILEPATH"
  result_string=$(urlencode "$result_string")
  if [ ! -z "$RETURN" ]; then
    C=$(/usr/bin/curl -g 'http://kodi/jsonrpc?request={"jsonrpc":"2.0","id":"1","method":"Player.Open","params":{"item":{"file":"'"$result_string"'"}}}')
  fi
fi
