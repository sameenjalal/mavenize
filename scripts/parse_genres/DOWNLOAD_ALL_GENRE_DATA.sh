FILE="genre_urls.txt"
node=($(cat $FILE))
NODES=${node[@]}

#for i in $NODES; do
	#echo "\n\n$i\n\n"
	#echo "wget $i -O `awk -F'[(|)]' '{print $2}' genre_urls.txt`"
#done

c=0
for i in $NODES ; do
	l1[$c]=$i
	c=$(($c+1))
done

c=0
for j in `awk -F'[(|)]' '{print $2}' genre_urls.txt` ; do
	echo ${l1[$c]} `echo $j | sed 's/%//g' | sed 's/20/_/g' | sed 's/26/_/g' | sed 's/2C/_/g' | sed 's/___/_/g' | sed 's/_th/20th/g' | sed 's/C3A9/e/g'`
	#wget ${l1[$c]} -O `echo $j | sed 's/%//g' | sed 's/20/_/g' | sed 's/26/_/g' | sed 's/2C/_/g' | sed 's/___/_/g' | sed 's/_th/20th/g' | sed 's/C3A9/e/g'`
	#echo ${l1[$c]} $j
	c=$(($c+1))
done
