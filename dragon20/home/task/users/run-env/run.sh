tmp_dir=$1
mkdir $tmp_dir/admin
cp -rf `pwd`/../task-env/* $tmp_dir/admin/
docker run --rm --cpus="1" -m "512m" -it -d  -v $tmp_dir/exploit.sh:/exploit.sh -v $tmp_dir/admin/:/home/admin/data/ --name $2 ds-desktop-enviroment
