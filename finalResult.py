import glob, os, sys

inputFolder = sys.argv[1] if sys.argv[1][-1] == '/' else sys.argv[1] + '/'
inputFolder = inputFolder if inputFolder[0] != '/' else inputFolder[1:]
outputFolder = inputFolder + 'final_result'

# if os.path.exists(inputFolder[0:-1] + '_result') is False:
#     os.mkdir(inputFolder[0:-1] + '_result')
# else:
#     os.system('rm -r ' + inputFolder[0:-1] + '_result')
#     os.mkdir(inputFolder[0:-1] + '_result')

if os.path.exists(inputFolder + 'final_result') is False:
    os.mkdir(inputFolder + 'final_result')
else:
    os.system('rm -r ' + inputFolder + 'final_result')
    os.mkdir(inputFolder + 'final_result')

# classification -> genome_orf_0_result.csv
# regression -> genome_orf_0_normal_breast.csv

final_result = []
for classify_result in glob.glob(inputFolder + "classification_result/*"):
    classify_fasta = []
    with open(classify_result, 'r') as classify_infile:
        classify_fasta = [item.rstrip("\n").split(",") for item in classify_infile.readlines()].copy()
    # for index in range(len(classify_fasta)):
    #     while len(classify_fasta[index]) < 10:
    #         classify_fasta[index].append("")

    # combine each tissue result
    regression_fasta = []
    tissueType = ['breast', 'cervix', 'colon', 'lung', 'prostate', 'skin']
    for eachType in tissueType:
        with open(classify_result.replace('classification', 'regression').replace("_result.csv", "_normal_" + eachType + '.csv'), 'r') as infile:
            reg_fasta = [item.rstrip('\n').split(',') for item in infile.readlines()[1:]].copy()

        if len(regression_fasta) == 0:
            regression_fasta = reg_fasta.copy()
        else:
            while len(reg_fasta) != 0:
                for index in range(len(regression_fasta)):
                    if len(reg_fasta) == 0:
                        break
                    if reg_fasta[-1][0] == regression_fasta[index][0]:
                        regression_fasta[index].append(reg_fasta[-1][1])
                        del reg_fasta[-1]

    # combine classification and regression result

    while len(regression_fasta) != 0:
        for index in range(len(classify_fasta)):
            if len(regression_fasta) == 0:
                break
            if regression_fasta[-1][0] == classify_fasta[index][0]:
                classify_fasta[index].extend(regression_fasta[-1][1:])
                del regression_fasta[-1]

    for index in range(len(classify_fasta)):
        if len(classify_fasta[index]) == 4:
            if classify_fasta[index][-1] != "":
                classify_fasta[index].append("Zero samples in the AD range!")
                classify_fasta[index].extend(["", "", "", "", ""])
            else:
                classify_fasta[index].extend(["", "", "", "", "", ""])

    classify_fasta.insert(0, ["Name", "Sequence", "Predicted Label", "Predicted Probability", "Breast", "Cervix", "Colon", "Lung", "Prostate", "Skin"])

    if os.path.isfile(inputFolder[0:-1] + "_result.csv") is False:
        outfile = open(inputFolder[0:-1] + '_result.csv', 'w+')
        for item in classify_fasta:
            outfile.write(",".join(item) + '\n')
        outfile.close()
    else:
        outfile = open(inputFolder[0:-1] + '_result.csv', 'a')
        for item in classify_fasta:
            outfile.write(",".join(item) + '\n')
        outfile.close()
os.system('rm -r ' + inputFolder)
