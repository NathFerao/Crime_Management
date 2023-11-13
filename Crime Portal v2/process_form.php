<?php
$first_name = $_POST['first_name'];
$last_name = $_POST['last_name'];
$location = $_POST['location'];
$password = $_POST['password'];

$conn = new mysqli('localhost','root','','police');
if ($conn->connect_error) {
    die('Connection Failed'. $conn->connect_error);
}else{
    echo "success";
   // $stmt = $conn->prepare("insert into police(Fname, Lname, location, password) values(?,?,?,?)");
   // $stmt->bind_param("ssss",$first_name, $last_name, $location, $password);
   // $stmt->execute();
   // echo "registration success...";
   // $stmt->close();
   // $conn->close();
}
?>
