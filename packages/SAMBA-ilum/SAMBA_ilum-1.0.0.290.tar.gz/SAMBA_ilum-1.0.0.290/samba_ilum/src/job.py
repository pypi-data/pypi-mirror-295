# SAMBA_ilum Copyright (C) 2024 - Closed source


#--------------------------------------------
vasp_std = 'srun -n ${SLURM_NTASKS} vasp_std'
vasp_ncl = 'srun -n ${SLURM_NTASKS} vasp_ncl'
#--------------------------------------------
folders1 = '${folders1[@]}'
folders2 = '${folders2[@]}'
tasks1 = '${ttasks[@]}'
tasks2 = '${tasks[@]}'
files = '${files[@]}'
temp1 = "`echo $j|cut -d '.' -f1`"
temp2 = "`echo $j|cut -d '.' -f2`"
temp3 = "`echo $k|cut -d '.' -f1`"
temp4 = "`echo $k|cut -d '.' -f2`"
#---------------------------------

job = open(dir_out + '/job', "w")
#--------------------------------
job.write(f'#!/bin/bash \n')
job.write(f'#SBATCH --partition=batch \n')
job.write(f'#SBATCH --job-name=WFlow \n')
job.write(f'#SBATCH --nodes=1 \n')
job.write(f'#SBATCH --ntasks-per-node=32 \n')
job.write(f'#SBATCH --ntasks=32 \n')
job.write(f'#SBATCH --exclusive \n')
job.write(f'#SBATCH -o %x.o%j \n')
job.write(f'#SBATCH -e %x.e%j \n')
job.write(f' \n')
job.write(f'#-------------------------- \n')
job.write(f'dir0=`pwd` \n')
job.write(f'# dir0="{dir_out}" \n')
job.write(f'source {dir_virtual_python} \n')
job.write(f'#-------------------------- \n')
job.write(f' \n')
job.write(f'cd $SLURM_SUBMIT_DIR \n')
job.write(f'ulimit -s unlimited \n')
job.write(f' \n')
job.write(f'# module load ????????????????????python???????????????????? \n')
job.write(f'module load vasp-6.2.0-gcc-9.3.0-epqgvat \n')
job.write(f'vasp_std="{vasp_std}" \n')
job.write(f'vasp_ncl="{vasp_ncl}" \n')
job.write(f' \n') 
job.write(f'ttasks=( "xyz-scan" "xy-scan" "z-scan" "a-scan" "relax" "scf" "bands" "dos" "bader" "scf.SO" "bands.SO" "dos.SO" "bader.SO" ) \n')
job.write(f' \n')
job.write(f'#------------------------ \n')
job.write(f'if [ ! -d "$dir0/completed" ]; then \n')
job.write(f'   mkdir "$dir0/completed" \n')
job.write(f'fi \n')
job.write(f'#------------------------ \n')
job.write(f'folders1=() \n')
job.write(f'for folder in "$dir0"/*; do \n')
job.write(f'    if [ -d "$folder" ] && [ "$(basename "$folder")" != "completed" ]; then \n')
job.write(f'        folders1+=("$(basename "$folder")") \n')
job.write(f'    fi \n')
job.write(f'done \n')
job.write(f'#------------------------ \n')
job.write(f'for i in "{folders1}"; do \n')
job.write(f'    cd $dir0/$i \n')
job.write(f'    mkdir output \n')
job.write(f'    #----------- \n')
job.write(f'    tasks=() \n')
job.write(f'    for j in "{tasks1}"; do \n')
job.write(f'        if [ -d "$dir0/$i/$j" ]; then \n')
job.write(f'           tasks+=("$j") \n')
job.write(f'        fi \n')
job.write(f'    done \n')
job.write(f'    #--------------------- \n')
job.write(f'    for j in "{tasks2}"; do \n')
job.write(f'        if [ -d "$dir0/$i/$j" ]; then \n')
job.write(f'           string1={temp1} \n')
job.write(f'           string2={temp2} \n')
job.write(f'           cd $dir0/$i/$j \n')
job.write(f'           echo "$dir0/$i/$j" >> "$dir0/check_list.txt" \n')
job.write(f'           #===================================================== \n')
job.write(f'           if [[ "$j" == "xyz-scan" || "$j" == "xy-scan" ]]; then \n')
job.write(f'              cd $dir0/$i/$j \n')
job.write(f'              cp POSCAR POSCAR.0 \n')
job.write(f'              python3 contcar_update.py \n')
job.write("              python3 ${j}.py \n")
job.write(f'              #--------------- \n')
job.write(f'              folders2=() \n')
job.write(f'              for folder in $dir0/$i/$j/*; do \n') 
job.write(f'                  if [ -d "$folder" ]; then \n')
job.write(f'                  folders2+=("$(basename "$folder")") \n') 
job.write(f'                  fi \n')
job.write(f'              done \n')
job.write(f'              #------------------------ \n')
job.write(f'              for k in "{folders2}"; do \n')
job.write(f'                  cd $dir0/$i/$j/$k \n')
job.write(f'                  $vasp_std \n')
job.write(f'                  rm -r CHG CHGCAR DOSCAR PROCAR WAVECAR EIGENVAL IBZKPT vasprun.xml \n')
job.write(f'                  python3 contcar_update.py \n')
job.write(f'                  python3 energy_scan.py \n')
job.write(f'                  bzip2 OUTCAR \n')
job.write(f'              done \n')
job.write(f'              #------------- \n')
job.write(f'              cd $dir0/$i/$j \n')
job.write("              python3 ${j}_analysis.py \n")
job.write(f'              #----------------------- \n')
job.write(f'              for k in "{tasks2}"; do \n')
job.write(f'                  #------------------------------ \n')
job.write(f'                  if [ "$j" == "xyz-scan" ]; then \n')
job.write(f'                     if [ "$k" != "xyz-scan" ];  then \n')
job.write(f'                        cp $dir0/$i/$j/POSCAR  $dir0/$i/$k/POSCAR \n')
job.write(f'                        cp $dir0/$i/$j/CONTCAR  $dir0/$i/$k/CONTCAR \n')
job.write(f'                     fi \n')
job.write(f'                  fi \n')
job.write(f'                  cp $dir0/$i/$j/CONTCAR $dir0/$i/output/CONTCAR \n')  
job.write(f'                  cp $dir0/$i/$j/POSCAR $dir0/$i/output/POSCAR \n')
job.write(f'                  #----------------------------- \n')
job.write(f'                  if [ "$j" == "xy-scan" ]; then \n')
job.write(f'                     if [[ "$k" != "xyz-scan" && "$k" != "xy-scan" ]];  then \n')
job.write(f'                        cp $dir0/$i/$j/POSCAR  $dir0/$i/$k/POSCAR \n')
job.write(f'                        cp $dir0/$i/$j/CONTCAR  $dir0/$i/$k/CONTCAR \n')
job.write(f'                     fi \n')
job.write(f'                  fi \n')
job.write(f'                  cp $dir0/$i/$j/CONTCAR $dir0/$i/output/CONTCAR \n')  
job.write(f'                  cp $dir0/$i/$j/POSCAR $dir0/$i/output/POSCAR \n')
job.write(f'                  #------------------------------ \n')
job.write(f'              done \n')
job.write(f'           #==================================================== \n')
job.write(f'           elif [[ "$j" == "z-scan" || "$j" == "a-scan" ]]; then \n')
job.write(f'              cd $dir0/$i/$j \n')
job.write(f'              cp POSCAR POSCAR.0 \n')
job.write(f'              python3 contcar_update.py \n')
job.write("              for p in {1..11}; do \n")
job.write(f'                  echo "$p" > "$dir0/$i/$j/check_steps.txt" \n')
job.write("                  python3 ${j}.py \n")
job.write(f'                  #--------------- \n')
job.write(f'                  folders2=() \n')
job.write(f'                  for folder in $dir0/$i/$j/*; do \n') 
job.write(f'                      if [ -d "$folder" ]; then \n')
job.write(f'                      folders2+=("$(basename "$folder")") \n') 
job.write(f'                      fi \n')
job.write(f'                  done \n')
job.write(f'                  #------------------------ \n')
job.write(f'                  for k in "{folders2}"; do \n')
job.write("                      prefixo=${k:0:3} \n")
job.write(f'                      if [ "$prefixo" != "OK_" ]; then \n')
job.write(f'                         cd $dir0/$i/$j/$k \n')
job.write(f'                         $vasp_std \n')
job.write(f'                         rm -r CHG CHGCAR DOSCAR PROCAR WAVECAR EIGENVAL IBZKPT vasprun.xml \n')
job.write(f'                         python3 contcar_update.py \n')
job.write(f'                         python3 energy_scan.py \n')
job.write(f'                         bzip2 OUTCAR \n')
job.write(f'                         cd $dir0/$i/$j \n')
job.write(f'                         mv $k OK_$k \n')
job.write(f'                      fi \n')
job.write(f'                  done \n')
job.write(f'              done \n')
job.write(f'              #------------- \n')
job.write(f'              cd $dir0/$i/$j \n')
job.write(f'              folders2=() \n')
job.write(f'              for folder in $dir0/$i/$j/*; do \n') 
job.write(f'                  if [ -d "$folder" ]; then \n')
job.write(f'                  folders2+=("$(basename "$folder")") \n') 
job.write(f'                  fi \n')
job.write(f'              done \n')
job.write(f'              for k in "{folders2}"; do \n')
job.write("                  new_name=${k:3} \n")
job.write(f'                  mv "$k" "$new_name" \n')
job.write(f'              done \n')
job.write("              python3 ${j}_analysis.py \n")
job.write(f'              #----------------------- \n')
job.write(f'              for k in "{tasks2}"; do \n')
job.write(f'                  #---------------------------- \n')
job.write(f'                  if [ "$j" == "z-scan" ]; then \n')
job.write(f'                     if [[ "$k" != "xyz-scan" && "$k" != "xy-scan" && "$k" != "z-scan" ]];  then \n')
job.write(f'                        cp $dir0/$i/$j/POSCAR  $dir0/$i/$k/POSCAR \n')
job.write(f'                        cp $dir0/$i/$j/CONTCAR  $dir0/$i/$k/CONTCAR \n')
job.write(f'                     fi \n')
job.write(f'                  fi \n')
job.write(f'                  cp $dir0/$i/$j/CONTCAR $dir0/$i/output/CONTCAR \n')  
job.write(f'                  cp $dir0/$i/$j/POSCAR $dir0/$i/output/POSCAR \n')
job.write(f'                  #---------------------------- \n')
job.write(f'                  if [ "$j" == "a-scan" ]; then \n')
job.write(f'                     if [[ "$k" != "xyz-scan" && "$k" != "xy-scan" && "$k" != "z-scan" && "$k" != "a-scan" ]];  then \n')
job.write(f'                        cp $dir0/$i/$j/POSCAR  $dir0/$i/$k/POSCAR \n')
job.write(f'                        cp $dir0/$i/$j/CONTCAR  $dir0/$i/$k/CONTCAR \n')
job.write(f'                     fi \n')
job.write(f'                  fi \n')
job.write(f'                  cp $dir0/$i/$j/CONTCAR $dir0/$i/output/CONTCAR \n')  
job.write(f'                  cp $dir0/$i/$j/POSCAR $dir0/$i/output/POSCAR \n')   
job.write(f'              done \n')
job.write(f'           #============================= \n')
job.write(f'           elif [ "$j" == "relax" ]; then \n')
job.write(f'              cp POSCAR POSCAR.0 \n')
job.write(f'              mv INCAR INCAR_relax \n')  
job.write(f'              #------------------- \n')         
job.write(f'              mv INCAR_relax_frozen INCAR \n')
job.write(f'              $vasp_std \n')
job.write(f'              mv OSZICAR OSZICAR_frozen \n')
job.write(f'              rm -r CHG CHGCAR DOSCAR PROCAR WAVECAR EIGENVAL IBZKPT vasprun.xml \n')
job.write(f'              mv INCAR INCAR_relax_frozen \n')
job.write(f'              mv OUTCAR OUTCAR_frozen \n')
job.write(f'              #---------------------- \n')
job.write(f'              mv INCAR_relax INCAR \n')
job.write(f'              $vasp_std \n')
job.write(f'              rm -r CHG CHGCAR DOSCAR PROCAR WAVECAR EIGENVAL IBZKPT vasprun.xml \n')
job.write(f'              python3 contcar_update.py \n')
job.write(f'              #------------------------ \n')
job.write(f'              for k in "{tasks2}"; do \n')
job.write(f'                  if [[ "$k" != "xyz-scan" && "$k" != "xy-scan" && "$k" != "z-scan" && "$k" != "a-scan" && "$k" != "relax" ]]; then \n')
job.write(f'                     cp  $dir0/$i/$j/CONTCAR  $dir0/$i/$k/CONTCAR \n')
job.write(f'                     cp  $dir0/$i/$j/CONTCAR  $dir0/$i/$k/POSCAR \n')
job.write(f'                  fi \n')
job.write(f'              done \n')
job.write(f'              bzip2 OUTCAR \n')
job.write(f'              cp  $dir0/$i/$j/CONTCAR  $dir0/$i/output/CONTCAR \n')
job.write(f'              cp  $dir0/$i/$j/CONTCAR  $dir0/$i/output/POSCAR \n')
job.write(f'           #================================= \n')
job.write(f'           elif [ "$string1" == "scf" ]; then \n')
job.write(f'              if [ "$string2" != "SO" ]; then \n')
job.write(f'                 $vasp_std \n')
job.write(f'                 for k in "{tasks2}"; do \n')
job.write(f'                     if [[ "$k" == "bands" || "$k" == "dos" ]]; then \n')
job.write(f'                        cp  $dir0/$i/$j/CHGCAR  $dir0/$i/$k/CHGCAR \n')
job.write(f'                     fi \n')
job.write(f'                 done \n')
job.write(f'              elif [ "$string2" == "SO" ]; then \n')
job.write(f'                 $vasp_ncl \n')
job.write(f'                 for k in "{tasks2}"; do \n')
job.write(f'                     if [[ "$k" == "bands.SO" || "$k" == "dos.SO" ]]; then \n')
job.write(f'                        cp  $dir0/$i/$j/CHGCAR  $dir0/$i/$k/CHGCAR \n')
job.write(f'                     fi \n')
job.write(f'                 done \n')
job.write(f'              fi \n')
job.write(f'              #------------------- \n')
job.write(f'              python3 -m vasprocar \n')
job.write(f'              #------------------- \n')
job.write(f'              rm -r CHG DOSCAR WAVECAR EIGENVAL IBZKPT OSZICAR PCDAT XDATCAR vasprun.xml \n')
job.write(f'              bzip2 CHGCAR OUTCAR PROCAR LOCPOT \n')
job.write(f'              python3 contcar_update.py \n')
job.write(f'              #----------------------------------------------- \n')
job.write(f'              cp  $dir0/$i/$j/CONTCAR  $dir0/$i/output/CONTCAR \n')
job.write(f'              cp  $dir0/$i/$j/POSCAR  $dir0/$i/output/POSCAR \n')
job.write(f'              #------------------------------ \n')
job.write(f'              if [ "$string2" != "SO" ]; then \n')
job.write(f'                 cp  $dir0/$i/$j/output/informacoes.txt  $dir0/$i/output/info_scf.txt \n')
job.write(f'              elif [ "$string2" == "SO" ]; then \n')
job.write(f'                 cp  $dir0/$i/$j/output/informacoes.txt  $dir0/$i/output/info_scf_SO.txt \n')
job.write(f'              fi \n')
job.write(f'           #=================================== \n')
job.write(f'           elif [ "$string1" == "bands" ]; then \n')
job.write(f'              #-------------------------------- \n')
job.write(f'              files=() \n')
job.write(f'              for file in $dir0/$i/$j/*; do \n')
job.write(f'                  if [ -f "$file" ]; then \n')
job.write(f'                     files+=("$(basename "$file")") \n')
job.write(f'                  fi \n')
job.write(f'              done \n')
job.write(f'              #--------------------- \n')
job.write(f'              for k in "{files}"; do \n')
job.write(f'                  string3={temp3} \n')
job.write(f'                  string4={temp4} \n')
job.write(f'                  #----------------------------------- \n')
job.write(f'                  if [ "$string3" == "KPOINTS" ]; then \n')
job.write(f'                     #----------------------------------- \n')
job.write(f'                     if [ "$string4" != "KPOINTS" ]; then \n')
job.write(f'                        mv KPOINTS.$string4 KPOINTS \n')
job.write(f'                     fi \n')
job.write(f'                     #------------------------------ \n')
job.write(f'                     if [ "$string2" != "SO" ]; then \n')
job.write(f'                        $vasp_std \n')
job.write(f'                     elif [ "$string2" == "SO" ]; then \n')
job.write(f'                        $vasp_ncl \n')
job.write(f'                     fi \n')
job.write(f'                     #----------------------------------- \n')
job.write(f'                     rm -r CHG DOSCAR WAVECAR EIGENVAL IBZKPT OSZICAR PCDAT XDATCAR vasprun.xml \n')
job.write(f'                     python3 contcar_update.py \n')
job.write(f'                     #----------------------------------- \n')
job.write(f'                     if [ "$string4" != "KPOINTS" ]; then \n')
job.write(f'                        cp OUTCAR OUTCAR.$string4 \n')
job.write(f'                        mv PROCAR PROCAR.$string4 \n')
job.write(f'                        mv KPOINTS KPOINTS.$string4 \n')
job.write(f'                     fi \n')
job.write(f'                  fi \n')
job.write(f'              done \n')
job.write(f'              #------------------- \n')
job.write(f'              python3 -m vasprocar \n')
job.write(f'              #------------------- \n')
job.write(f'              bzip2 CHGCAR OUTCAR* PROCAR* LOCPOT \n')
job.write(f'              #---------------------------------- \n')
job.write(f'              cp  $dir0/$i/$j/CONTCAR  $dir0/$i/output/CONTCAR \n')
job.write(f'              cp  $dir0/$i/$j/POSCAR  $dir0/$i/output/POSCAR \n')
job.write(f'              #------------------------------ \n')
job.write(f'              if [ "$string2" != "SO" ]; then \n')
job.write(f'                 cp  $dir0/$i/$j/output/informacoes.txt  $dir0/$i/output/info_bands.txt \n')
job.write(f'              elif [ "$string2" == "SO" ]; then \n')
job.write(f'                 cp  $dir0/$i/$j/output/informacoes.txt  $dir0/$i/output/info_bands_SO.txt \n')
job.write(f'              fi \n')
job.write(f'           #================================= \n')
job.write(f'           elif [ "$string1" == "dos" ]; then \n')
job.write(f'              if [ "$string2" != "SO" ]; then \n')
job.write(f'                 $vasp_std \n')
job.write(f'              elif [ "$string2" == "SO" ]; then \n')
job.write(f'                 $vasp_ncl \n')
job.write(f'              fi \n')
job.write(f'              python3 -m vasprocar \n')
job.write(f'              rm -r CHG WAVECAR EIGENVAL IBZKPT OSZICAR PCDAT XDATCAR vasprun.xml \n')
job.write(f'              bzip2 CHGCAR OUTCAR DOSCAR PROCAR \n')
job.write(f'              python3 contcar_update.py \n')
job.write(f'              cp  $dir0/$i/$j/CONTCAR  $dir0/$i/output/CONTCAR \n')
job.write(f'              cp  $dir0/$i/$j/POSCAR  $dir0/$i/output/POSCAR \n')
job.write(f'           #=================================== \n')
job.write(f'           elif [ "$string1" == "bader" ]; then \n')
job.write(f'              python3 bader_update.py \n')
job.write(f'              #---------------------- \n')
job.write(f'              folders2=() \n')
job.write(f'              for folder in $dir0/$i/$j/*; do \n') 
job.write(f'                  if [ -d "$folder" ]; then \n')
job.write(f'                  folders2+=("$(basename "$folder")") \n') 
job.write(f'                  fi \n')
job.write(f'              done \n')
job.write(f'              #------------------------ \n')
job.write(f'              for k in "{folders2}"; do \n')
job.write(f'                  if [ "$k" != "Charge_transfer" ]; then \n')
job.write(f'                     cd $dir0/$i/$j/$k \n')
job.write(f'                     if [ "$string2" != "SO" ]; then \n')
job.write(f'                        $vasp_std \n')
job.write(f'                     elif [ "$string2" == "SO" ]; then \n')
job.write(f'                        $vasp_ncl \n')
job.write(f'                     fi \n')
job.write(f'                     python3 -m vasprocar \n')
job.write(f'                     #------------------- \n')
job.write(f'                     cp -r $dir0/$i/$j/$k/output/Potencial  $dir0/$i/$j/Charge_transfer/Potencial_$k \n')
job.write(f'                     rm -r output \n')                            
job.write(f'                     #------------------ \n')
job.write(f'                     chmod 777 chgsum.pl \n')
job.write(f'                     ./chgsum.pl AECCAR0 AECCAR2 \n')
job.write(f'                     chmod 777 bader \n')
job.write(f'                     # ./bader -vac off CHGCAR -ref CHGCAR_sum \n')
job.write(f'                     ./bader CHGCAR \n')
job.write(f'                     #------------- \n')
job.write(f'                     cp  $dir0/$i/$j/$k/CHGCAR  $dir0/$i/$j/Charge_transfer/CHGCAR_$k \n')
job.write(f'                     rm -r CHG DOSCAR WAVECAR EIGENVAL IBZKPT OSZICAR PCDAT XDATCAR vasprun.xml \n')
job.write(f'                     bzip2 AECCAR* CHGCAR* OUTCAR PROCAR LOCPOT \n')
job.write(f'                  fi \n')
job.write(f'              done \n')
job.write(f'              #------------- \n')
job.write(f'              cd $dir0/$i/$j \n')
job.write(f'              python3 charge_transfer.py \n')
job.write(f'              #----------------------------- \n')
job.write(f'              cd $dir0/$i/$j/Charge_transfer \n')
job.write(f'              python3 -m vasprocar \n')
job.write(f'              cp -r $dir0/$i/$j/Charge_transfer/output/Charge  $dir0/$i/$j/Charge_transfer/Charge_transfer_plot2D \n')
job.write(f'              rm -r output CHGCAR_H* CHGCAR_m* \n')
job.write(f'              rm -r bzip2 CHGCAR_Charge_Transfer.vasp \n')
job.write(f'              #-------------------------------------- \n')
job.write(f'              cd $dir0/$i/$j \n')
job.write(f'              rm -r POSCAR \n')
job.write(f'           #============== \n')
job.write(f'           fi \n')
# job.write(f'        else \n')
# job.write(f'           echo "$dir0/$i/$j: directory missing" >> "$dir0/check_list.txt" \n')
job.write(f'        fi \n')
job.write(f'    done \n')
job.write(f'    cd $dir0/$i \n')
job.write(f'    python3 output.py \n')
job.write(f'    python3 lattice_plot3d.py \n')
job.write(f'    python3 data-base_json.py \n')
job.write(f'    #------------------------ \n')
job.write(f'    if [ ! -d "$dir0/completed" ]; then \n')
job.write(f'       mv $dir0/$i $dir0/completed/$i \n')
job.write(f'    fi \n')
job.write(f'    #------------------------ \n')
job.write(f'done \n')
job.write(f' \n')
job.write(f'deactivate \n')
#--------------------------
job.close()
