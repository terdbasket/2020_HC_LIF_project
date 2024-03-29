import matplotlib
import numpy as np

from programs.function_files.Relative_density_plot_functions import *

#Load all function files, perhaps as dictionary
#Data_files to use
Date = '18_12_2020'
Experiment_type = '1000_1'
Voltage = '-1000'
Pressure = '37'
laser_position = 'cax'
if laser_position == 'cax':
    title_position = 'Centre Axis'
elif laser_position == 'bax':
    title_position = 'Bottom Axis'
elif laser_position == 'rad':
    title_position = 'Radial'
title_position += ', Self Sust.' if Date == '18_12_2020' else ''
combined = 'y'

if Date == '15_12_2020':
    Exp_no = 1
    cathode_lip = 161
    spacing_val = 0.4
elif Date == '16_12_2020':
    Exp_no = 2
    cathode_lip = 161
    spacing_val = 0.4
elif Date == '18_12_2020':
    Exp_no = 3
    cathode_lip = 159
    spacing_val = 0.1
elif Date == '17_12_2020':
    Exp_no = 4
    cathode_lip = 159
    spacing_val = 0.4

linestyles = ['solid']*20

#Getting location of file names
cwd = os.getcwd()
cwd = os.path.dirname(cwd)
path = os.path.join(cwd, 'analysis_files')
path = os.path.join(path, Date)
path = os.path.join(path, Experiment_type) if combined == 'n' else path
if combined == 'y':
    path = os.path.join(path, 'combined')
    path = os.path.join(path, 'adjusted')
if Date == '17_12_2020':
    if laser_position == 'cax':
        path = os.path.join(path, Experiment_type)
    elif laser_position == 'bax':
        path = os.path.join(path, Experiment_type+'_bottom_left')
    else:
        path = os.path.join(path, Experiment_type + '_radial')
experiments = os.listdir(path)

number_ramps_in_file_name = 'n'

print(path)
#Load all the csv files as dic: {exp_name: pandas_DataFrame}
experiments_dic = load_experiment_files_as_dic(path, experiments)
dic_keys = list(experiments_dic.keys())
nerds, positions = get_densities_normalised_to_bulk_density(experiments_dic)
dist_positions = np.abs(np.asarray(positions)-cathode_lip)

x_axis_list, y_axis_list = [],[]
for key in dic_keys:
    df = experiments_dic[key]
    column_headers = list(experiments_dic[dic_keys[0]].columns.values)
    x_axis_list.append(np.asarray(df[column_headers[1]]))
    y_axis_list.append(np.asarray(df[column_headers[0]]))

plasma_velocity = x_axis_list[0][find_nearest_index_in_array(y_axis_list[0], max(y_axis_list[0]))]
# plasma_frequency =
#
print('\nThe peak velocity in the plasma bulk is {:.3f} km/s, corresponding to a frequency of {:.3e}'.format(plasma_velocity*1e-3, 0))

color_values = np.linspace(0,0.75,len(dic_keys))
color_map = matplotlib.cm.get_cmap('CMRmap')
colours, spacing = [], []
spacing_start = 0
for value in color_values:
    colours.append(color_map(value))
    spacing.append(spacing_start)
    spacing_start+=spacing_val

ylimlist = []

for i in range(len(dic_keys)):
    for j in range(len(y_axis_list[i])):
        ylimlist.append(y_axis_list[i][j]+spacing[i])

fig, ax = plt.subplots(figsize = (6,6))

lw = 1.25
axis_fs = 14
title_fs = axis_fs+1
for i in range(len(dic_keys)):
    ax.plot(x_axis_list[i]*1e-3, y_axis_list[i]+spacing[i], color = colours[i], linestyle = linestyles[i], linewidth = lw, label = '{:.0f}'.format(dist_positions[i]))
    ax.text(-16 if x_axis_list[i][0] <-10e3 else -10, (np.mean(y_axis_list[i][:50] + spacing[i])), '{:.0f}'.format(dist_positions[i]))
ax.set_xlabel('Ion Velocity (km/s)', fontsize = axis_fs)
ax.set_ylabel('Signal Intensity (arb.)', fontsize = axis_fs)
ax.set_xlim(-17.5, 25)
ax.set_ylim(0, max(ylimlist)+0.1)
ax.set_title('Exp. {}, {} mTorr, {} V, {}'.format(Exp_no, Pressure, Voltage, title_position), fontsize = title_fs)
ax.axvline(x=plasma_velocity*1e-3, color = 'black', linestyle = 'dotted', alpha = 0.5)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], loc = 'lower right', fontsize = 'medium', framealpha = 0.75, handlelength=2, borderpad = 0.2, title = 'Axial Dist. (mm)', title_fontsize = 'medium', labelspacing = 0.2)

fig.tight_layout()
figure_path = os.path.join(os.path.dirname(os.getcwd()), 'figures', 'paper_figures')
plt.savefig(os.path.join(figure_path, 'IVDF_plot_{}_{}.eps'.format(Date[:5], laser_position)), format = 'eps')
plt.savefig(os.path.join(figure_path, 'IVDF_plot_{}_{}.png'.format(Date[:5], laser_position)), format = 'png')

plt.show()
plt.close()