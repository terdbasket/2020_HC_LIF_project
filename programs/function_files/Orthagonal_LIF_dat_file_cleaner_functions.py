import csv
import numpy as np
import sys
import matplotlib.pyplot as plt
import os
import pandas as pd
from itertools import cycle
from scipy.optimize import curve_fit
from programs.function_files.generally_useful_functions import *

#parameters to use in functions
k_B = 1.38064852e-23  # m^2.kg.s^-2.K^-1
c = 299792458.0  # m/s

def create_dic_of_all_experiments_as_pandas(path, filenames, column_names):
    experiments_dic = {}
    for file in filenames:
        data, dt, wavelength_ramps, iodine_signal, lockin_signal, laser_power = create_panda_dataset_and_data_arrays(path, file, column_names)
        experiments_dic[file] = data
    return experiments_dic

def get_experimental_parameters_orthagonal(filename, *num_ramps_specified):
    directories_list = filename.split('/') #breaks up directories after the 2020 folder
    date = directories_list[2] #date of experiment
    temp = directories_list[3].split('_')
    cat_vol = int(temp[0]) #Cathode voltage V
    slit_size = float(temp[1]) #size of viewing slit mm
    temp = directories_list[4][:-4].split('_')
    viewing_position = float(temp[0]) #The viewing position along the laser beam mm
    centre_offset = float(temp[1]) #Scanning lazer frequency central offset GHz
    if len(num_ramps_specified) == 0 or num_ramps_specified[0] == 'y':
        no_ramps = int(temp[2]) #How many ramps were performed for each viewing position
    else:
        no_ramps = num_ramps_specified[0]
    return(date, cat_vol, slit_size, viewing_position, centre_offset, no_ramps)

def create_panda_dataset_and_data_arrays(directory, name, column_names):
    file_string = directory + name
    # If I wanted just up to the folder containing the file, i'd end it with \\' since \' doesn't end the string
    data = pd.read_csv(file_string, delimiter='\t', skiprows=3,
                       header=None)  # we start at the 3th line (want the dt data)
    # we need to say header=none or otherwise pandas tries to find column headers automatically
    data.columns = column_names  # Giving names to the columns
    dt = data[column_names[0]][0]
    # we create np arrays for each column for manipulation
    wavelength_ramps = np.array(data['wlr'][1:])  # pulls out column under 'wlr' heading starting at line 1
    iodine_signal = np.array(data['iod sig'][1:])
    lockin_signal = np.array(data['lock sig'][1:])
    laser_power = np.array(data['las pow'][1:])
    return data, dt, wavelength_ramps, iodine_signal, lockin_signal, laser_power

def create_power_adjustement_array(all_experiments_dic, name, experiment_names, column_names, n_point_average):
    total_power = np.asarray([])
    positions_dic = {}
    print('\nSmoothing laser power signal.')
    start = timeit.default_timer()
    for i in range(len(all_experiments_dic)):
        positions_dic[experiment_names[i]] = [len(total_power)]
        power = np.asarray(all_experiments_dic[experiment_names[i]][column_names[-1]][1:])
        power = n_point_array_smooth(power, n_point_average, 'n')
        total_power = np.concatenate((total_power, power))
        positions_dic[experiment_names[i]].append(len(total_power))
    end = timeit.default_timer()
    print('\nSmoothing took {} s.'.format(end-start))
    max_pow = max(total_power)
    left_index, right_index = positions_dic[name][0], positions_dic[name][1]
    total_power_normalised = total_power/max_pow
    adjusted_power = []
    for i in range(left_index, right_index):
        adjusted_power.append(total_power_normalised[i])
    return np.asarray(adjusted_power)

