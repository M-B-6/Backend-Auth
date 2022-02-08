<?php
      $hostname="localhost";
    	$username="u";
    	$password="p";
    	$dbname="template";
    	$usertable="members";
    	$iptable ="ip_array";
        $hacklogtable="ip_array";
        //
        //
        $discord = "discord";
    	//
        $notes = "notes";

        //Webhook channel
        $prowebhookurl = "x";
        //Alt webhook channel (can be same as above)
        $webhookurl = "x";
        //DISCORD ID FOR PING
        $admin = "0";

        // RETURN ERRORS //
        // NORMAL USER - ALL OTHER ERRORS PING ADMIN
        $error0= "*0*";

        // VALID ID BUT USER NOT IN DB
        $error1 = "*1*";

        // VALID ID BUT USER NOT IN DB
        $error2 = "*2*";

        // ID == 100 FROM SINGLE IP ADDRESSES 
        $error3 = "*3*";

        // ID == 100 FROM MULTIPLE IP ADDRESSES 
        $error4 = "*4*";

        // UNAUTHORIZED USER HAS BEN IDENTIFIED IN CURRENT DB
        $error5 = "*5*";
?>
