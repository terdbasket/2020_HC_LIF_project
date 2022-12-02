from programs.function_files.Relative_density_plot_functions import *

#Load all function files, perhaps as dictionary
#Data_files to use
Date = '18_12_2020'
Experiment_type = '1000_1'

#Lab note important files
filament_discharge = 'n' #Were the electron filaments used in the discharge?
pressure_mBarr = {'mBarr': 5e-2}
pressure_mTorr = {'mTorr': list(pressure_mBarr.values())[0]/0.0013332237}
average_current = 7 #mA

adjusted = input('\nAre you analysing adjusted data files? y/n: ').lower().replace(' ', '')

#Getting location of file names
cwd = os.getcwd()
cwd = os.path.dirname(cwd)
figure_path = os.path.join(cwd, 'figures')
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

relative_densities, positions = get_densities_normalised_to_bulk_density(experiments_dic)

dist_positions = np.abs(np.asarray(positions)-150)/10.0 #JUST FOR ABSTRACT FOR FLTPD2022

relative_density_plot_show(relative_densities, positions, Experiment_type, filament_discharge, pressure_mTorr, average_current, adjusted)

figure_path = os.path.join(figure_path, Date)
if adjusted == 'y':
    Experiment_type = 'adjusted_'+Experiment_type
else:
    pass
figure_name = Date+'_'+Experiment_type+'relative_density'

relative_density_plot_save(figure_path, figure_name, relative_densities, positions, Experiment_type, filament_discharge, pressure_mTorr, average_current, adjusted)

plt.plot(dist_positions, relative_densities, 'kx-', markersize = 8)
plt.xlabel('Axial distance from cathode edge (cm)', fontsize = 14)
plt.ylabel('Relative density (Arb. Units)', fontsize = 14)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.title('Hollow Cathode ArII $3\mathregular{d} ^2\mathregular{G}_{9/2}$ Density', fontsize = 14)
plt.xlim((max(dist_positions)+0.1, 0))
plt.show()

