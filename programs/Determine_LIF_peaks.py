from programs.function_files.Determine_LIF_peaks_functions import *

#This is a program that takes LIF signals and gives you a relative density plot against measurement position.

#Load all function files, perhaps as dictionary
#Data_files to use
Date = '18_12_2020'
Experiment_type = '1000_1'

adjusted = input('\nAre you analysing adjusted data files? y/n: ').lower().replace(' ', '')

#Getting location of file names
cwd = os.getcwd()
cwd = os.path.dirname(cwd)
path = os.path.join(cwd, 'analysis_files')
path = os.path.join(path, Date)
path = os.path.join(path, 'combined')
if adjusted == 'y':
    path = os.path.join(path, 'adjusted')
else:
    path = os.path.join(path, 'original')
if '17_12' in Date:
    path = os.path.join(path, Experiment_type)
else:
    pass
experiments = os.listdir(path)

experiments_dic = load_experiment_files_as_dic(path, experiments)
dic_keys = list(experiments_dic.keys())

Sig_to_noise = 3
analysis_dic = find_region_of_signal_above_threshold(experiments_dic, Sig_to_noise)

path = os.path.dirname(path)
path = os.path.dirname(path)
if '17_12' in Date: #An extra folder deep if in this case
    path = os.path.dirname(path)
else:
    pass
path = os.path.join(path, 'selected_peaks')
if adjusted == 'y':
    path = os.path.join(path, 'adjusted')
else:
    path = os.path.join(path, 'original')
if '17_12' in Date:
    path = os.path.join(path, Experiment_type)
else:
    pass
filenames = list(analysis_dic.keys())
save_experiments_dic_to_csv(analysis_dic, path, filenames)