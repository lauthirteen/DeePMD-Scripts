#!/bin/bash 

sys_name=$1

rm -rf ${sys_name}
mkdir ${sys_name}

cp -rf init_data ${sys_name}/data.init

mkdir data.iter
mv data.iter ${sys_name}
mkdir workspace
mv workspace ${sys_name}


for i in iter.*
do
  #echo $i
  cd ${sys_name}/data.iter
  mkdir $i
  cd $i
  mkdir 02.fp
  cd ../../../
  cp -rf $i/02.fp/data.* ${sys_name}/data.iter/$i/02.fp
  cp $i/00.train/000/input.json ${sys_name}/workspace
done

mkdir sys_dir
mv sys_dir ${sys_name}
cp *.py  ${sys_name}
cd ${sys_name}
mkdir data
mv data.* data
path=`pwd`
python3 gen_list.py -p $path -o ${path}/sys_dir/list.txt
python3 count.py -i ${path}/sys_dir/list.txt -o ${path}/sys_dir/count.txt
python3 shuffle.py -i ${path}/sys_dir/list.txt -o ${path}/sys_dir/shuffled.txt

line_count=$(wc -l < "${path}/sys_dir/shuffled.txt")
#echo $line_count

p_90=$(( $line_count * 90 / 100 ))
p_10=$(( $line_count - $p_90 ))

#echo $p_90
#echo $p_10

head -n $p_90 ${path}/sys_dir/shuffled.txt > ${path}/sys_dir/train.txt
tail -n $p_10 ${path}/sys_dir/shuffled.txt > ${path}/sys_dir/valid.txt


rm *.py
cd ..
rm ${sys_name}.zip
zip -q -r ${sys_name}.zip ${sys_name}
