import csv
import numpy as np
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pandas as pd
from itertools import cycle
from programs.function_files.generally_useful_functions import *

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
            centre_offsets.append(broken_name[1])
        if number_ramps_in_file_name == 'y':
            no_ramps.append(float(name[2]))
        else:
            pass
    return measurement_positions, centre_offsets, no_ramps

def show_3D_plot_equal_spacing(measurement_positions, experiments_dic, arb_positions, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, **orientation):

    if len(orientation) == 0:
        elevation = 90
        azimuthal_angle = -90
    else:
        keys = list(orientation.keys())
        elevation = orientation[keys[0]]
        azimuthal_angle = orientation[keys[1]]

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(figsize = (12,8))
    ax = fig.gca(projection='3d')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    for i in range(len(measurement_positions)):
        lockin_signal_average = np.array(experiments_dic[dic_keys[i]][column_headers[0]])
        velocity_axis = np.array(experiments_dic[dic_keys[i]][column_headers[1]])
        if centre_offsets[i] != normal_centre_offset:  # If IVDF not centered at zero
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                    color=next(colours), zdir='z')
            ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        else:
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.title(Date.replace('_', '/') + ' ' + Experiment_type.replace('_', ' V, ') + ' mm slit width')
    plt.xlabel('ion velocity (km/s)')
    plt.ylabel('Relative amplitude (a.u.)')
    ax.view_init(elev=elevation, azim=azimuthal_angle)
    ax.set_zticklabels([])
    close_figure_with_keyboard_or_mouse()
    plt.close(fig)
    return


def show_3D_plot_actual_spacing(measurement_positions, experiments_dic, centre_offsets, dic_keys,
                               column_headers, normal_centre_offset, Date, Experiment_type, **orientation):
    if len(orientation) == 0:
        elevation = 90
        azimuthal_angle = -90
    else:
        keys = list(orientation.keys())
        elevation = orientation[keys[0]]
        azimuthal_angle = orientation[keys[1]]

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(figsize = (12,8))
    ax = fig.gca(projection='3d')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    for i in range(len(measurement_positions)):
        lockin_signal_average = np.array(experiments_dic[dic_keys[i]][column_headers[0]])
        velocity_axis = np.array(experiments_dic[dic_keys[i]][column_headers[1]])
        if centre_offsets[i] != normal_centre_offset:  # If IVDF not centered at zero
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, measurement_positions[i],
                    label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                    color=next(colours), zdir='z')
            ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        else:
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, measurement_positions[i],
                    label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.title(Date.replace('_', '/') + ' ' + Experiment_type.replace('_', ' V, ') + ' mm slit width')
    plt.xlabel('ion velocity (km/s)')
    plt.ylabel('Relative amplitude (a.u.)')
    ax.view_init(elev=elevation, azim=azimuthal_angle)
    close_figure_with_keyboard_or_mouse()
    plt.close(fig)
    return

