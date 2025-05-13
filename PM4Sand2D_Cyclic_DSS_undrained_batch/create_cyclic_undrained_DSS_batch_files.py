#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday Feb1 08:03:57 2024
@author: kziot

- File opens Template with header line info, writes parametrically varying 
  parameters underneath, writes complete contents of DSS_cyclic_undrained.f2fis file
  sets savefile information (for *.sav in running FLAC) and closes it
- Each produced *.f2fis file is named according to the varied parameters
- a batch_undrainedDSS_cyc***.fis is produced populated by call commands for each file
  generated for later being called in FLAC2D
- As of now, placeholders for relative density, overburden stress, static shear
  stress bias, and Ko (can be provided with 1 or more array values)
- all other variables are defined inside DSS_cyclic_undrained.f2fis and can be either
  changed within (if constant across all drivers) or brought herein to be added as 
  another array to be iterated over... following the same philosophy
- only the batch_undrainedDSS_cyc***.f2fis file needs to be called by FLAC2D
- CAUTION: file naming conventions intimately related to post-processing & plotting protocols
"""
import os
# Get absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
#------------------------------------------------------------------------------
# Input Parameters - Example
#------------------------------------------------------------------------------
Soil     = ""        # empty now -- populate if more specific
TestName = "uDSS"    # will match template and Driver and built upon that

# Create arrays of values to be varied across all Drivers
# Produced files will be named accordingly

Dr       = [0.35, 0.55, 0.75]         # Relative Density
sig_vc   = [1,4,8]                    # initial overburden stress
alpha   = [0.0,0.1,0.2,0.3]          # static shear stress bias ratio
#alpha    = [0.0]                      # static shear stress bias ratio
Ko       = [0.3,0.8,1.2]              # coefficient of lateral earth pressures at rest
#Ko      = [0.5]                      # coefficient of lateral earth pressures at rest

Test_File     = os.path.join(script_dir, "DSS_cyclic_undrained.f2fis")
Template_File = os.path.join(script_dir, "templ_uDSScyc.f2fis")

# Initialize lines for final batch file
call_line   = 'program call \'#\'\n'
batch_lines = []

for Dr_i in Dr:
    for sig_vc_i in sig_vc:
        for alpha_i in alpha:
            for Ko_i in Ko:
                # First create a file name 
                
                if alpha_i == 0.0:
                    FirstCallFlag = 0
                else:
                    FirstCallFlag = 1

                BaseFile = TestName + Soil+"_cyc"+"_Dr"+str(int(Dr_i*100))+"_sig"+str(sig_vc_i)+"_a"+str(alpha_i)+"_Ko"+str(Ko_i)
                FileName = os.path.join(script_dir, BaseFile + ".f2fis")

                # Create a new file and open template and test file
                fileID 			= open(FileName,"w+");
                Template_fileId = open(Template_File,"r");
                Test_fileId     = open(Test_File,"r")

                # Writing to a file
                fileID.write(Template_fileId.read())
                fileID.write("\n\n")

                fileID.write(";------------GENERAL INPUT CONDITIONS------------\n")
                fileID.write("fish def $var_inputs\n")
                fileID.write("\t$Dr          = " + str(Dr_i) + " \n")
                fileID.write("\t$static_bias = " + str(alpha_i) + " \n")
                fileID.write("\t$flag_on_FirstCall = " + str(FirstCallFlag) + " \n")
                fileID.write("\t$confinement = " + str(sig_vc_i) + " \n")
                fileID.write("\t$Ko          = " + str(Ko_i) + " \n")
                fileID.write("\t$basefile    = \'" + BaseFile + "\' \n")
                fileID.write("end \n");
                fileID.write("[$var_inputs]\n\n")

                fileID.write(Test_fileId.read())

                fileID.write(";-------------Footer-------------------\n")
                fileID.write(";save @$savefile\n")
                fileID.write(";--------------------------------------\n")

                # Closing the files
                Test_fileId.close()
                Template_fileId.close()
                fileID.close()
                batch_lines.append(call_line.replace("#", FileName))

batch_file_path = os.path.join(script_dir, "batch_undrainedDSS_cyc.f2fis")
batch_file = open(batch_file_path, "w")

batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write(";                     FLAC batch calling of input files                 \n")
batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write("\n")
batch_file.writelines(batch_lines)
batch_file.close()
''' EoF'''
