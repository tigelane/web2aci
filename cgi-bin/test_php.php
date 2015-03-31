<?php

echo "Content-type: text/html\n";
echo "<p><p>";
echo '<HTML><HEAD><TITLE>PHP Test</TITLE></HEAD>';
echo '<BODY><H2>Hello there from a PHP Script!</H2>';
echo $_SERVER['SERVER_ADDR'];

echo "<H3>The time is currently: ";
echo date('l j \of F Y h:i:s A');
echo "</H3><p>";
echo "You are connecting from: ";
echo $_SERVER['REMOTE_ADDR'];
echo '</BODY></HTML>';

?>
