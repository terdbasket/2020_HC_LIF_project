from programs.function_files.generally_useful_functions import *
import os
import sys
import pandas as pd

def load_experiment_files_as_dic(path, experiments):
    names = []
    for name in experiments:
        names.append(name.replace('.csv',''))
    experiments_dic = {}
    for i in range(len(experiments)):
        temp = pd.read_csv(os.path.join(path,experiments[i]))
        experiments_dic[names[i]] = temp
    return experiments_dic

def get_experiment_parameters(experiments, *number_ramps_in_file_name):
    measurement_positions = []
    centre_offsets = []
    no_ramps = []
    for name in experiments:
        broken_name = name.replace('csv','').split('_')
        if 'adjusted' in broken_name:
            measurement_positions.append(float(broken_name[1]))
        else:
            measurement_positions.append(float(broken_name[0]))
        if 'ghz' in name.lower():
            if 'left' in name.lower():
                centre_offsets.append('Left')
            elif 'right' in name.lower():
                centre_offsets.append('Right')
            elif 'radial' in name.lower():
                centre_offsets.append('Radial')
            else:
                print('\nProblem in file names: Centre offset')
                sys.exit()
        else:
            if 'adjusted' in broken_name:
                centre_offsets.append(broken_name[2])
            else:
                centre_offsets.append(broken_name[1])
        if number_ramps_in_file_name == 'y':
            no_ramps.append(float(name[2]))
        else:
            pass
    return measurement_positions, centre_offsets, no_ramps

def get_max_lockin_value(experiments_dic, dick_keys, column_headers):
    max_vals = []
    for i in range(len(experiments_dic)):
        max_vals.append(max(experiments_dic[dick_keys[i]][column_headers[0]])) #Get max of each experiment
    max_tot = max(max_vals)
    return max_vals, max_tot

