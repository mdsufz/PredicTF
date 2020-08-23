import sys
import os
import commands
from itertools import groupby





def get_best_matches(mappingARG):
	f=open(mappingARG,"r")
	best_matches={}
	header=f.readline()

	while True:
		l=f.readline()
		if not l: break
		else:
			query=l.split()[3]

			identi=l.split()[7]
			alilenght=l.split()[8]
			alibitscore=l.split()[9]
			alievalue=l.split()[10]

			best_matches[query]=[identi,alilenght,alibitscore,alievalue]

			
	f.close()
	return best_matches

def get_all_matches(aligntsv,tf_best_matches):
	f=open(aligntsv,"r")
	dic_coords={}
	data=f.readlines()
	f.close()
	candidates=[]
	# remove all lines that do not have a query
	for l in data:
		if l.split()[0] not in tf_best_matches:
			pass
		else:
			candidates.append(l)
	return candidates
	
def retrieve_coords(tf_best_matches,all_matches):

	c=0
	final_coords={}
	for k,v in tf_best_matches.iteritems():
		c= c + 1
		for match in all_matches:
			if k in match:
				if v[0] == match.split()[2]: # check for identity
					if v[1] == match.split()[3]: # check for alignment length
						if v[2] == match.split()[-1]: # check for alignment bitscore
							if v[3] == match.split()[-2]: # check for alignment evalue
								status,aux=commands.getstatusoutput("echo \""+match +"\" | cut -f7,8  | head -n1 ")
								coordsaux= aux.split('\t')
								coords=[int(coordsaux[0]),int(coordsaux[1])]
								final_coords[k]=coords
								break
	return final_coords

def handling_fasta(fasta_name,tf_coords,fa_out):
	print "-> extracting to",fa_out
	c=0
    	# given a fasta file. yield tuples of header, sequence
	f = open(fasta_name) # opens fasta file
	fout=open(fa_out,"w")
	f_iterator = (x[1] for x in groupby(f, lambda line: line[0] == ">"))
	for header in f_iterator:
		header = header.next()[1:].strip()                   # drop the ">"   # <-------------------------------- optional
		seq = "".join(s.strip() for s in f_iterator.next())  # join all sequence lines to one.
		seq = str(seq)                                       # cast sequence to string  #  
		header = str(header)                                 # cast header to string    #  for troubleshooting purpose
		header = header.split()[0]
		if header in tf_coords:
			fout.write(">TF-"+str(c)+"_"+header+"\n")
			fout.write(seq[tf_coords[header][0]-1:tf_coords[header][1]]+"\n")
			c=c+1

        
deeparg_output_align_daa_tsv=sys.argv[1] # deeparg output file.out.align.daa.tsv
deeparg_output_mappingARG =sys.argv[2] # deeparg output file.out.mapping.ARG
fasta_name = sys.argv[3]   # manual input    sequences.fa
fasta_out = sys.argv[4]   # sequences from the predicted TFS 
tf_intervals= sys.argv[5] # file to dump the intervals from each TF found


# for each line in mapping.ARG
	# fetch query and 4 parameters (identity,length, bitscore,evale)
	# search in mapping.tsv for the 5 fields in their specific expected locations


# 1 get the query and 4 parameters (key=query, value= [identity, alignment, bitscore, evalue])
print 'step 1/5'
tf_best_matches = get_best_matches(deeparg_output_mappingARG)

# 2 extract all data from the align.tsv file
print 'step 2/5'
all_matches = get_all_matches(deeparg_output_align_daa_tsv,tf_best_matches)

# 3 for each entry in tf_best_matches check inside all_matches
print 'step 3/5'
final_coords=retrieve_coords(tf_best_matches,all_matches)

print 'step 4/5'
#f=open("/gpfs1/data/msb/CAS/zander/TF_investigation/deeparg_3/TF_intervals.tsv","w")

f=open(tf_intervals,"w")

for k,v in final_coords.iteritems():
	f.write(k+"\t"+str(v[0])+"\t"+str(v[1])+"\n")
f.close()
handling_fasta(fasta_name,final_coords,fasta_out)
print 'step 5/5'
print 'done'
