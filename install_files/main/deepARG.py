import predict.bin.deepARG as clf
import sys
import getopt
import options as gopt
import os

iden = 50
evalue = 1e-10
minCoverage = 0.8
numAlignmentsPerEntry = 1000
pipeline = 'reads'
version = 'v2'
#opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["predict", "align", "genes", "reads",
#                                                  "v1", 'type=',  "input=", "output=", "iden=", "prob=", "evalue=", "coverage=", "nk="])

opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["predict", "align", "genes", "reads",
                                                   "v1", 'type=',  "input=", "output=", "iden=", "prob=", "evalue=", "coverage=", "nk=","folder="])

options = {}
for opt, arg in opts:
    if opt == '-h' or opt == '--help':
        print('''
                DeepARG:
                    https://bitbucket.org/gusphdproj/deeparg-ss

                    A deep learning based approach for predicting Antibiotic Resistance Genes and annotation.
                    You can use --predict if you already have a blast-like tabular output (outfmt6) from any
                    other program (blast, userarch, vsearch, diamond, etc.). Here you can use the --reads options
                    that will predict NGS reads or --genes that will take longer gene-like sequences (NOT ASSEMBLED CONTIGS).
                    If you use the --align flag, the system will first perform blast over the input you provide
                    (genes or reads) and continue with the predict stage. There are additional parameter such as idenity (60% default)
                    or prediction probability to retrieve the most significant predictions (default --prob 0.8).

                USAGE:  python deepARG.py --predict --reads --input /Volumes/data/dev/deepARG/test/test.tsv --output /Volumes/data/dev/deepARG/test/test.out
                        python deepARG.py --align --genes --type prot --input /Volumes/data/dev/deepARG/test/test.fasta --output /Volumes/data/dev/deepARG/test/test.out

                General options:
                    --type          (nucl/prot) Molecule type of input data
                    --iden          (50% default) minimum percentaje of identity to consider
                    --prob          (0.8 default) Significance of the prediction, default 0.8
                    --evalue        (1e-10 default) evalue of alignments (default 1e-10)
                    --coverage      (0.8 default) minimum coverage of the alignment (alignment_length/reference_gene_length)
                    --reads         short sequences version
                    --genes         long sequences version
                    --v1            Use this flag to activate deepARG version v1 [default: v2]
		    --folder		Location of where features.dmnd is stored
                Optional:
                    --nk            (1000 default) maximum number of alignments reported for each query (diamond alignment)


                PREDICT ARG-like sequences using blast output file as input:
                    deepARG --predict --input <inputfile> --output <outputfile>
                        --input         blast tab delimited file.
                        --output        output of annotated reads.

                ALIGN sequences to DEEP_ARGDB and PREDICT ARGs using fasta files as input:
                    deepARG --align  --input <inputfile> --output <outputfile>
                        --input         fasta file containing reads.
                        --output        blast tab delimited alignment file.

                Thanks for using DeepARG
                ''')

        sys.exit()
    else:
        options[opt.replace("--", "")] = arg

if "genes" in options:
    mdl = "_LS"
    iden = 30
    evalue = 1e-10
    prob = 0.8
    minCoverage = 0.8
    pipeline = 'genes'

if "reads" in options:
    mdl = "_SS"
    iden = 60
    evalue = 1e-5
    prob = 0.8
    minlen = 0.8
    minCoverage = 30
    pipeline = 'reads'

if "v1" in options:
    print("Using deepARG models Version 2")
    version = "v1"

try:
    iden = float(options['iden'])
except:
    pass

try:
    evalue = float(options['evalue'])
except:
    pass

try:
    prob = float(options['prob'])
except:
    pass

try:
    minCoverage = float(options['coverage'])
except:
    pass

try:
    numAlignmentsPerEntry = int(options['nk'])
except:
    pass

if "type" in options:
    if options['type'] == "prot":
        aligner = "blastp"
    if options['type'] == "nucl":
        aligner = "blastx"

if "predict" in options:
    clf.process(options['input'], options['output'], iden,
                mdl, evalue, prob, minCoverage, pipeline, version)

if "align" in options:
    print("DIAMOND "+aligner+" alignment")

    print(" ".join([gopt.path+'/bin/diamond ', aligner,
                        '-q', options['input'],
                        #'-d', gopt.path+"/database/"+version+"/features",
                        '-d',options['folder']+"/database/v2/features",# location where the features.dmnd is stored - should be dynamic
                        '-k', str(numAlignmentsPerEntry),
                        '--id', str(iden),
                        '--sensitive',
                        '-e', str(evalue),
                        '-a', options['output']+'.align'
                        ]))


    os.system(" ".join([gopt.path+'/bin/diamond ', aligner,
                        '-q', options['input'],
                        #'-d', gopt.path+"/database/"+version+"/features",
                      	'-d',options['folder']+"/database/v2/features",# location where the features.dmnd is stored - should be dynamic
                        '-k', str(numAlignmentsPerEntry),
                        '--id', str(iden),
                        '--sensitive',
                        '-e', str(evalue),
                        '-a', options['output']+'.align'
                        ]))

    print("parsing output file")
    os.system(" ".join([
        gopt.path+'/bin/diamond view',
        '-a', options['output']+'.align.daa',
        '-o', options['output']+'.align.daa.tsv'
    ]))
    clf.process(options['output']+'.align.daa.tsv', options['output'] +
                '.mapping', iden, mdl, evalue, prob, minCoverage, pipeline, version)
