<?php

$uname1 = $_POST['name'];
$email  = $_POST['email'];
$upswd1 = $_POST['phone'];
$upswd2 = $_POST['password'];
$upswd2 = $_POST['confirm_password'];



if (!empty($name) || !empty($email) || !empty($phone) || !empty($password) || !empty(confirm_password))
{

$host = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "tech_turtles";



// Create connection
$conn = new mysqli ($host, $dbusername, $dbpassword, $dbname);

if (mysqli_connect_error()){
  die('Connect Error ('. mysqli_connect_errno() .') '
    . mysqli_connect_error());
}
else{
  $SELECT = "SELECT email From register Where email = ? Limit 1";
  $INSERT = "INSERT Into register ( name1 , email ,phone, password1,confirm_password )values(?,?,?,?)";

//Prepare statement
     $stmt = $conn->prepare($SELECT);
     $stmt->bind_param("s", $email);
     $stmt->execute();
     $stmt->bind_result($email);
     $stmt->store_result();
     $rnum = $stmt->num_rows;

     //checking username
      if ($rnum==0) {
      $stmt->close();
      $stmt = $conn->prepare($INSERT);
      $stmt->bind_param("ssss", $name1,$email,$phone,$password1,$confirm_password);
      $stmt->execute();
      echo "New record inserted sucessfully";
     } else {
      echo "Someone already register using this email";
     }
     $stmt->close();    
     $conn->close();
    }
} else {
 echo "All field are required";
 die();
}
?>