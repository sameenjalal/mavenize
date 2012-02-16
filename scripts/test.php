<?php
    include ('./OAuthSimple.php');

    $apiKey = 'acga93y7k6vfv4czcer6csrp';
    $sharedSecret = 'HkVMWTQECf';


	$arguments = Array(
        term=>'comedy',
        expand=>'formats,synopsis,cast,directors,seasons,episodes,discs,similars,filmography,awards,person',
        max_results=> 100,
        output=>'json'
	);


    // this is the URL path (note the lack of arguments.)
    $path = "http://api.netflix.com/catalog/titles";
    //$path = "http://api.netflix.com/catalog/titles/index";

    // Create the Signature object.
    $oauth = new OAuthSimple();
    $signed = $oauth->sign(Array(path=>$path,
                    parameters=>$arguments,
                    signatures=> Array('consumer_key'=>$apiKey,
                                        'shared_secret'=>$sharedSecret
                                        /* If you wanted to do queue functions
                                          or other things that require access
                                          tokens and secrets, you'd include them
                                          here as:
                                        'access_token'=>$accessToken,
                                        'access_secret'=>$tokenSecret
                                        */
                                        )));

    // Now go fetch the data.
    $curl = curl_init();
    curl_setopt($curl,CURLOPT_URL,$signed['signed_url']);
    curl_setopt($curl,CURLOPT_RETURNTRANSFER,1);
    curl_setopt($curl,CURLOPT_ENCODING,'gzip,deflate');
    curl_setopt($curl,CURLOPT_SETTIMEOUT,5);
    $buffer = curl_exec($curl);
    if (curl_errno($curl))
    {
        die ("An error occurred:".curl_error());
    }
    $result = json_decode($buffer);
?>
<p>
<b>Your signed URL:</b></br>
<?php print $signed['signed_url'] ?>;
</p>
<p>
And the output is:</br>
<pre>
<?php print_r($result); ?>
</pre>
</p>
