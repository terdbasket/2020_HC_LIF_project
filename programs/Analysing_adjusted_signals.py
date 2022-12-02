from programs.function_files.Analysing_adjusted_signals_functions import *

Date = '18_12_2020'
Experiment_type = '1000_1'
adjusted = input('\nAre you analysing adjusted data? y/n: ').lower().replace(' ', '')

if adjusted.lower() == 'y':
    Experiment_type = 'adjusted_'+Experiment_type
else:
    pass

cwd = os.getcwd()
cwd = os.path.dirname(cwd)
figure_path = os.path.join(cwd, 'figures')
path = os.path.join(cwd, 'analysis_files')
path = os.path.join(path, Date)
path = os.path.join(path, Experiment_type)
experiments = os.listdir(path)

number_ramps_in_file_name = 'n'

remove = check_waterfall_plot_for_problems(figure_path, Date, Experiment_type, adjusted)

#Load all the csv files as dic: {exp_name: pandas_DataFrame}
experiments_dic = load_experiment_files_as_dic(path, experiments)
dic_keys = list(experiments_dic.keys())
while True:
    experiments_dic = inspect_and_remove_bad_files(experiments_dic, remove)
    if remove == 'n':
        break
    else:
        pass
    waterfall_plot_dictionary_of_pandas_show(experiments_dic, title='Check for final product')
    good = input('\nAre there any more datasets you would like to remove? y/n: ').lower().replace(' ', '')
    if good == 'n':
        break
    elif good == 'y':
        pass
    else:
        print('User input error. Try again')
        pass

dic_keys = list(experiments_dic.keys())


#Now we join measurements made at the same position
experiments_dic, measurement_positions = join_measurements_at_same_position(experiments_dic)

waterfall_plot_dictionary_of_pandas_show(experiments_dic, label = measurement_positions, title = '{} Experiment at {} mm slit width'.format(Date.replace('_','/'), Experiment_type.replace('_', ' V, ')), legend_title='Measurement position (mm)', legend_loc= 'upper left', xlabel= 'Metastable ion velocity (Km/s)', figsize=(12,8))
figure_path = os.path.join(figure_path, 'combined')
figure_path = os.path.join(figure_path, Date)

figure_name = Date+'_'+Experiment_type

waterfall_plot_dictionary_of_pandas_save(experiments_dic, figure_path, figure_name, label = measurement_positions, title = '{} Experiment at {} mm slit width'.format(Date.replace('_','/'), Experiment_type.replace('_', ' V, ')), legend_title='Measurement position (mm)', legend_loc= 'upper left', xlabel= 'Metastable ion velocity (Km/s)', figsize=(12,8))

path = os.path.dirname(path)
path = os.path.join(path, 'combined')
if adjusted == 'y':
    path = os.path.join(path, 'adjusted')
else:
    path = os.path.join(path, 'original')
if '17_12' in Date:
    Experiment_type = Experiment_type.replace('adjusted_', '')
    path = os.path.join(path, Experiment_type)
else:
    pass

save_experiments_dic_to_csv(experiments_dic, path, measurement_positions)
