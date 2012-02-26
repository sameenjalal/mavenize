

url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?q=%s&apikey=mz7z7f9zm79tc3hcaw3xb85w&page="

queries = ['star','harry','potter','wars','twilight','titanic','list','hotel','love','heart','lawyer','lord','ring','matrix']

for x in queries:
    for i in range( 1 , 26 ):
        bash_url = url % x
        bash_url += str(i) + " -O searches/" + x + "/" + x + str(i)
        print bash_url
