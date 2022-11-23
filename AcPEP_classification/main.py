#!~/anaconda3/bin/python
import os, pickle, numpy, time, re, glob
from functionList import *
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
# fasta list [['AC_1', 'ALWKTMLKKLGTMALHAGKAALGAAADTISQGTQ'], ['AC_2', 'AWKKWAKAWKWAKAKWWAKAA']]

start_time = time.time()

inputFolder = sys.argv[1] if sys.argv[1][-1] == '/' else sys.argv[1] + '/'
inputFolder = inputFolder if inputFolder[0] != '/' else inputFolder[1:]
outputFolder = inputFolder + 'classification_result'

rootDir = os.path.abspath(os.getcwd())

if os.path.exists(inputFolder + 'classification_result') is False:
    os.mkdir(inputFolder + 'classification_result')
else:
    os.system('rm -r ' + inputFolder + 'classification_result')
    os.mkdir(inputFolder + 'classification_result')

for inputFile in glob.glob(inputFolder + '*.fasta'):

    tmpName = inputFile.split('/')[-1].split('.')[0]
    folderdir = inputFile.split('/')[-1].split('.')[0] + '_tmpFolder'

    fasta = readFasta(inputFile)
    # rootDir = os.path.abspath(os.getcwd())

    fasta_normal = []
    fasta_long = []
    fasta_short = []
    for item in fasta:
        if len(item[1]) < 10:
            fasta_short.append(item)
        elif len(item[1]) > 38:
            fasta_long.append(item)
        else:
            fasta_normal.append(item)

    # create folder
    if os.path.exists(rootDir + '/' + folderdir) is False:
        os.mkdir(rootDir + '/' + folderdir)
    else:
        os.system('rm -r ' + rootDir + '/' + folderdir)
        os.mkdir(rootDir + '/' + folderdir)


    out_normal_fasta = open(rootDir + '/' + tmpName + '_tmpFolder/' + tmpName + '_normal.fasta', 'w+')
    for item in fasta_normal:
        out_normal_fasta.write(item[0] + '\n' + item[1] + '\n')
    out_normal_fasta.close()

    out_long_fasta = open(rootDir + '/' + tmpName + '_tmpFolder/' + tmpName + '_long.fasta', 'w+')
    for item in fasta_long:
        out_long_fasta.write(item[0] + '\n' + item[1] + '\n')
    out_long_fasta.close()

    out_short_fasta = open(rootDir + '/' + tmpName + '_tmpFolder/' + tmpName + '_short.fasta', 'w+')
    for item in fasta_short:
        out_short_fasta.write(item[0] + '\n' + item[1] + '\n')
    out_short_fasta.close()

    # generate all feature
    os.system('bash ' + rootDir + '/serverModel/feat.sh' + ' ' + str(10) + ' ' + str(10) + ' ' + tmpName + ' ' + folderdir + ' ' + rootDir)

    # load model - alternate
    fclass = open(rootDir + '/serverModel/sav/selected.txt','r')
    selected = fclass.readline()
    tmp = [True if x == 'True' else False for x in selected.split('\t')]
    fclass.close()
    with open(rootDir + '/serverModel/sav/model.sav', 'rb') as f:
        model = pickle.load(f)
    with open(rootDir + '/serverModel/sav/scaler.sav', 'rb') as f:
        standscaler = pickle.load(f)

    featureList = [tmpName + '_QSOrder_lambda8.txt', tmpName + '_APAAC_lambda3.txt', tmpName + '_PAAC_lambda7.txt', tmpName + '_AAC.txt', tmpName + '_CKSAAP.txt', tmpName + '_CTDC.txt', tmpName + '_DPC.txt', tmpName + '_CTDD.txt', tmpName + '_CTDT.txt']

    X, out, header = readDataset(pathTraining=rootDir + '/' + folderdir + '/' + tmpName + "_all_ifea/", inputFile=featureList)
    X = standscaler.transform(X)
    X = X[:, tmp].copy()

    result = model.predict(X)
    result_proba = model.predict_proba(X)

    with open(rootDir + '/' + outputFolder + '/' + tmpName + '_result.csv', 'w+') as outfile:
        for index in range(len(fasta_normal)):
            label_str = "1" if result_proba[index][1] > 0.50 else "0"
            outfile.write(fasta_normal[index][0].replace('>','') + ',' + fasta_normal[index][1] + ',' + label_str + ',' + str(result_proba[index][1]) + '\n')
        for index in range(len(fasta_short)):
            outfile.write(fasta_short[index][0].replace('>','') + ',' + fasta_short[index][1] + ',' + 'Sequence length must > 9' + ',' + ''  + '\n')
        for index in range(len(fasta_long)):
            outfile.write(fasta_long[index][0].replace('>','') + ',' + fasta_long[index][1] + ',' + 'Sequence length must < 39' + ',' + '' + '\n')
    os.system("rm -r " + rootDir + '/' + folderdir)

    with open(rootDir + '/' + inputFolder + tmpName + '_normal.fasta', 'w+') as outfile:
        for index in range(len(fasta_normal)):
            outfile.write(fasta_normal[index][0] + '\n' + fasta_normal[index][1] + '\n')
    
    end_time = time.time()
    print("running time: {}".format(end_time-start_time))
