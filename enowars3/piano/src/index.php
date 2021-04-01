<?php
require_once 'checklogin.php';
if (check_login()) {
    include 'main.php';
} else {
    include 'login.html';
}