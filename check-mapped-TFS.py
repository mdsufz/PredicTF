import os
import math
import subprocess
import sys
import commands

#from /gpfs1/data/msb/lummy/feb_2020/assembly/P19012_mgSRR7067999/extract_TFs_deeparg import GET_tfs_coordinates, 




def get_intervals_from_TFs(TFs_intervals_file):
    dic={}
    
    f=open(TFs_intervals_file,'r')
    while True:
        l=f.readline()
        if not l: break
        else:
            #print l.strip()
            frame=int(l.split()[0].split("_")[-1])
            #print frame
            #print ""
            raw_interval=[int(l.split()[1]),  int(l.split()[2])]
            if frame   == 1: interval=[int(l.split()[1]), int(l.split()[2]),'F']
            elif frame == 2: interval=[raw_interval[0]+1, raw_interval[1]+1,'F'] 
            elif frame == 3: interval=[raw_interval[0]+2, raw_interval[1]+2,'F'] 
            elif frame == 4: interval=[int(l.split()[1]), int(l.split()[2]),'R']
            elif frame == 5: interval=[raw_interval[0]-1, raw_interval[1]-1,'R']
            elif frame == 6: interval=[raw_interval[0]-2, raw_interval[1]-2,'R']
            #print interval
            #print ""
            interval.append(frame)
            dic[l.split()[0][:-2]] = interval
    return dic

def get_mapped_regions(SAM_mapped_regions):
    mapped_dic={}
    f=open(SAM_mapped_regions,"r")
    while True:
        l=f.readline()
        if not l: break
        else:
            info=l.split()
            #print info
            mapped_dic[info[0]]=info[1].split(';')
    return mapped_dic
# inputs
# TFs_intervals_file
# SAM_mapped_regions


#TFs_intervals_file='/gpfs1/data/msb/lummy/feb_2020/assembly/P19012_mgSRR7067999/P19012-mgSRR7067999-predicted-TFs_intervals.tsv'

#SAM_mapped_regions='/gpfs1/data/msb/lummy/feb_2020/mapping_mt2mgs/sam_files/workdir_mtSRR7523243/mapped_regions.tsv'

#deeparg_mapping_ARG='/gpfs1/data/msb/lummy/feb_2020/assembly/P19012_mgSRR7067999/deeparg/file.out.mapping.ARG'

TFs_intervals_file=sys.argv[1]
SAM_mapped_regions=sys.argv[2]

ref=SAM_mapped_regions.split('/')[-2].replace("workdir_","")

TFs_dic= get_intervals_from_TFs(TFs_intervals_file)
mapped_dic= get_mapped_regions(SAM_mapped_regions)

found_TFs=0
#print TFs_dic
for k,v in TFs_dic.iteritems():
   # print k,v
    if k in mapped_dic:
        #print k
        tf_start,tf_end,orientation,frame = v[0],v[1],v[2],v[3]
        #print start,end
        for region in mapped_dic[k]:
            if len(region.split(',')) == 2:
                #print region
                #a=raw_input()
                map_start,map_end = region.strip().split(',') 
                if int(tf_start) >= int(map_start): 
                    if int(tf_end) <= int(map_end):
                        found_TFs = found_TFs + 1
                        print ref+"\t"+k+'_'+str(frame)+'\t'+orientation#'YESS'
                        # print k+'_'+str(frame)

#print 'number of TFS :', len(TFs_dic)
#print 'for '+ref+', '+str(found_TFs)+' TFs were found' 