def break_data_into_ramp_regions(time, wavelength_ramps, iodine_signal, lockin_signal, laser_power):
    print('\nBreaking data into separate scanning ramp regions')
    maxpoints = [] #the positions of the final value of a ramp
    for i in range(len(wavelength_ramps)-1):
        if wavelength_ramps[i+1] > wavelength_ramps[i]:
            pass
        else:
            maxpoints.append(i)
    time_sections = []
    wavelength_ramps_sections = []
    iodine_signal_sections = []
    lockin_signal_sections = []
    laser_power_sections = []
    for i in range(len(maxpoints)): #use the maxpoints to break up the data into sections
        if i == 0:
            start = 0
        else:
            start = maxpoints[i-1] #always start at either 0 or the value after the last section ended at
        time_sections_temp = ()
        wavelength_ramps_sections_temp = ()
        iodine_signal_sections_temp = ()
        lockin_signal_sections_temp = ()
        laser_power_sections_temp = ()
        for j in range(start, maxpoints[i]): #set up an array for each section
            time_sections_temp = np.append(time_sections_temp, time[j])
            wavelength_ramps_sections_temp = np.append(wavelength_ramps_sections_temp, wavelength_ramps[j])
            iodine_signal_sections_temp = np.append(iodine_signal_sections_temp, iodine_signal[j])
            lockin_signal_sections_temp = np.append(lockin_signal_sections_temp, lockin_signal[j])
            laser_power_sections_temp = np.append(laser_power_sections_temp, laser_power[j])
        #create a list of the section arrays #arrays of arrays not so easy to deal with
        time_sections.append(time_sections_temp)
        wavelength_ramps_sections.append(wavelength_ramps_sections_temp)
        iodine_signal_sections.append(iodine_signal_sections_temp)
        lockin_signal_sections.append(lockin_signal_sections_temp)
        laser_power_sections.append(laser_power_sections_temp)
            #we want all the time sections to start at 0 and go onwards for easy comparison, so we do that
        #Fix up lengths if they differ slightly
        lengths = []
        for n in range(len(time_sections)):
            lengths.append(len(time_sections[n]))
        lengths = np.array(lengths)
        if all(length == lengths[0] for length in lengths) == True:  # check if all lengths the same
            pass
        else: #Find the longest list and remove it's last value until it matches other lengths
            while all(length == lengths[0] for length in lengths) == False:
                index = np.where(lengths == max(lengths))[0][0]
                a = np.delete(wavelength_ramps_sections[index], -1)
                wavelength_ramps_sections[index] = a
                b = np.delete(iodine_signal_sections[index], -1)
                iodine_signal_sections[index] = b
                d = np.delete(lockin_signal_sections[index], -1)
                lockin_signal_sections[index] = d
                e = np.delete(laser_power_sections[index], -1)
                laser_power_sections[index] = e
                f = np.delete(time_sections[index], -1)
                time_sections[index] = f
                lengths = []
                for n in range(len(time_sections)):
                    lengths.append(len(time_sections[n]))
                lengths = np.array(lengths)
    time_section = time_sections[0]  # they are all the same length in the end
    return(time_section, wavelength_ramps_sections, iodine_signal_sections, lockin_signal_sections, laser_power_sections)


def check_iodine_signals_overlap(time_section, iodine_sections):

    num_ramps = len(iodine_sections)
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colours = cycle(prop_cycle.by_key()['color'])
    print('\nUser check to see if iodine signals overlap for each lamp.')
    for i in range(num_ramps):
        plt.plot(time_section, iodine_sections[i], color=next(colours))
    plt.title('All iodine absorption reference signals overlayed by ramp')
    close_figure_with_keyboard_or_mouse()
    plt.close()
    while True:
        overlap = input('\nDo the iodine plots overlap? y/n: ').lower()
        if overlap == 'y' or overlap == 'n':
            break
        else:
            print('Please try again')
    return(overlap)

