from programs.function_files.generally_useful_functions import *
import pandas as pd

def load_experiment_files_as_dic(path, experiments):
    names = []
    for name in experiments:
        names.append(name.replace('.csv','').replace('adjusted_',''))
    experiments_dic = {}
    for i in range(len(experiments)):
        temp = pd.read_csv(os.path.join(path,experiments[i]))
        experiments_dic[names[i]] = temp
    return experiments_dic

def get_densities_normalised_to_bulk_density(experiments_dic):
    keys = list(experiments_dic.keys())
    total_densities = np.asarray([])
    for key in keys:
        column_headers = list(experiments_dic[key].columns.values)
        density_axis = experiments_dic[key][column_headers[0]]
        total_densities = np.append(total_densities, np.sum(density_axis))
    total_densities = total_densities/total_densities[0]
    for i in range(len(keys)):
        keys[i] = float(keys[i])
    return total_densities, keys

def relative_density_plot_show(relative_densities, positions, Experiment_type, filament_discharge, pressure, average_current, adjusted):
    cathode_voltage = Experiment_type.split('_')[0]
    if filament_discharge == 'y':
        filament_discharge = 'Electron filament'
    else:
        filament_discharge = 'Cathode'
    if adjusted == 'y':
        adjusted = 'Power adjusted '
        filament_discharge = filament_discharge.lower()
    else:
        adjusted = ''
    if 'bottom_left' in Experiment_type:
        laser_position = ' (cathode lip)'
    elif 'radial' in Experiment_type:
        laser_position = ' (radial measurement)'
    else:
        laser_position = ''
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.plot(positions, relative_densities, 'x-')
    plt.title('{}{} discharge with {} V, {} mA cathode at {:.2f} {}{}'.format(adjusted, filament_discharge, cathode_voltage, average_current, list(pressure.values())[0], list(pressure.keys())[0], laser_position))
    plt.xlabel('Measurement position (mm)')
    plt.ylabel('Relative density (a.u.)')
    y_lims = ax.get_ylim()
    x_lims = ax.get_xlim()
    new_xlims = [int(x_lims[0]), int(x_lims[1])]
    plt.xlim(new_xlims)
    positions.append(new_xlims[1])
    for i in range(len(relative_densities)):
        plt.axvline(x = positions[i], ymax = (relative_densities[i]-y_lims[0])/(y_lims[1]-y_lims[0]), linestyle = ':', color = 'grey', linewidth = 1)
    plt.xticks(ticks = positions, rotation = 'vertical')
    ax.set_xticks(positions)
    plt.show()
    plt.close(fig)
    return

def relative_density_plot_save(figure_path, figure_name, relative_densities, positions, Experiment_type, filament_discharge, pressure, average_current, adjusted):
    cathode_voltage = Experiment_type.split('_')[0]
    if filament_discharge == 'y':
        filament_discharge = 'Electron filament'
    else:
        filament_discharge = 'Cathode'
    if adjusted == 'y':
        adjusted = 'Power adjusted '
        filament_discharge = filament_discharge.lower()
    else:
        adjusted = ''
    if 'bottom_left' in Experiment_type:
        laser_position = ' (cathode lip)'
    elif 'radial' in Experiment_type:
        laser_position = ' (radial measurement)'
    else:
        laser_position = ''
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    positions.pop()
    ax.plot(positions, relative_densities, 'x-')
    plt.title('{}{} discharge with {} V, {} mA cathode at {:.2f} {}{}'.format(adjusted, filament_discharge, cathode_voltage, average_current, list(pressure.values())[0], list(pressure.keys())[0], laser_position))
    plt.xlabel('Measurement position (mm)')
    plt.ylabel('Relative density (a.u.)')
    y_lims = ax.get_ylim()
    x_lims = ax.get_xlim()
    new_xlims = [int(x_lims[0]), int(x_lims[1])]
    plt.xlim(new_xlims)
    positions.append(new_xlims[1])
    for i in range(len(relative_densities)):
        plt.axvline(x = positions[i], ymax = (relative_densities[i]-y_lims[0])/(y_lims[1]-y_lims[0]), linestyle = ':', color = 'grey', linewidth = 1)
    plt.xticks(ticks = positions, rotation = 'vertical')
    ax.set_xticks(positions)
    plt.savefig(os.path.join(figure_path,figure_name+'.png'))
    plt.close(fig)
    return