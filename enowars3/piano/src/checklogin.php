<?php
function check_login () {
    session_start();
    if (isset($_SESSION['token']) && $_SESSION['token'] != '') {
        return true;
    } else {
        return false;
    }
}