def fix_up_problematic_iodine_signals(overlap, time_section, wavelength_ramps_sections, iodine_signal_sections, lockin_signal_sections, laser_power_sections, no_ramps):
    if overlap == 'y':
        return wavelength_ramps_sections, iodine_signal_sections, lockin_signal_sections, laser_power_sections, no_ramps
    else:
        print('\nUser must search through iodine absorption spectrum and identify which ramp contains first shifted spectrum')
        for i in range(no_ramps-1):
            plt.plot(time_section, iodine_signal_sections[i], 'b')
            plt.plot(time_section, iodine_signal_sections[i+1], 'r')
            plt.title('Spectra {} and {}'.format(str(i), str(i+1)))
            close_figure_with_keyboard_or_mouse()
            plt.close()
            problem = input('\nWas absorption spectra shift shown? y/n: ').lower().replace(' ', '')
            if problem == 'y':
                if i >= no_ramps/2.0-1:
                    no_ramps = i
                    print('\nRetaining ramps {} to {}'.format(0,i))
                    #list[:4] returns list elements [0,1,2,3]. we want the ith value, so we have to input i+1
                    return wavelength_ramps_sections[:i+1], iodine_signal_sections[:i+1], lockin_signal_sections[:i+1], laser_power_sections[:i+1], no_ramps
                elif i == 0:
                    first = input('\nWhich signal was leftmost? b/r ').lower().replace(' ', '')
                    if first == 'b':
                        no_ramps = len(lockin_signal_sections)-1
                        print('\nRetaining ramps {} to {}'.format(1, no_ramps))
                        return wavelength_ramps_sections[1:], iodine_signal_sections[1:], lockin_signal_sections[1:], laser_power_sections[1:], no_ramps
                    elif first == 'r':
                        no_ramps = len(lockin_signal_sections)-2
                        print('\nRetaining ramps {} to {}'.format(2, no_ramps))
                        return wavelength_ramps_sections[2:], iodine_signal_sections[2:], lockin_signal_sections[2:], laser_power_sections[2:], no_ramps
                    else:
                        print('\nIncorrect input error. Next time, please input "r" or "b"')
                        sys.exit()
                else:
                    no_ramps = len(lockin_signal_sections) - (i+1)
                    #list[4:] returns list elements [4,5,6,7,...]
                    print('\nRetaining ramps {} to {}'.format(i+1, len(iodine_signal_sections)))
                    return wavelength_ramps_sections[i+1:], iodine_signal_sections[i+1:], lockin_signal_sections[i+1:], laser_power_sections[i+1:], no_ramps
            else:
                pass
        print('\nYa done fucked something. Program exiting.')
        sys.exit()



def choose_peak_points(time_section, iodine_section):
    print('\nSelect two known peaks from left to right. If using zero positions, choose the zero peak and one to the right of it.')
    print('\nBefore selecting, compare the absorption spectrum to the reference iodine absorption data (found at ')
    print('https://www.cnrseditions.fr/catalogue/physique-et-astrophysique/atlas-spectre-dabsorption-molecule-diode-gerstenkorn/ )'
          '\nand determine the wave-number of the two peaks you are selecting.')
    print('\nBe careful to left click as close to the peak maximum as possible. ')
    while True:
        plt.plot(time_section, iodine_section)
        plt.title('Select two known peaks from left to right')
        plt.get_current_fig_manager().full_screen_toggle()
        positions = plt.ginput(2, timeout=0)
        plt.close()
        while True:
            fuckup = input('\nDid you fuck up the points? y/n: ').lower()
            if fuckup == 'y':
                print("\nSigh. Then, let's go again.")
                break
            elif fuckup == 'n':
                break
            else:
                print("\nChe?")
                continue
        if fuckup == 'n':
            break
        else:
            pass
    peak1, peak2 = positions[0][0], positions[1][0]
    return peak1, peak2

def convert_time_axis_to_wavelength(time_sections, peak1, peak2, dt, *zero_positions):
    print('\nConverting time axis to wavelengths.')
    if len(zero_positions) == 0:
        known_left_peak = float(input(u"\nEnter the leftmost peak's wavenumber in cm\u207B\u00B9: "))
        known_right_peak = float(input(u"\nEnter the rightmost peak's wavenumber in cm\u207B\u00B9: "))
    else:
        known_left_peak = zero_positions[0]
        known_right_peak = zero_positions[1]
    known_left_peak = 1.0/(known_left_peak*100) #Wavelength in nm
    known_right_peak = 1.0/(known_right_peak*100)
    # Determining a time-step equivalent in wavelength
    wave_per_dt = -abs((known_right_peak-known_left_peak)/((peak2-peak1)/dt))
    #Since differences are small, we need to change our time graph to time from the first peak
    time_differences_in_num_dt = []
    for i in time_sections:
        time_differences_in_num_dt.append((i-peak1)/dt)
    wavelength_section = []
    for i in time_differences_in_num_dt: #Faster to create list for this method and then turn to array
        wavelength_section.append(known_left_peak + (i*wave_per_dt))
    wavelength_section = np.array(wavelength_section)
    return wavelength_section, time_differences_in_num_dt, wave_per_dt

