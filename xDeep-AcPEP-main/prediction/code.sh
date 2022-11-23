#!/bin/bash

type="breast cervix colon lung prostate skin"

mkdir Anal_result/AnalTissues1DS_input_skin
for filename in Anal/AnalTissues1DS_input/*;
do
		
	#echo $filename;
	srun python prediction.py -t skin -m model/ -d $filename -o Anal_result/AnalTissues1DS_input_skin/ 2>&1 &
done



#for i in {0..5}
#do 
	#srun python prediction.py -t breast -m model/ -d Anal/AnalFin1DS/
#done