def show_3D_subplots(measurement_positions,experiments_dic,arb_positions, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, spacing_type, **orientation):
    if len(orientation) == 0:
        elevation = 90
        azimuthal_angle = -90
    else:
        keys = list(orientation.keys())
        elevation = orientation[keys[0]]
        azimuthal_angle = orientation[keys[1]]
    fig = plt.figure(figsize=(15,7))
    mpl.rcParams['legend.fontsize'] = 10
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    for i in range(len(measurement_positions)):
        lockin_signal_average = np.array(experiments_dic[dic_keys[i]][column_headers[0]])
        velocity_axis = np.array(experiments_dic[dic_keys[i]][column_headers[1]])
        if centre_offsets[i] != normal_centre_offset:  # If IVDF not centered at zero
            if spacing_type.lower() == 'equal':
                ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                        label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                        color=next(colours), zdir='z')
            elif spacing_type.lower() == 'actual':
                ax.plot(velocity_axis / 1000.0, lockin_signal_average, measurement_positions[i],
                        label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                        color=next(colours), zdir='z')
            else:
                print("Enter spacing_type as either 'equal' or 'actual.")
                sys.exit()
        else:
            if spacing_type.lower() == 'equal':
                ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            elif spacing_type.lower() == 'actual':
                ax.plot(velocity_axis / 1000.0, lockin_signal_average, measurement_positions[i],
                        label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            else:
                print("Enter spacing_type as either 'equal' or 'actual.")
                sys.exit()
    plt.title(Date.replace('_', '/') + ' ' + Experiment_type.replace('_', ' V, ') + ' mm slit width')
    plt.xlabel('ion velocity (km/s)')
    plt.ylabel('Relative amplitude (a.u.)')
    ax.view_init(elev=elevation, azim=azimuthal_angle)
    ax.set_zticklabels([])

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    for i in range(len(measurement_positions)):
        lockin_signal_average = np.array(experiments_dic[dic_keys[i]][column_headers[0]])
        velocity_axis = np.array(experiments_dic[dic_keys[i]][column_headers[1]])
        if centre_offsets[i] != normal_centre_offset:  # If IVDF not centered at zero
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                    color=next(colours), zdir='z')
            ax.legend(loc='upper right', bbox_to_anchor=(0.18, 1))
        else:
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            ax.legend(loc='upper right', bbox_to_anchor=(0.18, 1))
    plt.title(Date.replace('_', '/') + ' ' + Experiment_type.replace('_', ' V, ') + ' mm slit width')
    plt.xlabel('ion velocity (km/s)')
    plt.ylabel('Relative amplitude (a.u.)')
    ax.view_init(elev=elevation+30, azim=azimuthal_angle)
    if spacing_type.lower() == 'actual':
        pass
    else:
        ax.set_zticklabels([])
    plt.suptitle('Two angles of same dataset')
    close_figure_with_keyboard_or_mouse()
    plt.close(fig)
    return

def save_3D_plot_equal_spacing(measurement_positions, experiments_dic, arb_positions, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, figure_path, **orientation):
    fig_name = Date + '_' + Experiment_type + '_all_results_equal_spacing.png'
    if len(orientation) == 0:
        elevation = 90
        azimuthal_angle = -90
    else:
        keys = list(orientation.keys())
        elevation = orientation[keys[0]]
        azimuthal_angle = orientation[keys[1]]

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(figsize = (12,8))
    ax = fig.gca(projection='3d')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    for i in range(len(measurement_positions)):
        lockin_signal_average = np.array(experiments_dic[dic_keys[i]][column_headers[0]])
        velocity_axis = np.array(experiments_dic[dic_keys[i]][column_headers[1]])
        if centre_offsets[i] != normal_centre_offset:  # If IVDF not centered at zero
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                    color=next(colours), zdir='z')
            ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        else:
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.title(Date.replace('_', '/') + ' ' + Experiment_type.replace('_', ' V, ') + ' mm slit width')
    plt.xlabel('ion velocity (km/s)')
    plt.ylabel('Relative amplitude (a.u.)')
    ax.view_init(elev=elevation, azim=azimuthal_angle)
    ax.set_zticklabels([])
    plt.savefig(os.path.join(figure_path, fig_name))
    plt.close(fig)
    return

def save_3D_plot_actual_spacing(measurement_positions, experiments_dic, centre_offsets, dic_keys,
                               column_headers, normal_centre_offset, Date, Experiment_type, figure_path, **orientation):
    if len(orientation) == 0:
        elevation = 90
        azimuthal_angle = -90
    else:
        keys = list(orientation.keys())
        elevation = orientation[keys[0]]
        azimuthal_angle = orientation[keys[1]]
    fig_name = Date + '_' + Experiment_type + '_all_results_actual_spacing.png'
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(figsize = (12,8))
    ax = fig.gca(projection='3d')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    for i in range(len(measurement_positions)):
        lockin_signal_average = np.array(experiments_dic[dic_keys[i]][column_headers[0]])
        velocity_axis = np.array(experiments_dic[dic_keys[i]][column_headers[1]])
        if centre_offsets[i] != normal_centre_offset:  # If IVDF not centered at zero
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, measurement_positions[i],
                    label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                    color=next(colours), zdir='z')
            ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        else:
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, measurement_positions[i],
                    label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.title(Date.replace('_', '/') + ' ' + Experiment_type.replace('_', ' V, ') + ' mm slit width')
    plt.xlabel('ion velocity (km/s)')
    plt.ylabel('Relative amplitude (a.u.)')
    ax.view_init(elev=elevation, azim=azimuthal_angle)
    plt.savefig(os.path.join(figure_path, fig_name))
    plt.close(fig)
    return