def determine_wavelength_em_axis(wavelength_abs_section, em_zero_point_on_ab, ArI_em_wave):
    wavelength_em_section = wavelength_abs_section - em_zero_point_on_ab + ArI_em_wave #This isn't correct! It'll put the emission line at the absorption line.
    return wavelength_em_section

def convert_wave_to_doppler_shift(wavelength_sections, ArI_ab_wave):
    print('\nConverting emission wavelengths to Argon ion metastable velocities against known emission line.')
    velocity_section_c = [] # velocity as fraction of speed of light
    for i in wavelength_sections:
        velocity_section_c.append(1.0-i/ArI_ab_wave)
    velocity_section_c = np.array(velocity_section_c)
    velocity_section = velocity_section_c*c
    return(velocity_section_c, velocity_section)


def convert_speeds_to_ev(velocity_section, ArI_mass):
    ion_energy_ev = []
    for i in velocity_section:
        ion_energy_ev.append(0.5*ArI_mass*i**2)
    return np.array(ion_energy_ev)/1.602e-19

def average_lockin_signals(lockin_signal_sections, no_ramps):
    lockin_signal_average = np.zeros(len(lockin_signal_sections[0]))
    for i in range(no_ramps):
        temp = lockin_signal_average+lockin_signal_sections[i]
        lockin_signal_average = temp
    return np.divide(lockin_signal_average,no_ramps)

def spot_gaussian_peak(lockin_signal_average, peak_cut_off, tolerance):
    #if more than peak_cut_off percentage of the total values are above tolerance * maximum value of averaged signals,
    #then the peak shouldn't be a gaussian
    new_array = np.where(lockin_signal_average >= peak_cut_off*max(lockin_signal_average))[0]
    cut_off = len(lockin_signal_average)*tolerance
    if len(new_array) <= cut_off:
        peak_type = 'gaussian'
        print('\nAutomatic gaussian spotter has detected gaussian peak.')
    else:
        peak_type = 'other'
        print('\nAutomatic gaussian spotter has detected non-gaussian peak.')
    return peak_type
def subplot_analysis(time_section, wavelength_section, velocity_section_c, velocity_section, ion_energy_ev, iodine_signal_sections, lockin_signal_average, em_peak_cen_v):
    plt.subplot(2, 3, 1)
    plt.plot(time_section, iodine_signal_sections[1])
    plt.xlabel('time')

    plt.subplot(2, 3, 2)
    plt.plot(wavelength_section, iodine_signal_sections[1])
    plt.gca().invert_xaxis() #wavelength is decreasing as wavenumber increases
    plt.xlabel('wavelength')

    plt.subplot(2, 3, 3)
    plt.plot(velocity_section_c, iodine_signal_sections[1])
    plt.xlabel('velocity c')

    plt.subplot(2, 3, 4)
    plt.plot(velocity_section, iodine_signal_sections[1])
    plt.xlabel('velocity')

    plt.subplot(2, 3, 5)
    plt.plot(ion_energy_ev, iodine_signal_sections[1])
    plt.xlabel('ion energy')

    plt.subplot(2, 3, 6)
    plt.plot(velocity_section, iodine_signal_sections[1], 'b')
    plt.plot(velocity_section, lockin_signal_average, 'r')
    plt.axvline(x = em_peak_cen_v, color = 'k', linestyle = '--')
    plt.xlabel('velocity iodine lockin overlay')

    plt.suptitle('Axes analysis of data')
    close_figure_with_keyboard_or_mouse()
    plt.close()

