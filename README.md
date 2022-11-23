# AcPEP_classification
=========

Arguments <br>
-> path of fasta file <br>
-> jobid <br>

Step 1. Determine whether user choose genome screening method or not. 

	No need to apply genome screening
	
	python genome_seq/ORF_noCodon.py ${arg 1 -> path of fasta file} ${arg 2 -> jobid}

	Need to apply genome screening
	
	python genome_seq/ORF_Codon.py ${arg 1 -> path of fasta file} ${arg 2 -> codon table} ${arg 3 -> jobid}
	
	* Codon Table in [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 16, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33]

Remark: 
	For process screening, it required to have "biopython" in python package which anaconda environment can be migrate from AmPEP server. 

Step 2. Process classification model

	python AcPEP_classification/main.py genome_${arg 1 -> jobid}/

Remark: 
	Before process classification model, have to use "conda activate" to activate classification anaconda environment. Here is package version requirements below.

	Anaconda 3 - 4.8.3
	Python 3 - 3.7.6
	sklearn - 0.22.1
	numpy - 1.20.1
	scipy - 1.4.1
	pandas - 0.25.3

Step 3. Process regression model

	python xDeep-AcPEP-main/prediction/prediction.py genome_${arg 1 -> jobid}/

Remark:
	Before process regression model, have to use "conda activate" to activate regression anaconda environment. Here is package version requirements below.

	Anaconda 4.7.0
	Python 3.6.9
	Scikit-learn 0.21.3
	Pytorch 1.2.0 with CUDA 10.0
	Scipy 1.4.1
	Pandas 1.0.2
	Numpy 1.18.1
	Openpyxl 3.0.6

Step 4. Combine classification result and regression result

	python finalResult.py genome_${arg 1 -> jobid}/

Step 5. Got result csv with below content in genome_${arg 1 -> jobid}_result.csv

	Name,Sequence,Predicted Label,Predicted Probability,Breast,Cervix,Colon,Lung,Prostate,Skin
	+|TRINITY_DN102890_c0_g1_i1:100..165,IRLRFLRRRRRSSIATLMSETG,0,0.06653945045890704,191.619397,418.179679,250.175822,104.760344,192.834661,6.461527
