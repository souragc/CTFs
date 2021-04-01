tmp_dir=$(mktemp -d -t ds-XXXXXXXXXX)
echo $tmp_dir
mkdir $tmp_dir/admin
cp -rf `pwd`/../task-env/* $tmp_dir/admin/
cp $1 $tmp_dir/exploit.sh
docker run --rm --cpus="1" -m "512m" -it -v $tmp_dir/exploit.sh:/exploit.sh -v $tmp_dir/admin/:/home/admin/data/ -p 5900:5900 -e START_VNC=1 ds-desktop-enviroment
rm -rf $tmp_dir
