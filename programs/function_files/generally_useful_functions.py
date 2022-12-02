import _tkinter
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import os
import timeit
import sys

def find_nearest_index_in_array(array, value):
    array = np.asarray(array)
    index = (np.abs(array-value)).argmin()
    return index

def get_pandas_indexes(dfObj, value):
    ''' Get index positions of value in dataframe i.e. dfObj.'''
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos

def close_figure_with_keyboard_or_mouse():
    try:
        plt.waitforbuttonpress()
    except _tkinter.TclError:
        pass
    return

def waterfall_plot_dictionary_of_pandas_show(dic_of_pandas, **kwargs):
    kwarg_keys = kwargs.keys()
    dic_keys = list(dic_of_pandas.keys())
    column_headers = list(dic_of_pandas[dic_keys[0]].columns.values)
    max_vals = []

    for i in range(len(dic_of_pandas)):
        max_vals.append(max(dic_of_pandas[dic_keys[i]][column_headers[0]]))
    max_tot = max(max_vals)

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])

    if 'figsize' in kwarg_keys:
        fig = plt.figure(figsize = kwargs['figsize'])
    else:
        fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    for i in range(len(dic_of_pandas)):
        spacing = (2*float(len(dic_of_pandas)-i-1)/float(len(dic_of_pandas)))*max_tot
        x_axis = np.array(dic_of_pandas[dic_keys[-i-1]][column_headers[1]])/1000.0
        y_axis = np.array(dic_of_pandas[dic_keys[-i-1]][column_headers[0]])+spacing
        if 'linestyle' in kwarg_keys:
            if 'label' in kwarg_keys:
                ax.plot(x_axis, y_axis, color = next(colours), linestyle = kwargs['linestyle'], label = kwargs['label'][i])
            else:
                ax.plot(x_axis, y_axis, color=next(colours), linestyle=kwargs['linestyle'])
        else:
            if 'label' in kwarg_keys:
                ax.plot(x_axis, y_axis, color = next(colours), label = kwargs['label'][i])
            else:
                ax.plot(x_axis, y_axis, color = next(colours))
    if 'label' in kwarg_keys:
        handles, labels = ax.get_legend_handles_labels()
        if 'legend_title' in kwarg_keys:
            if 'legend_loc' in kwarg_keys:
                ax.legend(handles, labels[::-1], title = kwargs['legend_title'], loc = kwargs['legend_loc'])
            else:
                ax.legend(handles, labels[::-1], title=kwargs['legend_title'])
        else:
            if 'legend_loc' in kwarg_keys:
                ax.legend(handles, labels[::-1], loc=kwargs['legend_loc'])
            else:
                ax.legend(handles, labels[::-1])
    else:
        pass
    if 'xlabel' in kwarg_keys:
        plt.xlabel(kwargs['xlabel'])
    else:
        pass
    if 'title' in kwarg_keys:
        plt.title(kwargs['title'])
    else:
        pass
    close_figure_with_keyboard_or_mouse()
    plt.close(fig)
    return

def waterfall_plot_dictionary_of_pandas_save(dic_of_pandas, save_path, save_name, **kwargs):
    kwarg_keys = kwargs.keys()
    dic_keys = list(dic_of_pandas.keys())
    column_headers = list(dic_of_pandas[dic_keys[0]].columns.values)
    max_vals = []

    for i in range(len(dic_of_pandas)):
        max_vals.append(max(dic_of_pandas[dic_keys[i]][column_headers[0]]))
    max_tot = max(max_vals)

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])

    if 'figsize' in kwarg_keys:
        fig = plt.figure(figsize = kwargs['figsize'])
    else:
        fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    for i in range(len(dic_of_pandas)):
        spacing = (2*float(len(dic_of_pandas)-i-1)/float(len(dic_of_pandas)))*max_tot
        x_axis = np.array(dic_of_pandas[dic_keys[-i-1]][column_headers[1]])/1000.0
        y_axis = np.array(dic_of_pandas[dic_keys[-i-1]][column_headers[0]])+spacing
        if 'linestyle' in kwarg_keys:
            if 'label' in kwarg_keys:
                ax.plot(x_axis, y_axis, color = next(colours), linestyle = kwargs['linestyle'], label = kwargs['label'][i])
            else:
                ax.plot(x_axis, y_axis, color = next(colours), linestyle=kwargs['linestyle'])
        else:
            if 'label' in kwarg_keys:
                ax.plot(x_axis, y_axis, color = next(colours), label = kwargs['label'][i])
            else:
                ax.plot(x_axis, y_axis, color = next(colours))
    if 'label' in kwarg_keys:
        handles, labels = ax.get_legend_handles_labels()
        if 'legend_title' in kwarg_keys:
            if 'legend_loc' in kwarg_keys:
                ax.legend(handles, labels[::-1], title = kwargs['legend_title'], loc = kwargs['legend_loc'])
            else:
                ax.legend(handles, labels[::-1], title=kwargs['legend_title'])
        else:
            if 'legend_loc' in kwarg_keys:
                ax.legend(handles, labels[::-1], loc=kwargs['legend_loc'])
            else:
                ax.legend(handles, labels[::-1])
    else:
        pass
    if 'xlabel' in kwarg_keys:
        plt.xlabel(kwargs['xlabel'])
    else:
        pass
    if 'title' in kwarg_keys:
        plt.title(kwargs['title'])
    else:
        pass
    plt.savefig(os.path.join(save_path, save_name)+'_waterfall_plot.png')
    plt.close(fig)
    return

def n_point_array_smooth(data, n, *print_values):
    new_array = []
    if print_values == 'y':
        print('\nSmoothing array of length {} with {} point average'.format(len(data), n))
    else:
        pass
    start = timeit.default_timer()
    for i in range(len(data)):
        temp = []
        if i < n:
            for j in range(0, i+n):
                temp.append(data[j])
        elif i >= len(data)-n:
            for j in range(i-n, len(data)):
                temp.append(data[j])
        else:
            for j in range(i-n, i+n):
                temp.append(data[j])
        temp = np.mean(temp)
        new_array.append(temp)
    end = timeit.default_timer()
    if print_values == 'y':
        print('\nSmoothing took {} seconds.'.format(end-start))
    else:
        pass
    return(np.asarray(new_array))