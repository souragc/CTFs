<?php
if (isset($_POST['token']) && $_POST['token'] != '') {
    $token = $_POST['token'];
    $filepath = "../data/{$token}";
    if (file_exists($filepath)) {
        session_start();
        $_SESSION['token'] = $token;
        header('Location: main.php');
        exit;
    } else {
        $error = "<p> You need to register first! </p>";
    }
} else {
    $error = "<p> Please input a token! </p>";
}
?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login Error</title>
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
                        <h5 class="card-title">Login Error!</h5>
                        <p class="card-text">
                            <?= $error ?>
                        </p>
                        <div class="text-center">
                            <a href="login.html" class="btn btn-primary">Login</a>
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
