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

def find_region_of_signal_above_threshold(experiments_dic, Sig_to_noise):
    keys = list(experiments_dic.keys())
    column_headers = list(experiments_dic[keys[0]].columns.values)
    analysis_dic = {}
    for key in keys:
        x_axis = np.asarray(experiments_dic[key][column_headers[1]])
        y_axis = np.asarray(experiments_dic[key][column_headers[0]])
        #Find the signal to noise ratio by searching through dataset
        peak_index = np.where(y_axis == max(y_axis))[0][0]
        if peak_index <= len(y_axis)/2: #If max in first half of data
            STN_mean = np.mean(y_axis[int(0.8*len(y_axis)):])
            STN_std = np.std(y_axis[int(0.8*len(y_axis)):])
        else:
            STN_mean = np.mean(y_axis[:int(0.2 * len(y_axis))])
            STN_std = np.std(y_axis[:int(0.2 * len(y_axis)):])
        x_signal = np.asarray([])
        y_signal = np.asarray([])
        for i in range(len(y_axis)):
            if y_axis[i] >= STN_mean + Sig_to_noise*STN_std:
                x_signal = np.append(x_signal, x_axis[i])
                y_signal = np.append(y_signal, y_axis[i])
            else:
                pass
        plt.plot(x_axis, y_axis, 'b')
        plt.plot(x_signal, y_signal, 'r')
        plt.title('Check for accuracy of Signal to noise threshold')
        close_figure_with_keyboard_or_mouse()
        plt.close()
        signal = 'y'
        while True:
            worked = input('\nWas the automatic STN finder accurate enough? y/n: ').lower().replace(' ','')
            if worked == 'y':
                break
            elif worked == 'n':
                no_peaks = int(input('\nhow many peaks were there as an integer? '))
                if no_peaks == 0:
                    signal = 'n'
                    break
                elif no_peaks == 1:
                    while True:
                        plt.plot(x_axis, y_axis)
                        plt.title('Select region to integrate under')
                        plt.get_current_fig_manager().full_screen_toggle()
                        positions = plt.ginput(2, timeout=0)
                        plt.close()
                        point1, point2 = positions[0][0], positions[1][0]
                        left_finding, right_finding = np.abs(x_axis-point1), np.abs(x_axis-point2)
                        left_position = np.where(left_finding == min(left_finding))[0][0]
                        right_position = np.where(right_finding == min(right_finding))[0][0]
                        x_signal = x_axis[left_position:right_position]
                        y_signal = y_axis[left_position:right_position]
                        plt.plot(x_axis, y_axis, 'b')
                        plt.plot(x_signal, y_signal, 'r')
                        plt.title('Check for user selected signal accuracy')
                        close_figure_with_keyboard_or_mouse()
                        plt.close()
                        fixed = input('\nDid you select the signal successfully? y/n: ').lower().replace(' ','')
                        if fixed == 'y':
                            break
                        else:
                            pass
                    break
                elif no_peaks == 2:
                    while True:
                        plt.plot(x_axis, y_axis)
                        plt.title('Select first region to integrate under')
                        plt.get_current_fig_manager().full_screen_toggle()
                        positions1 = plt.ginput(2, timeout=0)
                        plt.close()
                        point1, point2 = positions1[0][0], positions1[1][0]
                        plt.plot(x_axis, y_axis)
                        plt.title('Select second region to integrate under')
                        plt.get_current_fig_manager().full_screen_toggle()
                        positions2 = plt.ginput(2, timeout=0)
                        plt.close()
                        point3, point4 = positions2[0][0], positions2[1][0]
                        finding1, finding2, finding3, finding4 = np.abs(x_axis-point1), np.abs(x_axis- point2), np.abs(x_axis-point3), np.abs(x_axis-point4)
                        position1 = np.where(finding1 == min(finding1))[0][0]
                        position2 = np.where(finding2 == min(finding2))[0][0]
                        position3 = np.where(finding3 == min(finding3))[0][0]
                        position4 = np.where(finding4 == min(finding4))[0][0]
                        x_signal = x_axis[position1:position2]
                        x_signal = np.concatenate((x_signal, x_axis[position3:position4]))
                        y_signal = y_axis[position1:position2]
                        y_signal = np.concatenate((y_signal, y_axis[position3:position4]))
                        plt.plot(x_axis, y_axis, 'b')
                        plt.plot(x_signal, y_signal, 'r')
                        plt.title('Check for user selected signal accuracy')
                        close_figure_with_keyboard_or_mouse()
                        plt.close()
                        fixed = input('\nDid you select the signal successfully? y/n: ').lower().replace(' ', '')
                        if fixed == 'y':
                            break
                        else:
                            pass
                break
            else:
                print('\nUser input error. Try again.')
        if signal == 'y':
            data_file = pd.DataFrame(data={column_headers[0]: y_signal, column_headers[1]: x_signal})
            analysis_dic[key] = data_file
        else:
            pass
    return analysis_dic

def save_experiments_dic_to_csv(experiments_dic, path, filenames):
    print('\nSaving combined files to {}'.format(path))
    keys = list(experiments_dic.keys())
    i = 0
    for key in keys:
        experiments_dic[key].to_csv(path_or_buf=os.path.join(path, filenames[i])+'.csv', index = False)
        i += 1
    return