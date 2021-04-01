<?php
$registered = false;
while (!$registered) {
    $token = bin2hex(random_bytes(30));
    if (!file_exists("../data/{$token}")) {
        mkdir("../data/{$token}");
        $registered = true;
    }
}
?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register</title>
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
                        <h5 class="card-title">Registered!</h5>
                        <p class="card-text">Your token:</p>
                        <div class="alert alert-success" role="alert" id="token">
                            <?= $token ?>
                        </div>
                        <div class="alert alert-warning" role="alert">
                            IMPORTANT: Don't loose your token!
                        </div>
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