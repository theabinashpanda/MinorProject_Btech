<?php
// Retrieve the form data
$name = $_POST['name'];
$email = $_POST['email'];
$feedback = $_POST['feedback'];

// Connect to the database (replace with your own database details)
$conn = oci_connect("hr", "admin", "localhost/XE");

if (!$conn) {
    $e = oci_error();
    trigger_error(htmlentities($e['message'], ENT_QUOTES), E_USER_ERROR);
}

// Prepare the SQL statement
$sql = "INSERT INTO feedback (name, email, feedback) VALUES (:name, :email, :feedback)";
$stmt = oci_parse($conn, $sql);

// Bind the parameters
oci_bind_by_name($stmt, ':name', $name);
oci_bind_by_name($stmt, ':email', $email);
oci_bind_by_name($stmt, ':feedback', $feedback);

// Execute the SQL statement
if (oci_execute($stmt)) {
    echo "Thank you for your feedback!";  
} else {
    $e = oci_error($stmt);
    echo "Error: " . htmlentities($e['message'], ENT_QUOTES);
}

oci_free_statement($stmt);
oci_close($conn);
?>
