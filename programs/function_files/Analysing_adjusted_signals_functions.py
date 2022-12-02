from programs.function_files.generally_useful_functions import *
import pandas as pd
from PIL import Image

def load_experiment_files_as_dic(path, experiments):
    names = []
    for name in experiments:
        names.append(name.replace('.csv','').replace('adjusted_',''))
    experiments_dic = {}
    for i in range(len(experiments)):
        temp = pd.read_csv(os.path.join(path,experiments[i]))
        experiments_dic[names[i]] = temp
    return experiments_dic

def check_waterfall_plot_for_problems(figure_path, Date, Experiment_type, adjusted):
    print('\nUser check to see if any dataset needs to be removed.')
    figure_path = os.path.join(figure_path, Date)
    files = os.listdir(figure_path)
    #Now in correct directory, need to find correct figure
    if adjusted == 'y':
        for file in files:
            if 'adjusted' and Experiment_type+'_waterfall' in file:
                filename = file
            else:
                pass
    else:
        for file in files:
            if 'adjusted' not in file:
                if Experiment_type+'_waterfall' in file:
                    filename = file
                else:
                    pass
            else:
                pass
    image = Image.open(os.path.join(figure_path, filename))
    image.show()
    image.close()
    while True:
        remove = input('\nAre there any datasets you would like to remove? y/n: ').lower().replace(' ', '')
        if remove == 'y' or remove == 'n':
            return remove
        else:
            print('\nError in user input. Try again.')
            pass


def inspect_and_remove_bad_files(experiments_dic, remove):
    if remove == 'n':
        return experiments_dic
    else:
        pass
    print('\nUser will cycle through figures and select the dataset to remove.')
    keys = list(experiments_dic.keys())
    for key in keys:
        column_headers = list(experiments_dic[key].columns.values)
        x_axis = experiments_dic[key][column_headers[1]]
        y_axis = experiments_dic[key][column_headers[0]]
        plt.plot(x_axis, y_axis)
        plt.title(key)
        plt.xlabel(column_headers[1])
        plt.ylabel(column_headers[0])
        close_figure_with_keyboard_or_mouse()
        plt.close()
        while True:
            cont = input('\nRemove dataset? y/n: ').lower().replace(' ', '')
            if cont == 'n':
                break
            elif cont == 'y':
                print('\nRemoving {} from experiments list'.format(key))
                experiments_dic.pop(key)
                break
            else:
                print('\nUser input error. Please try again.')
                pass
    return experiments_dic

def join_measurements_at_same_position(experiments_dic):
    keys = list(experiments_dic.keys())
    column_headers = list(experiments_dic[keys[0]].columns.values)
    positions = []
    repetition_dic = {}
    for key in keys: #create dictionary with how many measurements made at the same position
        info = key.split('_')
        positions.append(info[0])
        if info[0] not in repetition_dic.keys():
            repetition_dic[info[0]] = 1
        else:
            repetition_dic[info[0]] += 1
    for place in list(repetition_dic.keys()):
        if repetition_dic[place] == 1:
            pass
        else:
            print('\nCombining and averaging the {} measurements'.format(place))
            datasets, x_axes, y_axes = [], [], []
            for key in keys:
                if place in key:
                    datasets.append(experiments_dic[key])
                    x_axes.append(experiments_dic[key][column_headers[1]])
                    y_axes.append(experiments_dic[key][column_headers[0]])
                    experiments_dic.pop(key) #Remove each individual experiment from the experiment dic
                else:
                    pass
            sorted_x_axes, sorted_y_axes = [], []
            while len(x_axes) > 0:
                mins = []
                for data in x_axes:
                    mins.append(min(data))
                for i in range(len(x_axes)):
                    if min(x_axes[i]) == min(mins):
                        sorted_x_axes.append(np.asarray(x_axes[i]))
                        del x_axes[i]
                        sorted_y_axes.append(np.asarray(y_axes[i]))
                        del y_axes[i]
                        break
                    else:
                        pass
