from programs.function_files.IVDF_3D_plotter_functions import *


#Data_files to use
Date = '18_12_2020'
Experiment_type = '1000_1'
normal_centre_offset = 0.0

#Getting location of file names
cwd = os.getcwd()
cwd = os.path.dirname(cwd)
path = os.path.join(cwd, 'analysis_files')
path = os.path.join(path, Date)
path = os.path.join(path, Experiment_type)
experiments = os.listdir(path)

number_ramps_in_file_name = 'y'


#Load all the csv files as dic: {exp_name: pandas_DataFrame}
experiments_dic = load_experiment_files_as_dic(path, experiments)

arb_positions = np.linspace(1,len(experiments),len(experiments))


dic_keys = list(experiments_dic.keys())

column_headers = list(experiments_dic[dic_keys[0]].columns.values)

measurement_positions, centre_offsets, no_ramps = get_experiment_parameters(experiments)

figure_path = os.path.join(cwd,'figures')
figure_path = os.path.join(figure_path, Date)

#To show the figure
elev = 120
azim = -90


show_3D_plot_equal_spacing(measurement_positions, experiments_dic, arb_positions, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, elevation = elev, azimuthal_angle = azim)

show_3D_plot_actual_spacing(measurement_positions, experiments_dic, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, elevation = elev, azimuthal_angle = azim)

show_3D_subplots(measurement_positions, experiments_dic, arb_positions,centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, 'equal')

save_3D_plot_equal_spacing(measurement_positions, experiments_dic, arb_positions, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, figure_path, elevation = elev, azimuthal_angle = azim)

save_3D_plot_actual_spacing(measurement_positions, experiments_dic, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, figure_path, elevation = elev, azimuthal_angle = azim)

save_3D_subplots(measurement_positions, experiments_dic, arb_positions, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, 'equal', figure_path)