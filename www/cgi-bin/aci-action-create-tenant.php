<html>
<body  background="">
<center>
<IMG SRC="" ALT="" >

<p>
<p>
<TABLE align="center" bgcolor="#FFFFFF" border="3"  BORDERCOLOR="#FF3300">
<TR><TD align="center" style="font-size: 24px"><font color="#FFB310">Please enter the information to attach a device to an EPG.</font>
</table>
<p>

<?php
// define variables and set to empty values
$var1 = "";
$err = "";

if ($_SERVER["REQUEST_METHOD"] == "POST")
{
	if(empty($_POST["var1"]))
		{$Err = "ERROR: A name is required";}
	else
		$var1 = test_input($_POST["var1"]);
	

	if ($Err == "") {
		if (($_POST["var1"]) != "") {
			echo 'Thank you for your input.';
			header("Location: aci-create-tenant.py");
			}
		}
}

function test_input($data)
{
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}
?>

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
<TABLE bgcolor="#FFFFFF" border="2" BORDERCOLOR="#990033">
<TR><TH>Enter a name
<TD><font color="#990033">

<?php
	if ($Err != "")
                echo $Err;
?>
</font>


<TR><TD>Tenant Name:
<TD><input type="text" name="var1" size="20" value="<?php echo htmlspecialchars($_POST['var1']); ?>">
</table>

<input type="submit" value="Submit" />
</form>
<p><button onclick="goBack()">Go Back</button><script>function goBack() { window.history.back(); } </script>

