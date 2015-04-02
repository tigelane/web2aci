<?php

echo "<p><p>";
echo '<HTML><HEAD><TITLE>PHP Test</TITLE></HEAD>';
echo '<BODY>';
echo '<H1>PHP Test File</H1>';
echo '<p>';

echo '<p>';
echo 'The current Date and Time are: ';
echo date('l j \of F Y h:i:s A');
echo '<p>';

echo 'The Server IP Address is: ';
echo $_SERVER['SERVER_ADDR'];
echo'<p>';

echo "You are connecting from: ";
echo $_SERVER['REMOTE_ADDR'];
echo '</BODY></HTML>';

?>
