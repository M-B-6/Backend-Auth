<!DOCTYPE html>
<html>
    <body style="color:#000000; background-color:#FFFFFF;">

    <?php
        require($_SERVER['DOCUMENT_ROOT']."/Template/config.php");
       	$key = $_POST['key'];
        $hwid = $_POST['hwid'];
        $version = $_POST['version'];
        $ip = $_SERVER['REMOTE_ADDR'];
        $date = date_create();
   
    	$con = mysqli_connect($hostname,$username,$password,$dbname);
    	
        /*if(mysqli_connect_errno()){
            echo "Failed to connect<br>" . mysqli_connect_errno();
        }*/
        if(mysqli_ping($con)){
            $ip_post = "INSERT INTO $iptable (ip , user) VALUES ('$ip' , '$key')";
            mysqli_query($con, $ip_post);

        	// check ip array for ip     	
        	$ip_check = ("SELECT COUNT(*) FROM $iptable WHERE (ip) = '$ip'");
        	$ip_resultq = mysqli_query($con, $ip_check);
            $ip_result = mysqli_fetch_array($ip_resultq);
            
            // check ip array for id 
        	$id_check = ("SELECT COUNT(*) FROM $iptable WHERE (user) = '$key'");
        	$id_resultq = mysqli_query($con, $id_check);
            $id_result = mysqli_fetch_array($id_resultq);
            
            if ($ip_result[0] > 0) {
                $ip_check_count = ("SELECT COUNT(*) FROM $iptable WHERE (user) = '$key'");
        	    $ip_result_countq = mysqli_query($con, $ip_check_count);
        	    $ip_result_count = mysqli_fetch_array($ip_result_countq);
            } 
            else {
                $ip_result_count[0] = 1;
            }

        	$sql = "SELECT * FROM $usertable WHERE (id) = '$key'" ;
        	$result = mysqli_query($con, $sql) or die("<p>*no key*</p>");
        	
        	/*if (!mysqli_query($con, $sql)) {
              echo("Error description: " . mysqli_error($con));
            }*/
        	
        	// check members for id 
        	$member_check = ("SELECT COUNT(*) FROM $usertable WHERE (id) = '$key'");
        	$member_checkq = mysqli_query($con, $member_check);
            $member_result= mysqli_fetch_array($member_checkq);
        	
        	if($result){
        	    $ch = curl_init( $prowebhookurl );
        	    while ($row = mysqli_fetch_assoc($result)) {
                    $id = $row['id'];
                    $name = $row['discord'];
                    $recordedhwid = $row['hwid'];
                }
                
                //Make sure hwid matches, if hwid is null then lock it to the running hwid
                $check_hwid = "SELECT hwid FROM $usertable WHERE $usertable.`id` = $key";
                $get_time_played = "SELECT totaltime FROM $usertable WHERE $usertable.`id` = $key";
                $grab_hwid = mysqli_query($con, $check_hwid);
                $current_hwid = mysqli_fetch_array($grab_hwid);
                
                //if current hwid is null, add the first running hwid
                if (is_null($current_hwid[0])) {
                    $hwid_post = "UPDATE $usertable SET `hwid` = '".$hwid."' WHERE $usertable.`id` = $key";
                    mysqli_query($con, $hwid_post);
                } else {
                    if($current_hwid[0] != $hwid) {
                        $member_result = 0;
                    }
                }
                
                //set default timezone
                date_default_timezone_set('America/Vancouver');
                
                //Create a current date object
                $now = new DateTime();
                //Check the subscription end date and compare to current date
                $check_date = "SELECT subscription FROM $usertable WHERE $usertable.`id` = $key";
                $grab_date = mysqli_query($con, $check_date);
                $current_date = mysqli_fetch_array($grab_date);
                $subscription = new DateTime($current_date[0]);
                
                //Grab recent time before we update it for this run
                $check_recent = "SELECT recent FROM $usertable WHERE $usertable.`id` = $key";
                $grab_recent = mysqli_query($con, $check_recent);
                $current_recent = mysqli_fetch_array($grab_recent);
                $recent_time = new DateTime($current_recent[0]);
                
                
                //update the running version
                $version_post = "UPDATE $usertable SET `version` = $version WHERE $usertable.`id` = $key";
                mysqli_query($con, $version_post);
                //update the latest time run
                $timestamp = date('Y-m-d H:i:s');
                $time_date_post = "UPDATE $usertable SET `recent` = now() WHERE $usertable.`id` = $key";
                mysqli_query($con, $time_date_post);
                
                $subresult = $subscription->format('Y-m-d');
                
                if ($hwid == null && $version == null) {
                    //bot
                    echo $error1;//Status: NO ID
                         $formcontent= "**Direct Link Visit**\nIP: **".$ip."\n**```>>>```\n";
                } else {
                    if ($member_result[0] < 1){
                        // 1 and !e100 and not member
                        echo $error1;//Status: NO ID
                        $formcontent= "<@{$admin}>\n**INVALID** - ID: **" .$key. "** \nIP: **".$ip."** \nRUNNING HWID: **".$hwid."** \nRECORDED HWID: **".$current_hwid[0]."** \nSCRIPT: **".$dbname."** \nTOTAL IP: **". $ip_result_count[0] . "** \nVERSION: **".$version."**\n```>>>```\n";
                        
                        //echo $reportBack;//Status: NORMAL
                    } else {
                        // normal member
                        if ($now < $subscription) {
                            
                            //Split IP and HWID string to not display them fully in form content
                            $ip = explode(".",$ip);
                            $hwid = explode("-",$hwid);
                            
                            
                            $now = $now->format('Y-m-d H:i:s');
                            $recent_time = $recent_time->format('Y-m-d H:i:s');
                            $now = new DateTime($now);
                            $recent_time = new DateTime($recent_time);
                            
                            $timeDiff = $recent_time->diff($now);
                            $timeDiff = $timeDiff->s;
                            
                            if($timeDiff == 0) {
                                //add 5 more minutes to the total time played
                                $time_played_post = "UPDATE $usertable SET `totaltime` = `totaltime`+5 WHERE $usertable.`id` = $key";
                                mysqli_query($con, $time_played_post);
                            } else {
                                $formcontent = "\nMEMBER: **" .$name. "** - ID: **xxxxx** \nIP: **xxx.xxx.".$ip[2].".".$ip[3]."** \nHWID: **xxxxxxxx-xxxx-xxxx-".$hwid[3]."-".$hwid[4]."** \nSCRIPT: **".$dbname."** \nTOTAL IP: **". $ip_result_count[0] ."**\nVERSION: **".$version."**\n```>>>```\n";
                            }
                            echo $error0;//Status: NORMAL
                            $reportBack = "<p>User: " .$name. "</p> Valid until: " .$subresult;
                            echo $reportBack;//Status: NORMAL
                        } else {
                            #set hwid to null
                            $hwid_null_post = "UPDATE $usertable SET `hwid` = NULL WHERE $usertable.`id` = $key";
                            $version_null_post = "UPDATE $usertable SET `version` = NULL WHERE $usertable.`id` = $key";
                            mysqli_query($con, $version_null_post);
                            mysqli_query($con, $hwid_null_post);
                            echo $error2;//Status: subscription expired
                            $formcontent = "<@{$admin}>\n__**EXPIRED**__\nMEMBER: **" .$name. "** - ID: **" .$key. "** \nIP: **".$ip."** \nHWID: **".$hwid."** \nSCRIPT: **".$dbname."** \nTOTAL IP: **". $ip_result_count[0] ."**\nVERSION: **".$version."**\n```>>>```\n";
                        }
                    }
                }

                // new function end 

            } else {
        	    $ch = curl_init( $webhookurl );
        	    echo "*FAIL*";//Status: NO CONNECTION
        		$formcontent= $date->format('Y/m/d H:i:s') . "** IP:** ".$ip."\n";	
        	}
        	
    		$json_data = json_encode([
    			"content" => "$formcontent"
    		 
    		], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );

    		curl_setopt( $ch, CURLOPT_HTTPHEADER, array('Content-type: application/json'));
    		curl_setopt( $ch, CURLOPT_POST, 1);
    		curl_setopt( $ch, CURLOPT_POSTFIELDS, $json_data);
    		curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, 1);
    		curl_setopt( $ch, CURLOPT_HEADER, 0);
    		curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1);
    		$response = curl_exec( $ch );
            //echo "<br><b>Webhook Complete<br>";
            //echo $response;
            curl_close( $ch );
        }
        else{
            //echo "Error: " . mysqli_error($con);
        }
        mysqli_close($con);

    ?>
    </body>
</html>