#Now we are making a x_axis that has no data where there is no y data but we can assign existing y values to a nearest point
            ranges = []
            for i in sorted_x_axes:
                ranges.append([min(i), max(i)])
            x_axes_ranges =[]
            number_values_per_array = []
            num = 0
            for i in range(len(ranges)):
                if i != len(ranges)-1:
                    if ranges[i][1] >= ranges[i+1][0]:
                        if i == 0:
                            x_axes_ranges.append(ranges[i][0])
                            num += np.count_nonzero(sorted_x_axes[i] <= ranges[i+1][0])

                        else:
                            if ranges[i][0] <= ranges[i-1][1]: #dataset fully contained by other datasets
                                if ranges[i][1] < ranges[i-1][1]:
                                    num += np.count_nonzero(sorted_x_axes[i] <= ranges[i+1][0])
                                else:
                                    num += len(sorted_x_axes[i]) - np.count_nonzero(sorted_x_axes[i] < ranges[i-1][1]) - np.count_nonzero(sorted_x_axes[i] > ranges[i+1][0])
                            else:
                                x_axes_ranges.append(ranges[i][0])
                                num += np.count_nonzero(sorted_x_axes[i] <= ranges[i + 1][0])
                    else:
                        if i == 0:
                            x_axes_ranges.append(ranges[i][0])
                            x_axes_ranges.append(ranges[i][1])
                            number_values_per_array.append(len(sorted_x_axes[i]))

                        elif ranges[i][0] <= ranges[i-1][1]:
                            x_axes_ranges.append(ranges[i][1])
                            num += len(sorted_x_axes[i])
                            number_values_per_array.append(num)
                            num = 0
                        else:
                            x_axes_ranges.append(ranges[i][0])
                            x_axes_ranges.append(ranges[i][1])
                            number_values_per_array.append(len(sorted_x_axes[i]))
                else:
                    if ranges[i][0] <= ranges[i-1][1]:
                        x_axes_ranges.append(ranges[i][1])
                        num += len(sorted_x_axes[i])
                        number_values_per_array.append(num)
                    else:
                        x_axes_ranges.append(ranges[i][0])
                        x_axes_ranges.append(ranges[i][1])
                        number_values_per_array.append(len(sorted_x_axes[i]))
            x_axes_ranges = np.asarray(x_axes_ranges).flatten()
            print('{} x_axes_ranges'.format(place), x_axes_ranges)
            print('{} number_values_per_array'.format(place), number_values_per_array)
            x_axis = np.asarray([])
            y_axis = []
            n,m = 0,0
            for i in range(int(len(x_axes_ranges)/2)):
                set = np.linspace(x_axes_ranges[m], x_axes_ranges[m+1], num = int(number_values_per_array[n]/2))
                #Make the bins twice as big, makes sure to capture both sets
                x_axis = np.concatenate((x_axis, set))
                m += 2
                n+=1
            for i in range(len(x_axis)):
                if i == len(x_axis)-1:
                    low_limit, top_limit = x_axis[i-1], x_axis[i]
                else:
                    low_limit, top_limit = x_axis[i], x_axis[i+1]
                y_values = []
                for j in range(len(sorted_x_axes)):
                    for n in range(len(sorted_x_axes[j])):
                        if sorted_x_axes[j][n] >= low_limit and sorted_x_axes[j][n] <= top_limit:
                            y_values.append(sorted_y_axes[j][n])
                        else:
                            pass
                if len(y_values) == 0:
                    y_axis.append(y_axis[-1])
                else:
                    y_axis.append(np.mean(y_values))
            y_axis = np.asarray(y_axis)
            print('x_axis', x_axis)
            print('y_axis:', y_axis)
            new_dataframe = {column_headers[0]: y_axis, column_headers[1]: x_axis}
            new_dataframe = pd.DataFrame(new_dataframe, columns=column_headers)
            experiments_dic[place + '_combined'] = new_dataframe
    temp = {}
    for key in sorted(experiments_dic): #sorting the dictionary by position
        temp[key] = experiments_dic[key]
    experiments_dic = temp
    return experiments_dic, list(repetition_dic.keys())

def save_experiments_dic_to_csv(experiments_dic, path, filenames):
    print('\nSaving combined files to {}'.format(path))
    keys = list(experiments_dic.keys())
    i = 0
    for key in keys:
        experiments_dic[key].to_csv(path_or_buf=os.path.join(path, filenames[i])+'.csv', index = False)
        i += 1
    return
