# PredicTF: a tool to predict bacterial transcription factors in complex microbial communities

# 1) Overview:**
Transcription Factors (TFs) are proteins controlling the rate of genetic information, regulating cellular gene expression. A better understanding of TFs in a bacterial community context open revenues for exploring gene regulation in ecosystems where bacteria play a key role. Here we describe PredicTF, the first platform supporting the prediction and classification of putative bacterial TF not only in single species but also in complex microbial communities. In summary, we collected publicly available data on TFs. Initially, we chose to collect data from CollecTF; a bacterial TF database containing experimentally validated TFs. This database was merged to TF sequences from UNIPROT. This merged and hand curated TF database (bacTFDB) was used to train a deep learning model (PredicTF) to predict new TFs and their families for genomes and metagenomes. Validation of the method can be found in the manuscript XXXXX. Here, we describe the use of PredicTF to predict TFs for single bacterial species (genomes and metatranscriptomes) and complex communities (metagenomes and metatranscriptomes) (Figure 1). Using PredicTF, the user can determine TFs distribution in complex communities, what opens the potential to evaluate regulatory networks in different ecosystems. PredictTF is open-source software.

![workflow] (https://github.com/mdsufz/PredicTF/blob/master/workflow.jpeg)
**Rational of the pipeline.**
The pipeline uses The Bacterial Transcription Factor Database (bacTFDB) and DeepARG approach to train (1. Training) a Deep Learning model named PredicTF.  PredicTF can use Genomes (a.1) or Metagenomes (b.1) as input, providing predictions of novel transcription factors that are listed in a file with their respective TF families (2. Prediction & Annotation). Finally, TFs listed and annotated can be mapped in the Transcriptomes (a.2) or Metatranscriptomes (b.2) providing a list of actives TFs in a specific condition (3. Mapping transcripts TFs). 

# 2)	System Requirements**
The resource requirements for this pipeline will vary greatly based on the amount of data in your DATABASE. The training step requires intensive computational resources, because of the deep learning, so it is recommended to do the training using the GPU routines from Theano a Python library that allows you to define, optimize, and evaluate mathematical expressions involving multi-dimensional arrays efficiently (http://deeplearning.net/software/theano/) (Team, T. T. D. et al., 2016). However, heavy computation is required only once to obtain the deep learning model (PredicTF) and the prediction routines do not require such computational resources. PredicTF is an open source tool updated twice a year and it can be downloaded from the GitHub page. 

# 3)	Database**
To create the Bacterial Transcription Factor Data Base (bacTFDB), we collected data from two publicly available databases. Initially, we chose to collect data from CollecTF (REF), a well described and characterized database. Since CollecTF does not provide an API for bulk download, we develop Python code (version 2.7) using the Beautiful Soup 4.4.0 library to recover the data from CollecTF. With this strategy we listed 390 TF experimentally validated amino acid sequences distributed over 44 TFs families. Additionally, we retrieved TF amino acid sequences from UNIPROT using UNIPROT API filtering for Reviewed (Swiss-Prot) - Manually annotated, from bacteria taxonomy and key words (Transcriotion factor, transcriptional factor, regulator, transcriptional repressor, transcriptional activator, transcriptional regulator). The UNIPROT API was accessed 8-Sep-2019 accumulating 21.581 TF amino acid sequences. We merged the data from CollecTF and UNIPROT databases which resulted in a total of 21.971 TFs amino acid. We removed redundant TF entries and since PredicTF was designed to also assign TF family, TF sequences lacking a TF family were removed. Finally, a manual inspection was performed to remove misleading of spelling, case sensitive and presence of characters associate to the database header. The final database (bacTFDB) contains a total of 11.691 TF unique sequences (Figure 2). 
To create your own database, you need to make sure that your .fasta file header follows this schema (an example file can be downloaded from here):

**>uniq_id|FEATURES|category|group|name
Example: >A0A024HKB0|FEATURES|CollecTF|LysR|ClcR**

![Database] (https://github.com/mdsufz/PredicTF/blob/master/database.jpeg)
**Scheme used for the construction of bacTFDB**

In this example A0A024HKB0 is the unique number that identify a specific TF, FEATURES is mandatory, CollecTF is the database where the sequence came from, LysR is the family (group) of transcription factor that ClcR (name) belongs. 

# 4)	PredicTF Pipeline** 
To use PredicTF it is required some dependencies.
The pipeline was developed in python 2.7 and requires DIAMOND for making the alignments.

**4.1) DEPENDENCIES**
PredicTF requires the next python modules (all can be installed via pip):
Nolearn lasagne deep learning library (https://lasagne.readthedocs.io/en/latest/).
Sklearn machine learning routines (https://scikit-learn.org/stable/).
Theano for fast computation. For GPU usage (see Theano documentation) (http://deeplearning.net/software/theano/).

**4.2) INSTALATION**
Open a terminal and clone the source code:
git clone https://xxxxxxxx


# 5) Usage**

**1) Activating DeepARG v2.0 environment in the terminal

```bash
module load python/2 diamond

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

**Steps 3 to 8 are for those who created their own databases and will train their own models.

**Very Important: 
If you are using PredicTF with bacTFDB (database described in this github), skip steps 3 to 8**

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

**9) Predicting TFs (genomes or metagenomes)
**Predicting TFs using the generated database**
```bash
python /path/to/deeparg-ss/deepARG.py --align --type prot --genes --input path/to/target/genomes/genome.fasta --out path/to/results/folder/file2.out --folder #path/to/parent/folder/of/model_and_v2 #where the latter folders were created

