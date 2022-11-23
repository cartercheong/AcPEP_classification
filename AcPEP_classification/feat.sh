#!/usr/bin/bash
startResidue=${1}
endResidue=${2}
tmpName=${3}
folderdir=${4}
rootDir=${5}
currentPath=`pwd`

#all_fea_type="AAC EAAC CKSAAP DPC DDE TPC BINARY GAAC EGAAC CKSAAGP GDPC GTPC AAINDEX ZSCALE BLOSUM62 NMBroto Moran Geary CTDC CTDT CTDD CTriad KSCTriad SOCNumber QSOrder PAAC APAAC PSSM SSEC SSEB Disorder DisorderC DisorderB ASA TA"

all_fea_type="AAC CKSAAP DPC CTDC CTDT CTDD DDE"

lambda_type=" SOCNumber QSOrder PAAC APAAC"

if [ ! -d ${rootDir}/${folderdir}/${tmpName}_all_ifea ]
then
	mkdir ${rootDir}/${folderdir}/${tmpName}_all_ifea
fi

for all_fea in $all_fea_type ; do
# echo ${all_fea}
python ${rootDir}/serverModel/iFeature-master/iFeature.py --file ${rootDir}/${tmpName}_tmpFolder/${tmpName}_normal.fasta --type ${all_fea} --out ${rootDir}/${folderdir}/${tmpName}_all_ifea/${tmpName}_${all_fea}.txt
done

for type in $lambda_type ; do
# echo ${type}
for ((lambda=3;lambda<=9;lambda++)); do
python ${rootDir}/serverModel/iFeature-master/codes/${type}.py ${rootDir}/${tmpName}_tmpFolder/${tmpName}_normal.fasta ${lambda} ${rootDir}/${folderdir}/${tmpName}_all_ifea/${tmpName}_${type}_lambda${lambda}.txt
done
done

