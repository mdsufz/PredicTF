#!/bin/bash


#1 project folder location (e.g. /home/project)
#2 location of the fasta file with the TFs (used to create the similarity matrix)
#3 location where the conda environment was generated (e.g /home/user)
#4 location of PredicTF (e.g. /home/user/PredicTF)

conda activate $3/deeparg_env

mkdir $1/database
mkdir $1/database/v2
mkdir $1/model
mkdir $1/model/v2
mkdir $1/v2


#Copy Database file
cp $2 $1/database/features.fasta

#Calculate gene lengths
python $4/scripts/seq_length.py $2 > $1/database/features.gene.length

echo "Gene lengths calculated"

#Index database
$4/deeparg-largerepo/bin/diamond makedb --in $1/database/features.fasta --db $1/database/features

echo "Database indexed"

# Building similarity matrix
python $4/deeparg-largerepo/train/generate_train_genes.py $1/database/features.fasta $1/database/train_genes.fasta train

$4/deeparg-largerepo/bin/diamond blastp --db $1/database/features --query $1/database/train_genes.fasta --id 30 --evalue 1e-10 --sensitive -k 10000 -a $1/database/train_genes

$4/deeparg-largerepo/bin/diamond view -a $1/database/train_genes.daa -o $1/database/train_genes.tsv

echo "Similarity matrix building concluded"
#Make copies of files to several folders

mv $1/database/* $1/database/v2
cp $1/database/* $1/v2
#cp $1/database/* $1 

#Train model

echo "Starting model training"
cd $1
python $4/deeparg-largerepo/argdb/train_arc_genes.py . ./v2

echo "Model trained"
