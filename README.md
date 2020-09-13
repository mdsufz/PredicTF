# PredicTF: a tool to predict bacterial transcription factors in complex microbial communities

# 1) Overview:
Transcription Factors (TFs) are proteins controlling the rate of genetic information, regulating cellular gene expression. A better understanding of TFs in a bacterial community open revenue for exploring gene regulation in ecosystems where bacteria play a key role. Here we describe PredicTF, the first platform supporting the prediction and classification of putative bacterial TF not only in single species but also in complex microbial communities. In summary, we collected publicly available data on TFs. Initially, we chose to collect data from CollecTF; a bacterial TF database containing experimentally validated TFs. This database was merged to TF sequences from UNIPROT. This merged and hand curated TF database (BacTFDB) was used to train a deep learning model (PredicTF) to predict TFs and their families in genomes and metagenomes. Here, we describe the use of PredicTF to predict TFs for single bacterial species (genomes and metatranscriptomes) and complex communities (metagenomes and metatranscriptomes) (Figure 1). Using PredicTF, the user can determine TFs distribution in complex communities, opening the potential to evaluate regulatory networks in different ecosystems. PredictTF is open-source software.

![workflow](https://github.com/mdsufz/PredicTF/blob/master/workflow.jpeg)
**Rational of the pipeline.**
The pipeline uses The Bacterial Transcription Factor Database (BacTFDB) and DeepARG approach [1] to train (1. Training) a Deep Learning model named PredicTF.  PredicTF can use Genomes (a.1) or Metagenomes (b.1) as input, providing predictions of transcription factors and respective families in a text file (2. Prediction & Annotation). Finally, TFs listed and annotated can be mapped in the Transcriptomes (a.2) or Metatranscriptomes (b.2) providing a list of active TFs in specific conditions (3. Mapping transcripts TFs). 

# 2)	System Requirements
The computational resources vary greatly based on the amount of data in your database. The training step requires intensive computational resources, because of the deep learning, so it is recommended to do the training using the GPU routines from Theano - a Python library that allows you to define, optimize, and evaluate mathematical expressions involving multi-dimensional arrays efficiently (http://deeplearning.net/software/theano/) [5]. However, heavy computation is required only once to obtain the deep learning model (PredicTF) and the prediction routines do not require such computational resources. PredicTF is an open source tool updated twice a year and it can be downloaded from the GitHub page. 

# 3)	Database
To create the Bacterial Transcription Factor Data Base (BacTFDB), we collected data from two publicly available databases. Initially, we chose to collect data from CollecTF [11], a well described and characterized database. Since CollecTF does not provide an API for bulk download, we develop Python code (version 2.7) using the Beautiful Soup 4.4.0 library to recover the data from CollecTF. With this strategy, we downloaded sequences from 390 experimentally validated TFs distributed over 44 TFs families. Additionally, we retrieved TF sequences from UNIPROT using UNIPROT’s API and the filters “Reviewed (Swiss-Prot) - Manually annotated”, bacteria taxonomy and a set of specific keywords (Transcription factor, transcriptional factor, regulator, transcriptional repressor, transcriptional activator, transcriptional regulator). The UNIPROT API was accessed on 8-Sep-2019. Next, we merged the data collected from CollecTF and UNIPROT resulting in a total of 21.971 TFs. Next, we removed redundant TF entries and TF sequences lacking a TF family since PredicTF was designed to also assign TF family. Finally, a manual inspection was performed to remove case sensitive and presence of characters associated to the database header. The final database (BacTFDB) contains a total of 11.691 TF unique sequences (Figure 2). 
To create your own database, the header in your FASTA file needs to match the following structure: 


**>uniq_id|FEATURES|category|group|name**

**Example: >A0A024HKB0|FEATURES|CollecTF|LysR|ClcR**
In this example A0A024HKB0 is the unique number that identify a specific TF, FEATURES is mandatory, CollecTF is the database where the sequence came from, LysR is the family (group) of transcription factor that ClcR (name) belongs. 

**Note: an example file can be downloaded from [here].

![Database](https://github.com/mdsufz/PredicTF/blob/master/database.jpeg)
**Scheme used for the construction of BacTFDB**
Bacterial Transcription Factor Data Base (bacTFDB) were created from from two publicly available databases. We collect 390 TFs from CollecTF and 21.581 from UniProt  (accessed 8-Sep-2019) accumulating 21.581 TF amino acid sequences. We merged the data from CollecTF and UniProt databases resulting in a total of 21.971 TFs amino acid. We removed redundant TF entries and since PredicTF was designed to also assign TF family, TF sequences lacking a TF family were removed. Finally, a manual inspection was performed to remove misleading of spelling, case sensitive and presence of characters associate to the database header. The final database (bacTFDB) contains a total of 11.691 TF unique sequences.


# 4)	PredicTF Pipeline
To use PredicTF it is required some dependencies.

Operating system: Linux64

Programming languages: Python 2.7


**4.1) DEPENDENCIES**

PredicTF requires the instalation:

DeepARG (https://github.com/gaarangoa/deeparg2.0) [1];

DIAMOND (https://github.com/python-diamond/Diamond) [2]; 

Nolearn Lasagne deep learning library (https://lasagne.readthedocs.io/en/latest/) [3]; 

Sklearn machine learning routines (https://scikit-learn.org/stable/) [4]; 

Theano (http://deeplearning.net/software/theano/) [5]. 

Trim Galore - v0.0.4 dev (https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/) [6]. 

MetaSPADES - v3.12.0 (https://github.com/ablab/spades#meta) [7]. 

Emboss transeq (http://www.bioinformatics.nl/cgi-bin/emboss/transeq) [8]. 

Bowtie2 - v2.3.0 (https://sourceforge.net/projects/bowtie-bio/) [9]. 

SAMTools - v1.9 (http://github.com/samtools/) [10].


**4.2) INSTALATION**

1) First you must be sure that DeepARG [1] was correctly installed

2) Open a terminal and clone the source code:
```bash
git clone git@github.com:mdsufz/PredicTF.git
```

# 5) Usage

**1) Activating DeepARG v2.0 environment in the terminal**

```bash
source /path_to_deeparg-ss/deeparg-ss/env-deeparg/bin/activate
```

**2) Creating folders**
Create folders (/model and /v2) in your directory of choice:
```bash
mkdir model 

mkdir v2
```
Create a /v2 folder inside the /model folder:
```bash
cd model

mkdir v2 
```

**Steps 3 to 8 are for those who created their own databases and will train their own models.**

# Very Important: 
**If you are using PredicTF with BacTFDB (database described in this github), skip steps 3 to 8**

**3) Generating a sequence length file**
This file will contain the headers and the protein length for each TF belonging to the database. This file will be used in the training step.  
```bash
python seq_length.py  /path/to/folder/file/with/TF_sequences.fasta > /path/to/folder/features.protein.length 
```

**4) Building database index:**
```bash
/path/to/deeparg-ss/bin/diamond makedb --in /path/to/folder/file/with/TF_sequences.fasta --db /path/to/folder/TF_sequences
```

**5) Generating gene-like sequences from database:**
```bash
python /path/to/deeparg-ss/train/generate_train_genes.py /path/to/folder/file/with/TF_sequences.fasta /train_genes.fasta train
```

**6) Building similarity matrix:**
```bash
/path/to/deeparg-ss/bin/diamond blastp --db /path/to/ TF_sequences.dmnd --query /path/to/train_genes.fasta --id 30 --evalue 1e-10 --sensitive -k 10000 -a /train_genes

/path/to/deeparg-ss/bin/diamond view -a /path/to/train_genes.daa -o /train_genes.tsv
```

**7) Copy files all train files to the created v2 folder (# files : train_genes.daa  train_genes.fasta  train_genes.tsv)**
```bash
cp train* v2
```

**8) Training the model**

Note: Make sure that your fasta file header follows this schema:
>uniq_id|category|group|name

Note2: this step requires a large amount of computational resources and may need to be performed in a cluster.

```bash
python / path/to/deeparg-ss/argdb/train_arc_genes.py /path/to/TF_sequences/folder /path/to/v2/folder 
```

**9) Predicting TFs (genomes or metagenomes)**
**Predicting TFs using the generated database**
```bash
python /path/to/deeparg-ss/deepARG.py --align --type prot --genes --input path/to/target/genomes/genome.fasta --out path/to/results/folder/file2.out --folder #path/to/parent/folder/of/model_and_v2 #where the latter folders were created
```

