#!/bin/bash 

################
iter_num=30

################

echo "Iter   Accurate" > accurate_dpgen_iter_info.txt
echo "Total dpgen iter info:" > total_dpgen_iter_info.txt
echo "Partial dpgen iter info:" > partial_dpgen_iter_info.txt
echo "Iter   Accurate for system" > Accurate_iter_info.txt
for i in $(seq 0 $iter_num)
do
  s=`printf "iter.%06d" $i`
  printf "\------------------------- %s task --------------------------\n" $s >> total_dpgen_iter_info.txt
  printf "\------------------------- %s task --------------------------\n" $s >> partial_dpgen_iter_info.txt
  wc -l ${s}/02.fp/candidate* > 111.txt
  n1=$(  tail -n 1 111.txt | awk '{ print $1}'  )

  wc -l ${s}/02.fp/rest_accurate* > 222.txt
  n2=$(  tail -n 1 222.txt | awk '{ print $1}'  )

  wc -l ${s}/02.fp/rest_failed*   > 333.txt
  n3=$(  tail -n 1 333.txt | awk '{ print $1}'  )

  n=$[ $n1 + $n2 + $n3 ]

  nn1=$( awk 'BEGIN{printf "%0.6f",'$n1/$n*100'}' )
  nn2=$( awk 'BEGIN{printf "%0.6f",'$n2/$n*100'}' )
  nn3=$( awk 'BEGIN{printf "%0.6f",'$n3/$n*100'}' )
  printf "Total candidate :%6d in %6d %7.2f %%\n" $n1 $n $nn1 >> total_dpgen_iter_info.txt
  printf "Total failed    :%6d in %6d %7.2f %%\n" $n3 $n $nn3 >> total_dpgen_iter_info.txt
  printf "Total accurate  :%6d in %6d %7.2f %%\n" $n2 $n $nn2 >> total_dpgen_iter_info.txt
  printf "%6d %7.2f \n" $i $nn2 >> accurate_dpgen_iter_info.txt

  line_num=-1
  while read line
  do
    let line_num=$line_num+1
  done < 111.txt
  
  printf "%6d" $i >> Accurate_iter_info.txt
  for j in $(seq 1 $line_num)
  do
    let iter=$j-1
    #echo $j
    n1=$(  sed -n "${j}p" 111.txt | awk '{ print $1}'  )
    n2=$(  sed -n "${j}p" 222.txt | awk '{ print $1}'  )
    n3=$(  sed -n "${j}p" 333.txt | awk '{ print $1}'  )
    let n=$n1+$n2+$n3
    #echo $n
    nn1=$( awk 'BEGIN{printf "%0.6f",'$n1/$n*100'}' )
    nn2=$( awk 'BEGIN{printf "%0.6f",'$n2/$n*100'}' )
    nn3=$( awk 'BEGIN{printf "%0.6f",'$n3/$n*100'}' )
    printf "%03d candidate :%6d in %6d %7.2f %%\n" $iter $n1 $n $nn1 >> partial_dpgen_iter_info.txt
    printf "%03d failed    :%6d in %6d %7.2f %%\n" $iter $n3 $n $nn3 >> partial_dpgen_iter_info.txt
    printf "%03d accurate  :%6d in %6d %7.2f %%\n" $iter $n2 $n $nn2 >> partial_dpgen_iter_info.txt
    printf "%7.2f" $nn2 >> Accurate_iter_info.txt
    printf "\n" >> partial_dpgen_iter_info.txt
  done
  printf "\n" >> Accurate_iter_info.txt
  rm 111.txt 222.txt 333.txt
done
