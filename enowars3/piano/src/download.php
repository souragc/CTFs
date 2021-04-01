<?php
require_once 'checklogin.php';
if (!check_login()) {
    header('Location: login.html');
    exit;
}
if (isset($_GET['file'])) {
    $token = $_SESSION["token"];
    $filename = basename($_GET['file']);
    $target_dir = "../data/{$token}/";
    $target_file = $target_dir . $filename;

    if (file_exists($target_file)) {
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . basename($target_file) . '"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($target_file));
        readfile($target_file);
        exit;
    }
} else {
    echo "Nothing to download";
}