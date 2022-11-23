import sys, glob, re, os, pandas, numpy

def readFasta(file):
    if os.path.exists(file) == False:
        print("Error: " + file + " does not exist")
        sys.exit()
    with open(file, "r") as f:
        records = f.read()
    if re.search('>', records) == None:
        print('The input file in not Fasta format')
        sys.exit()
    records = records.split('>')[1:]
    myFasta = []
    for fasta in records:
        array = fasta.split('\n')
        name, sequence = array[0].split()[0], re.sub('[^ARNDCQEGHILKMFPSTWYV-]', '-', ''.join(array[1:]).upper())
        myFasta.append([name, sequence])
    for index in range(len(myFasta)):
        myFasta[index][0] = '>' + myFasta[index][0]
    return myFasta


# input fasta file name
in_name = sys.argv[1]
jobid = sys.argv[2]
fasta = readFasta(in_name)

if os.path.exists("genome_" + jobid) is False:
    os.system('mkdir' + ' ' + "genome_" + jobid)
else:
    os.system('rm -r' + ' ' + "genome_" + jobid)
    os.system("mkdir" + ' ' + "genome_" + jobid)

seqnum = 0
filenum = 0
for item in fasta:

    if seqnum == 0:
        out_f = open("genome_" + jobid + '/' + "genome_orf_" + str(filenum) + '.fasta', 'w+')
    out_f.write("\n".join(item) + '\n')
    seqnum += 1
    if seqnum == 1000:
        out_f.close()
        seqnum = 0
        filenum += 1

if seqnum != 0:
    out_f.close()

os.system("python " + os.path.abspath(os.getcwd()) + "/" + "/".join(sys.argv[0].split('/')[0:-1]) + "/model_cla_reg.py")


