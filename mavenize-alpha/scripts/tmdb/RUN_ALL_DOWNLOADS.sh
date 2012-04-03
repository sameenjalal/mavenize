FILE="ALL_BASH.txt"

while read line; do 
	#echo "wget $line"
	wget $line
	#bash `$line`
done < $FILE
