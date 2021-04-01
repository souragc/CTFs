<?php
require_once 'checklogin.php';
if (!check_login()) {
    header('Location: login.html');
    exit;
}
$token = $_SESSION["token"];
$filename = basename($_FILES["file"]["name"]);

if(!file_exists("../data/{$token}")) {
    mkdir("../data/{$token}");
}

$target_dir = "../data/{$token}/";
$target_file = $target_dir . $filename;
$uploadOk = 1;
$fileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
if (isset($_POST["submit"])) {
    //check if file exists
    if (file_exists($target_file)) {
        $out = "File already exists!";
        $uploadOk = 0;
    }

    //check filename length
    if (strlen($target_file) > 100) {
        $out = "Too long file name!";
        $uploadOk = 0;
    }
    //check file size
    if ($_FILES['file']['size'] > 1000000) {
        $out = "File too large!";
        $uploadOk = 0;
    }

    if ($uploadOk != 0) {
        if (move_uploaded_file($_FILES['file']['tmp_name'], $target_file)) {
            $out = "File has been uploaded!";
        } else {
            $out = "File upload failed!";
        }
    }
}
?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload Info</title>
    <link rel="stylesheet" type="text/css" href="main.css"/>
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
</head>
<body>
<div id="content">
    <div class="container h-80">
        <div class="row align-items-center h-100">
            <div class="col-4 mx-auto">
                <div class="card" style="width: 30rem;">
                    <div class="card-body">
                        <h5 class="card-title">Upload Info!</h5>
                        <p class="card-text">
                            <?php
                            if ($uploadOk == 0) {
                                echo "<div class=\"alert alert-danger\" role=\"alert\">
                                    $out
                                    </div>";
                            } else {
                                echo "<div class=\"alert alert-success\" role=\"alert\">
                                    $out
                                    </div>";
                            }
                            ?>
                        </p>
                        <div class="text-center">
                            <a href="main.php" class="btn btn-primary">Back</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
</body>
</html>