def save_3D_subplots(measurement_positions,experiments_dic,arb_positions, centre_offsets, dic_keys, column_headers, normal_centre_offset, Date, Experiment_type, spacing_type, figure_path, **orientation):
    fig_name = 'subplot_'+Date + '_' + Experiment_type + '_all_results_{}_spacing.png'.format(spacing_type)
    if len(orientation) == 0:
        elevation = 90
        azimuthal_angle = -90
    else:
        keys = list(orientation.keys())
        elevation = orientation[keys[0]]
        azimuthal_angle = orientation[keys[1]]
    fig = plt.figure(figsize=(15,7))
    mpl.rcParams['legend.fontsize'] = 10
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    for i in range(len(measurement_positions)):
        lockin_signal_average = np.array(experiments_dic[dic_keys[i]][column_headers[0]])
        velocity_axis = np.array(experiments_dic[dic_keys[i]][column_headers[1]])
        if centre_offsets[i] != normal_centre_offset:  # If IVDF not centered at zero
            if spacing_type.lower() == 'equal':
                ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                        label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                        color=next(colours), zdir='z')
            elif spacing_type.lower() == 'actual':
                ax.plot(velocity_axis / 1000.0, lockin_signal_average, measurement_positions[i],
                        label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                        color=next(colours), zdir='z')
            else:
                print("Enter spacing_type as either 'equal' or 'actual.")
                sys.exit()
        else:
            if spacing_type.lower() == 'equal':
                ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            elif spacing_type.lower() == 'actual':
                ax.plot(velocity_axis / 1000.0, lockin_signal_average, measurement_positions[i],
                        label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            else:
                print("Enter spacing_type as either 'equal' or 'actual.")
                sys.exit()
    plt.title(Date.replace('_', '/') + ' ' + Experiment_type.replace('_', ' V, ') + ' mm slit width')
    plt.xlabel('ion velocity (km/s)')
    plt.ylabel('Relative amplitude (a.u.)')
    ax.view_init(elev=elevation, azim=azimuthal_angle)
    ax.set_zticklabels([])

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    for i in range(len(measurement_positions)):
        lockin_signal_average = np.array(experiments_dic[dic_keys[i]][column_headers[0]])
        velocity_axis = np.array(experiments_dic[dic_keys[i]][column_headers[1]])
        if centre_offsets[i] != normal_centre_offset:  # If IVDF not centered at zero
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm, ' + str(centre_offsets[i]) + ' offset',
                    color=next(colours), zdir='z')
            ax.legend(loc='upper right', bbox_to_anchor=(0.18, 1))
        else:
            ax.plot(velocity_axis / 1000.0, lockin_signal_average, arb_positions[i],
                    label=str(measurement_positions[i]) + ' mm', color=next(colours), zdir='z')
            ax.legend(loc='upper right', bbox_to_anchor=(0.18, 1))
    plt.title(Date.replace('_', '/') + ' ' + Experiment_type.replace('_', ' V, ') + ' mm slit width')
    plt.xlabel('ion velocity (km/s)')
    plt.ylabel('Relative amplitude (a.u.)')
    ax.view_init(elev=elevation+30, azim=azimuthal_angle)
    if spacing_type.lower() == 'actual':
        pass
    else:
        ax.set_zticklabels([])
    plt.suptitle('Two angles of same dataset')
    plt.savefig(os.path.join(figure_path, fig_name))
    plt.close(fig)
    return