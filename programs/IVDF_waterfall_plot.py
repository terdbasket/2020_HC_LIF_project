from programs.function_files.IVDF_waterfall_plot_functions import *

#Load all function files, perhaps as dictionary
#Data_files to use
Date = '15_12_2020'
Experiment_type = '200_1'
combined = 'y'

#Getting location of file names
cwd = os.getcwd()
cwd = os.path.dirname(cwd)
path = os.path.join(cwd, 'analysis_files')
path = os.path.join(path, Date)
path = os.path.join(path, Experiment_type) if combined == 'n' else path
if combined == 'y':
    path = os.path.join(path, 'combined')
    path = os.path.join(path, 'adjusted')
experiments = os.listdir(path)

number_ramps_in_file_name = 'n'


#Load all the csv files as dic: {exp_name: pandas_DataFrame}
experiments_dic = load_experiment_files_as_dic(path, experiments)
dic_keys = list(experiments_dic.keys())

column_headers = list(experiments_dic[dic_keys[0]].columns.values)

measurement_positions, centre_offsets, no_ramps = get_experiment_parameters(experiments)

waterfall_plot_dictionary_of_pandas_show(experiments_dic, figsize = (12,8), label = measurement_positions, legend_title='position', legend_loc='upper left', xlabel= 'Metastable ion velocity (Km/s)', title='{} {} waterfall plot'.format(Date.replace('_','/'), Experiment_type))

figure_path = os.path.join(cwd,'figures')
figure_path = os.path.join(figure_path, Date)

waterfall_plot_dictionary_of_pandas_save(experiments_dic, figure_path, Date+'_'+Experiment_type, figsize = (12,8), label = measurement_positions, legend_title='position', legend_loc='upper left', xlabel= 'Metastable ion velocity (Km/s)', title='{} {} waterfall plot'.format(Date.replace('_','/'), Experiment_type))