**10) Mapping TFs (transcriptomes or metatranscriptomes)**

1) Processing the output of Predicting TFs (step 9):
```bash
python process_output_predictf.py <deeparg/file.out.align.daa.tsv> <deeparg/file.out.mapping.ARG> <sequences_input.fa> <predicted_TFs.fa> <predicted_TFs_intervals.tsv>
```

2) Obtaining the mapped regions of each genome or metagenome in their respective transcriptomes or metatranscriptomes:
```bash
python get_mapped_regions.sam <mapping.sam> <output_directory>
```

3) Checking if the predicted TFs are covered by the transcriptome or metatranscriptome:
```bash
python check_mapped_TFs.py <predicted_TFs.fa>  <output_directory/mapped_regions.tsv>
```

# 6) Cite us:


# 7) References
1. Arango-Argoty G, Garner E, Pruden A, Heath LS, Vikesland P, Zhang L. DeepARG: A deep learning approach for predicting antibiotic resistance genes from metagenomic data. Microbiome. BioMed Central Ltd.; 2018;6. 
2. Buchfink B, Xie C, Huson DH. Fast and sensitive protein alignment using DIAMOND. Nat. Methods. Nature Publishing Group; 2014. p. 59–60. 
3. van Merriënboer B, Bahdanau D, Dumoulin V, Serdyuk D, Warde-Farley D, Chorowski J, et al. Blocks and Fuel: Frameworks for deep learning. arxiv.org [Internet]. 2015 [cited 2020 Jun 15]; Available from: https://arxiv.org/abs/1506.00619
4. Pedregosa FABIANPEDREGOSA F, Michel V, Grisel OLIVIERGRISEL O, Blondel M, Prettenhofer P, Weiss R, et al. Scikit-learn: Machine Learning in Python Gaël Varoquaux Bertrand Thirion Vincent Dubourg Alexandre Passos PEDREGOSA, VAROQUAUX, GRAMFORT ET AL. Matthieu Perrot [Internet]. J. Mach. Learn. Res. 2011. Available from: http://scikit-learn.sourceforge.net.
5. The Theano Development Team, Al-Rfou R, Alain G, Almahairi A, Angermueller C, Bahdanau D, et al. Theano: A Python framework for fast computation of mathematical expressions. 2016 [cited 2020 Jun 15]; Available from: https://groups.google.com/group/theano-dev/
6. Krueger F. Babraham Bioinformatics - Trim Galore! [Internet]. Version 0.5.0. 2018 [cited 2020 Jul 29]. Available from: https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/
7. Nurk S, Meleshko D, Korobeynikov A, Pevzner PA. MetaSPAdes: A new versatile metagenomic assembler. Genome Res [Internet]. 2017 [cited 2020 Jul 29];27:824–34. Available from: http://www.genome.org/cgi/doi/10.1101/gr.213959.116.
8. Madeira F, Park YM, Lee J, Buso N, Gur T, Madhusoodanan N, et al. The EMBL-EBI search and sequence analysis tools APIs in 2019. Nucleic Acids Res [Internet]. 2019 [cited 2020 Jul 29];47:W636–41. Available from: https://academic.oup.com/nar/article-abstract/47/W1/W636/5446251
9. Langmead B, Salzberg SL. Fast gapped-read alignment with Bowtie 2. Nat Methods [Internet]. 2012 [cited 2020 Jul 29];9:357–9. Available from: http://bowtie-bio.sourceforge.net/bowtie2/index.shtml.
10. Li H, Handsaker B, Wysoker A, Fennell T, Ruan J, Homer N, et al. The Sequence Alignment/Map format and SAMtools. Bioinformatics [Internet]. 2009 [cited 2020 Jul 29];25:2078–9. Available from: https://academic.oup.com/bioinformatics/article-abstract/25/16/2078/204688
11. Kiliç S, White ER, Sagitova DM, Cornish JP, Erill I. CollecTF: A database of experimentally validated transcription factor-binding sites in Bacteria. Nucleic Acids Res [Internet]. 2014 [cited 2020 Jun 15];42. Available from: https://academic.oup.com/nar/article-abstract/42/D1/D156/1051934
