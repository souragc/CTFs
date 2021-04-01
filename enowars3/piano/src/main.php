<?php
require_once 'checklogin.php';
if (!check_login()) {
    header('Location: login.html');
    exit;
}

$token = $_SESSION["token"];
$dir = "../data/{$token}";
$skip = array('.','..');

$dp = opendir($dir);
$files = [];
if ($dp) {
    while ($file = readdir($dp)) {
        if (in_array($file, $skip)) continue;
        $files[] = $file;
    }
}
?>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hackiano</title>
    <link rel="stylesheet" type="text/css" href="piano.css" />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
</head>
<body>
<div id="content">
    <div id="logout">
        <form align="right" name="logout" method="post" action="logout.php">
            <label class="logoutLblPos">
                <input name="submit2" type="submit" id="submit2" value="Log out">
            </label>
        </form>
    </div>
    <div id="content-inner">
        <div id="piano">
            <h1>Hackiano</h1>
        </div>
    </div>
    <div id="upload">
    <form action="upload.php" method="post" enctype="multipart/form-data">
        <p><input id="file" name="file" type="file"></p>
        <p><input type="submit" value="Upload File" name="submit"></p>
    </form>
    </div>
    <div id="files">
        <table>
            <tr>
                <th>
                    Filename
                </th>
            </tr>
            <?php foreach ($files as $file) { ?>
            <tr>
                <td><?= "<a href='/download.php?file=$file'>$file</a>" ?></td>
            </tr>
            <?php } ?>
        </table>
    </div>
</div>
<script src="audio.js"></script>
<script src="piano.js"></script>
</body>
</html>