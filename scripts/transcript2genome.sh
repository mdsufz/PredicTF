#!/bin/bash


#2 location of the results folder (e.g. /home/project/results)
# location of the fasta file with the TFs (used to create the similarity matrix)
#3 location where the conda environment was generated (e.g /home/user)


#1 location of PredicTF (e.g. /home/user/PredicTF)

#Processing the output of Predicting TFs:

python $1/process_output_predictf.py $2/file.out.align.daa.tsv $2/file.out.mapping.ARG <sequences_input.fa> <predicted_TFs.fa> <predicted_TFs_intervals.tsv>

#Obtain the mapped regions of each genome or metagenome in their respective transcriptomes or metatranscriptomes:

python get_mapped_regions.py <mapping.sam> <output_directory>

#Check if the predicted TFs are covered by the transcriptome or metatranscriptome:

python check_mapped_TFs.py <predicted_TFs.fa>  <output_directory/mapped_regions.tsv>



