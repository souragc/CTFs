build.sh: Downloads files and builds Docker image. This takes a while, use this time to read the sources!
run-env/run-debug.sh: Develop your exploit localy by running ./run-debug.sh exploit.sh, use "vncviewer 127.0.0.1" to observe graphical env.
run-env/run.sh: Your exploit will be executed on production using this script (the directory with your exploit will be passed as the first arg). It will be killed after a few minutes.
