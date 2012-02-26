FILE="download_all_crew_info.txt"

while read line; do 
	#echo "wget $line"
	wget $line
	#bash `$line`
done < $FILE
