import os
import math
import subprocess
import sys
import commands



def merge_intervals(intervals):
    #We can have intervals sorted by the first interval and we can build the merged list in the same interval list by checking the intervals one by one not appending to another one so. we increment i for every interval and interval_index is current interval check
    # https://stackoverflow.com/questions/49071081/merging-overlapping-intervals-in-python
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    interval_index = 0
    #print(sorted_intervals)
    for  i in sorted_intervals:

        if i[0] > sorted_intervals[interval_index][1]:
            interval_index += 1
            sorted_intervals[interval_index] = i
        else:
            sorted_intervals[interval_index] = [sorted_intervals[interval_index][0], i[1]]
    #print(sorted_intervals)
    return sorted_intervals[:interval_index+1]


def get_mapped_intervals_from_sam(sam,workdir ):

    
    print '\nstart'
    # 1) extract readid, refseqid, start mapping and readse
    if os.path.isdir(workdir) == False:
        os.system("mkdir "+workdir) # create working directory
    status,aux=commands.getstatusoutput('date')
    print 'step 1',aux
    cmd1 = "samtools view -F 4 "+sam+"  | cut -f3,4,10 > "+workdir+"/aux1"
    status,aux=commands.getstatusoutput(cmd1)
    os.system("touch "+workdir+"/step1done")

    # 2) getting the length of mapped seqs and creating interval (refseq, mappingstart, mapping end
    status,aux=commands.getstatusoutput('date')
    print 'step 2',aux
    f=open(workdir+"/aux1","r")
    data = f.readlines()
    os.system("touch "+workdir+"/step2done")

    # 3)  putting all intervals in a dictionary dic[seq]=[intervals]
    status,aux=commands.getstatusoutput('date')
    print 'step 3',aux
    dic={}
    for line in data:
        seq=line.split("\t")[0]
        start=int(line.split("\t")[1])
        end=start + int(len(line.split("\t")[2]))
        interval=[start,end]
        if seq not in dic:
            dic[seq] = [interval]
        else:
            dic[seq].append(interval)
    f.close()
    os.system("touch "+workdir+"/step3done")

    # 4)  overlapping all intervals and dumping into new dic_merged 
    status,aux=commands.getstatusoutput('date')
    print 'step 4',aux
    dic_merged={}
    for k,v in dic.iteritems():
        merged_intervals= merge_intervals(v)
        dic_merged[k]=merged_intervals
        #del dic[k]
    os.system("touch "+workdir+"/step4done")

    # 5) getting overlapped intervals and dumping to final file mapped_regions.tsv
    status,aux=commands.getstatusoutput('date')
    print 'step 5',aux
    fout=open(workdir+"/mapped_regions.tsv","w")
    for k,v in dic_merged.iteritems():
        #print k,
        aux=k+'\t'
        for region in v:
            aux=aux+str(region[0])+','+str(region[1])+';'
        fout.write(aux+"\n")
    fout.close()
    
    os.system("touch "+workdir+"/step5done")
    print 'done'  

    #return dic_merged


sam=sys.argv[1]
workdir=sys.argv[2]
mapped_regions=get_mapped_intervals_from_sam(sam,workdir)
