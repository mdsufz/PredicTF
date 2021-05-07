#!/bin/bash

#1 location of PredicTF (e.g. /home/user/PredicTf)
#2 location of the target genome for predicting TFs
#3 folder to store results (e.g. /home/project/results)


conda activate $1/deeparg_env

mkdir $3

python $1/deeparg-largerepo/deepARG.py --align --type prot --genes --input $2 --out $3/file.out --folder $1/BacTFDB/ 
