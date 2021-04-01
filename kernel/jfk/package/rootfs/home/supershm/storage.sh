#!/bin/sh

if test $# -lt 1
then
    echo "Usage: ./store.sh c <key> || r <key> || u <key> <data>"
    echo "c      create region with associated <key>"
    echo "r      read data from region associated with <key>"
    echo "s      store data to region associated with <key>"
    echo "E.g:   ./store.sh c mykey"
    echo "       ./store.sh u mykey \"Hello World!\""
    echo "       ./store.sh r mykey"
    exit
fi

if test $# -eq 2
then
    if expr match $1 "c"
    then
        echo -ne "c$2" > /dev/supershm
        echo "Creating storage"
        exit
    fi

    if expr match $1 "r"
    then
        echo -ne "s$2" > /dev/supershm
        echo "Reading"
        head -c 1024 /dev/supershm
        exit
    fi

    echo
    exit
fi

if test $# -eq 3
then
    if expr match $1 "u"
    then
        echo -ne "u$2" > /dev/supershm
        echo "Updating"
        echo -ne $3 > /dev/supershm
        exit
    fi
    exit
fi