def baseline_to_zero(lockin_signal_average, sig_to_noise_tol, **averaging_percentage):
    if len(averaging_percentage) < 1:
        ap = 0.2
    else:
        ap = averaging_percentage[0]
    print('\nSetting lockin signal baseline to zero for fitting gaussian')
    #need to first check that the peak isn't in the 1st 20 percent of the signal
    temp_start = 0
    for i in range(int(len(lockin_signal_average)*ap)):
        temp_start += lockin_signal_average[i]
    average_start = temp_start/int(len(lockin_signal_average)*ap)
    temp_end = 0
    for i in range(int(len(lockin_signal_average)*(1-ap)), len(lockin_signal_average)):
        temp_end += lockin_signal_average[i]
    average_end = temp_end/int(len(lockin_signal_average)*ap)
    #If nowhere in signal has value greater than sig_to_noise_tol times the average starting values or ending values,
    #then trying to fit a gaussian will be invalid anyway
    baseline = []
    if average_start >= sig_to_noise_tol*max(lockin_signal_average) and average_end >= sig_to_noise_tol*max(lockin_signal_average):
        print('No peak with signal to noise above {}, invalid to try gaussian fit.'.format(sig_to_noise_tol))
        return lockin_signal_average
    #If we have a peak, AND it's not in the first part of the signal (if it's in first part, average value could be high as well)
    elif average_start < sig_to_noise_tol*max(lockin_signal_average) and np.where(lockin_signal_average == max(lockin_signal_average))[0][0] > ap*len(lockin_signal_average):
        for i in lockin_signal_average:
            baseline.append(i-average_start)
    elif average_end < sig_to_noise_tol*max(lockin_signal_average) and np.where(lockin_signal_average == max(lockin_signal_average))[0][0] < (1-ap)*len(lockin_signal_average):
        for i in lockin_signal_average:
            baseline.append(i-average_end)
    else:
        print('\nSomething done gone goofed in your lockin signal')
        return print("cunt's fucked")
    lockin_signal_baseline0 = np.array(baseline)
    return lockin_signal_baseline0

def gaussian(x, amp, mu, sigma):
    return amp*(1.0/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*(x-mu)**2/sigma**2)

def fit_gaussian_to_data(time_differences_in_num_dt, lockin_signal, peak_type):
    amplitude = max(lockin_signal)
    def function(x, amp, mu, sigma):
        return amp*(1.0/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*(x-mu)**2/sigma**2)
    if peak_type == 'gaussian':
        print('\nCurve fitting gaussian to lockin signal with initial amp guess of {:.2f}'.format(amplitude))
        fit_values, useless = curve_fit(function, time_differences_in_num_dt, lockin_signal, p0=[amplitude, 0.0, 1.0])
    else:
        fit_values = [max(lockin_signal), np.where(lockin_signal == max(lockin_signal))[0], 1.0]
    return fit_values

def find_peak_by_max(lockin_signal_average):
    result = np.where(lockin_signal_average == max(lockin_signal_average))[0]
    return int(np.mean(result))

def find_peak_by_average_max(lockin_signal_average, peak_cut_off):
    top_vals_indice_list = np.where(lockin_signal_average >= peak_cut_off*max(lockin_signal_average))[0]
    return int(np.mean(top_vals_indice_list))


def fit_parameter_analysis(amp, mu, sigma, time_differences_in_num_dt, velocity_section, ArI_mass, wave_per_dt, em_zero_point_on_ab, peak_type):
    if peak_type == 'gaussian':
        #Getting mu as a velocity
        place = find_nearest_index_in_array(time_differences_in_num_dt, mu)
        mu = velocity_section[place]
        #determining the ion temperature assuming a maxwellian. It's already in number of dt's. So we need to convert this
        sigma = sigma * wave_per_dt
        sigma_w = em_zero_point_on_ab - sigma
        #wavelength diff from emission wavelength
        sigma_v_c = 1.0-sigma_w/em_zero_point_on_ab
        sigma_v = sigma_v_c*c
        ion_temp = ArI_mass*sigma_v**2/k_B
        return(mu, ion_temp)
    else:
        return (0, 0)

