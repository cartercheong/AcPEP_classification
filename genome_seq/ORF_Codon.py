import Bio.Data.CodonTable
from Bio.Seq import Seq
from Bio import SeqIO
import sys
import re
import os

#short_f = open("./short_len.fasta",'w')
#long_f = open("./long_len.fasta",'w')
#B,J,O,U,X,Z

# codon tab input "1".
filefasta = sys.argv[1]
codontablenum = sys.argv[2]
jobid = sys.argv[3]
#jid = filefasta.split('.')[0]
# out_f = open("/".join(filefasta.split('/')[0:-1]) + '/' + "genome_orf.fasta",'w')

fasta_sequences = SeqIO.parse(open(filefasta),'fasta')

table = int(codontablenum) #(standarde_table) for C_glabrata
#table = 12 #(Alternative Yeast Nuclear) for C_albicans
min_prot_len = 0 #(to avoid Null prot)

aminoacids = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
seqnum = 0
filenum = 0

#strand 1 : frame 1,2,3 => +1, +2, +3
#strand -1 : frame 1,2,3 => -1, -2, -3

if os.path.isdir("genome_" + jobid) is True:
  os.system("rm -r " + "genome_" + jobid)
os.system("mkdir " + "genome_" + jobid)

for fasta in fasta_sequences:
  seq = fasta.seq
  iden = fasta.id
  for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
    for frame in range(3):
      aa_count = 0
      posi_frame = frame+1
      # trim sequence
      trim_char = len(nuc[frame:])%3
      trim_seq = nuc[frame:-trim_char]
      for prot in trim_seq.translate(table).split('*'):
        indx=-1;
        for aa in prot:
          indx = indx + 1
          posi_aa = posi_frame + aa_count*3
          if aa == 'M':
            prot_new = prot[indx:]
            if strand == 1:
              s= '+'
            else :
              s='-'

            if len(prot_new)-1 >= 10 and len(prot_new)-1 <= 50: # after excluding 'M' min length with be 5
              notinaa = 0
              for char in prot_new:
                if char not in aminoacids:
                  notinaa = 1
              if notinaa == 0:
                # out_f.write(">%s|%s:%d..%d\n" % (s,iden,posi_aa+3,(len(prot_new)-1)*3-1+posi_aa+3))
                # out_f.write("%s\n" % (prot_new[1:]))

                if seqnum == 0:
                  splitoutf = open("genome_" + jobid + "/genome_orf_"+str(filenum)+".fasta",'w')
                splitoutf.write(">%s|%s:%d..%d\n" % (s,iden,posi_aa+3,(len(prot_new)-1)*3-1+posi_aa+3))
                splitoutf.write("%s\n" % (prot_new[1:]))
                seqnum += 1
                if seqnum == 1000:
                  splitoutf.close()
                  seqnum = 0
                  filenum+=1

          aa_count = aa_count+1

        aa_count = aa_count+1
#short_f.close()
#long_f.close()
#out_f.close()
if seqnum != 0:
  splitoutf.close()
