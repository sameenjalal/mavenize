for i in `awk -F'[(|)]' '{print $2}' genre_urls.txt` ; do
	echo `echo $i | sed 's/%//g' | sed 's/20/_/g' | sed 's/26/_/g' | sed 's/2C/_/g' | sed 's/___/_/g' | sed 's/_th/20th/g' | sed 's/C3A9/e/g'`
done