def create_excel_docs_lockin_signal_and_results(filename, lockin_signal_average, velocity_section, clear_peak, *adjusted, **results):
    cwd = os.getcwd()
    cwd = os.path.dirname(cwd) #now in 2020_HC_LIF_project
    aim_directory = cwd+'\\analysis_files\\'
    directory_files = filename.split('/')
    experiment_date = directory_files[2]
    if 'adjusted' in adjusted:
        experiment_group = 'adjusted_'+directory_files[3]
        experiment_name = 'adjusted_'+directory_files[-1].replace('.dat','')
    else:
        experiment_group = directory_files[3]
        experiment_name = directory_files[-1].replace('.dat','')
    path = os.path.join(aim_directory, experiment_date)
    try:
        os.mkdir(path)
        print('\nNew directory {} created.'.format(path))
        pass
    except FileExistsError:
        pass
    #want to create/update file containing all the important points for each individual experiment
    files = os.listdir(path)
    peak_data_file_name = experiment_group+'.csv'
    temp_dic = {}
    for key in results: #replacing keys with key_experiment_name
        temp_dic[experiment_name+'_'+key] = results[key]
    results = temp_dic
    results_pd = pd.DataFrame(results, index = [0])
    #This csv file will be saved as a row of strings followed by the particular values for each particular experiment.
    #This means that the first row will serve as the column headers for the entire dataset, even though it's actually
    #only relevant to the first data row.
    if peak_data_file_name in files: #If csv file already exists
        #Check if data headings already there. If so, overwrite.
        check = pd.read_csv(path+'\\'+peak_data_file_name)
        keys = results.keys() #get results keys to check against csv column headers
        temp = []
        for key in keys:
            temp.append(key)
        keys = temp #python doesn't like comparing a python thingy to a numpy thingy with an 'in' check
        if keys[0] in check.columns[0] or keys[0] in check.values: #if data already in the csv (checking column titles and also dataset
            print('\n{} Dataset already exists. Overwriting old dataset.'.format(peak_data_file_name))
            os.remove(path+'\\'+peak_data_file_name) #delete old csv file. Now we update the dataframe and remake the file
            if keys[0] in check.columns: #if we are replacing the first dataset from the dataframe (so that the dataframe column names are for this particular dataset
                for key in keys:
                    check[key][0] = results[key]
                check.to_csv(path_or_buf=path + '\\' + peak_data_file_name, index=False)
            else: #If we are replacing some random value in the dataframe
                row_index_of_titles = get_pandas_indexes(check, keys[0])[0][0]
                headers = check.columns
                for i in range(len(headers)):
                    check[headers[i]][row_index_of_titles+1] = results[keys[i]]
                check.to_csv(path_or_buf=path + '\\' + peak_data_file_name, index=False)
        else:
            print('\nAdding {} results to {}'.format(experiment_name, peak_data_file_name))
            results_pd.to_csv(path_or_buf = path+'\\'+peak_data_file_name, mode = 'a', index=False)
    else:
        print('\nCreating {} and adding {} results'.format(peak_data_file_name, experiment_name))
        results_pd.to_csv(path_or_buf = path+'\\'+peak_data_file_name, index = False)
    path = os.path.join(path, experiment_group)
    try:
        os.mkdir(path)
        print('\nNew directory {} created.'.format(path))
        pass
    except FileExistsError:
        pass
    #creating pandas dataframe

    if clear_peak == 'y':
        path = os.path.join(path, experiment_name)
        print('\nSaving lockin_signal_average vs velocity as {}.csv in {}\\{} folder.'.format(experiment_name,
                                                                                              experiment_date,
                                                                                              experiment_group))
    else:
        experiment_name +='_no_clear_peak'
        path = os.path.join(path, experiment_name)
        print('\nSaving lockin_signal_average vs velocity as {}.csv in {}\\{} folder.'.format(experiment_name,
                                                                                              experiment_date,
                                                                                              experiment_group))
    LIF_result = {'Average lockin_signal': lockin_signal_average, 'Ion velocity': velocity_section}
    LIF_result = pd.DataFrame(data=LIF_result)
    LIF_result.to_csv(path_or_buf=path+'.csv', index=False)
    return

def check_for_clear_peak(velocity_section, lockin_signal_baseline0, *nurries):
    if len(nurries) == 0:
        print('\nUser must check for clear peak in averaged lockin signal.')
        plt.plot(velocity_section, lockin_signal_baseline0, 'b')
        plt.title('Lockin_signal_baseline')
        close_figure_with_keyboard_or_mouse()
        plt.close()
        while True:
            clear_peak = input('\nWas there a clear lock-in signal peak? y/n: ').lower().replace(' ', '')
            if clear_peak == 'y' or clear_peak == 'n':
                break
            else:
                print('\nChe?')
    else:
        clear_peak = 'y'
    return(clear_peak)


