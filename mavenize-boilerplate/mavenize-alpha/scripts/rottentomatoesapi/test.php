<?php
$apikey = 'mz7z7f9zm79tc3hcaw3xb85w';
$all_searches = array( 'star','harry','potter','wars','twilight','titanic','list','hotel','love','heart','lawyer','lord','ring','matrix' );
foreach( $all_searches as $query )
{
	for( $i = 0 ; $i < 26 ; $i++ )
	{
		$q = urlencode( $query );
		$endpoint = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=$apikey&q=$q&page=$i";

		$session = curl_init($endpoint);
		curl_setopt($session, CURLOPT_RETURNTRANSFER, true);
		$data = curl_exec($session);
		curl_close($session);

		$fp = fopen( "$query$i", "w" );
		fwrite( $fp, $data );
		fclose( $fp );
	}
}
?>
