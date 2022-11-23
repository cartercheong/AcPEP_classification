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

def createFolder(start, end, folderdir, tmpName, fasta, rootDir):
    startResidue = start
    endResidue = end + 1
    os.mkdir(rootDir + '/' + folderdir)
    createFolder = rootDir + '/' + folderdir + '/' + tmpName + "_NT_CT_" + str(startResidue) + '_' + str(endResidue-1)
    os.mkdir(createFolder)
    for ct in range(startResidue, endResidue):
        ct_f = open(createFolder + '/' + tmpName + '_CT_' + str(ct) + '.txt', 'w')
        for num in range(len(fasta)):
            ct_f.write(fasta[num][0] + '\n')
            ct_f.write(fasta[num][1][:ct] + '\n')
        ct_f.close()
    
    for nt in range(startResidue, endResidue):
        nt_f = open(createFolder + '/' + tmpName + '_NT_' + str(nt) + '.txt', 'w')
        for num in range(len(fasta)):
            nt_f.write(fasta[num][0] + '\n')
            nt_f.write(fasta[num][1][:nt] + '\n')
        nt_f.close()
    
    os.system('cp -r' + ' ' + createFolder + ' ' + createFolder + '_pssm')
    os.system('cp -r' + ' ' + createFolder + ' ' + createFolder + '_ss')

def removeEmptyFile(filePath):
    for file in glob.glob(filePath + '/*.txt'):
        stateinfo = os.stat(file)
        if stateinfo.st_size == 30:
            os.remove(file)

def dGmemFeature(fastaList):
    # fastaList -> ['>ACP_1', 'XXXXXXXXXXXX']
    waterToDOPCinterface = {'L': -14.1, 'I': -20.6, 'V': -12.2, 'F': -14.9, 'A': -6.8, 'W': -21.6, 'M': -10.5, 'C': -6.6, 'Y': -14.0, 'T': -4.2, 'S': -0.7, 'Q': -8.9, 'K': -18.6, 'N': -6.5, 'E': -1.68, 'D': 1.6, 'R': -21.2, 'H': 0.0, 'G': 0.0, 'P': 0.0}
    waterToDOPCcenter = {'L': -15.2, 'I': -22.1, 'V': -13.8, 'F': -12.8, 'A': -8.4, 'W': -4.9, 'M': -4.4, 'C': -3.4, 'Y': 6.6, 'T': 13.9, 'S': 15.8, 'Q': 20.2, 'K': 19.9, 'N': 23.9, 'E': 21.1, 'D': 31.0, 'R': 58.1, 'H': 0.0, 'G': 0.0, 'P': 0.0}
    dGinterface=0.0
    dGcenter=0.0
    for char in fastaList[1]:
        dGinterface += waterToDOPCinterface[char]
        dGcenter += waterToDOPCcenter[char]

    return dGinterface, dGcenter

# ------------------------------------------------------------------------------------------------------------

# input:    Name of Training dataset, Name of Testing dataset, Path of Training dataset, Path of Testing dataset, List of feature file
# output:   Feature X of Training, Feature X of Testing, Label Y of Training, Label Y of Testing, Output filename of Training, Output filename of Testing, Header List of Training, Header List of Testing
def readDataset(pathTraining="", inputFile=[]):
    combine_Training_X = []
    headerTraining = []
    outfile_train=""
    outfile_test=""
    for fileTraining in inputFile:
        fileTesting = fileTraining

        infile=pathTraining+fileTraining.strip()

        dataset = pandas.read_csv(infile,sep="\t",header=0)
        for ele in list(dataset.columns.values)[1:]:
            headerTraining.append(fileTraining+';'+ele)
        nrow, ncol = dataset.shape

        print(infile," ", nrow, " ", ncol )

        # Split-out feature columns and class label
        array = []
        array = dataset.values   # convert dataframe into numpy array
        X = array[:,1:(ncol)]

        if fileTraining == inputFile[0]:
            combine_Training_X = X
            outfile_train=outfile_train+fileTraining.strip(".txt")
        else:
            combine_Training_X = numpy.concatenate((combine_Training_X, X),axis=1)
            outfile_train=outfile_train+"_"+fileTraining.strip(".txt")

    #endfor
    return combine_Training_X, outfile_train, headerTraining

# ------------------------------------------------------------------------------------------------------------
