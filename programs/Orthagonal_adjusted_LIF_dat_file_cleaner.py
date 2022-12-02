from programs.function_files.Orthagonal_LIF_dat_file_cleaner_functions import *
from programs.function_files.generally_useful_functions import *

#TODO find out argon bohm speed

#Experimental parameters
#We have to be very careful in the fact that the lines given in the relevant iodine absorption spectrum are vacuum lines or something,
#and the reality is very different. Nicolas has given me that the zero velocity point corresponds to 16348.909 angstroms on the
#iodine absorption graph. Furthermore, the main peak we find is quite far from the vacuum absorption value we'd expect, being actually
#6114.923 angstroms (1 A = 0.1 nm)
ArI_ab_wave_vac = 611.4923e-9 #nm (Argon ion metastable absorption line 3d^2G_(9/2) to 4p^2F_(7/2) )
ArI_ab_wave_reality = 611.6601e-9 #nm (Argon ion metastable absorption line that actually occurs in our system)
ArI_em_wave_vac = 460.9e-9 #nm (Argon ion metastable excited emission line (4p^2F_(7/2) to 3s^2G_(9/2) )
em_zero_point_on_ab = 611.66161e-9 #nm (The emission line at zero velocity on the iodine absorption graph. I'll need to determine this properly
ArI_mass = 6.6335209e-26 - 9.109e-31 #kg
sig_to_noise_tol = 5.0 #What signal to noise tolerance we are willing to accept as peak
zero_pos = 16348.9483 #value for the 0 peak iodine absorption peak cm^-1
right_pos = 16349.1458 #value of the first peak to the right of the zero peak

#Code decision parameters
near_to_centre = 'n'
norm_centre_offset = 2.0
num_ramps_specified = 'y' #TODO ONLY INCLUDE THIS IF NUMBER OF RAMPS NOT IN EXPERIMENT NAME

#Code analysis parameters
#Averaging value of the laser power signal
n_point_average = 25
peak_cut_off = 0.85 #Percentage as a fraction. Height of maximum peak value used to determine whether peak is too flat to
#be a gaussian
g_accept_tol = 0.1 #Percentage as a fraction. How many values can be above peak_cut_off value before we decide we don't
#have a gaussian

#get the current working directory
cwd = os.getcwd()
#change cwd to be the project folder
cwd = os.path.dirname(cwd)

directory = os.path.join(cwd+'/experiment_files/15_12_2020/200_1/')
experiment_files = os.listdir(directory)
#name = experiment_files[15]
column_names = ['wlr', 'iod sig', 'lock sig', 'las pow']

print('\nAnalysing experiment {}'.format(name))

date, cat_vol, slit_size, viewing_position, centre_offset, no_ramps = get_experimental_parameters_orthagonal(directory+name, num_ramps_specified)

data, dt, wavelength_ramps, iodine_signal, lockin_signal, laser_power = create_panda_dataset_and_data_arrays(directory, name, column_names)
#create the time array
time = np.arange(0, len(wavelength_ramps)*dt, dt)

#Normalising the results to laser power assuming a linear relationship (giving an upper limit to the peak density increase later in the experiment)
all_experiments_dic = create_dic_of_all_experiments_as_pandas(directory, experiment_files, column_names)
power_adjustment_array = create_power_adjustement_array(all_experiments_dic,  name, experiment_files, column_names, n_point_average)


adjusted_lockin_signal = lockin_signal/power_adjustment_array

time_section, wavelength_ramps_sections, iodine_signal_sections, adjusted_lockin_signal_sections, laser_power_sections = break_data_into_ramp_regions(time, wavelength_ramps, iodine_signal, adjusted_lockin_signal, laser_power)

#Checks if the ramps are overlapped.y If they are, the analysis is much, much simpler, as we can get the user to only
#have to choose peaks once.
while True:
    overlap = check_iodine_signals_overlap(time_section, iodine_signal_sections)
    if overlap == 'y':
        break
    else:
        wavelength_ramps_sections, iodine_signal_sections, adjusted_lockin_signal_sections, laser_power_sections, no_ramps = fix_up_problematic_iodine_signals(overlap, time_section, wavelength_ramps_sections, iodine_signal_sections, adjusted_lockin_signal_sections, laser_power_sections, no_ramps)

#To try and set up a system where the user picks the points from the graph. If centre offset is <= +- 3, we use given values.
#otherwise, we let the user choose to use them or not.
peak1, peak2 = choose_peak_points(time_section, iodine_signal_sections[1])

#now i'd need to change the time axis into a frequency axis or a wavelength or velocity axis.
#This needs to be done personally by checking the iodine absorption spectrum, unfortunately.
if near_to_centre == 'n':
    choice = input('\nDoes the iodine spectra contain the zero peak and rightmost peak? y/n: ').lower()
    if choice == 'y':
        wavelength_ab_section, time_differences_in_num_dt, wave_per_dt = convert_time_axis_to_wavelength(time_section,peak1, peak2, dt, zero_pos, right_pos)
    elif choice == 'n':
        wavelength_ab_section, time_differences_in_num_dt, wave_per_dt = convert_time_axis_to_wavelength(time_section, peak1, peak2, dt)
elif abs(norm_centre_offset-centre_offset) <=3: #If you are within 3 ghz of your normal cen offset
    wavelength_ab_section, time_differences_in_num_dt, wave_per_dt = convert_time_axis_to_wavelength(time_section, peak1, peak2, dt, zero_pos, right_pos)
else:
    choice = input('\nDoes the iodine spectra contain the zero peak and rightmost peak? y/n: ').lower()
    if choice == 'y':
        wavelength_ab_section, time_differences_in_num_dt, wave_per_dt = convert_time_axis_to_wavelength(time_section, peak1, peak2, dt, zero_pos, right_pos)
    elif choice == 'n':
        wavelength_ab_section, time_differences_in_num_dt, wave_per_dt = convert_time_axis_to_wavelength(time_section, peak1, peak2, dt)

#Creating the emission wavelength spectrum for showing the lock in signal
wavelength_em_section = determine_wavelength_em_axis(wavelength_ab_section, em_zero_point_on_ab, ArI_em_wave_vac)

#Converting doppler shifts from zero point to speeds
velocity_section_c, velocity_section = convert_wave_to_doppler_shift(wavelength_ab_section, em_zero_point_on_ab)

#Converting speeds into electron volts
ion_energy_ev = convert_speeds_to_ev(velocity_section, ArI_mass)

#If the input signals overlap, we could then average the lock in signals together
adjusted_lockin_signal_average = average_lockin_signals(adjusted_lockin_signal_sections, no_ramps)

#Determining if there is a Gaussian peak or not. If not, I don't know what to do, but we'll see.
peak_type = spot_gaussian_peak(adjusted_lockin_signal_average, peak_cut_off, g_accept_tol)

#Now i'd want to get some values out of this signal. I'm going to try the old fit a gaussian to the signal and see
#what the ion temp is and the median value etc. This could be bullshit if we have saturation, something i'll have to look
#into as well. Need to set baseline to zero as well to do this

adjusted_lockin_signal_baseline0 = baseline_to_zero(adjusted_lockin_signal_average, sig_to_noise_tol)

clear_peak = check_for_clear_peak(velocity_section, adjusted_lockin_signal_baseline0)
em_peak_amp_by_max_index = find_peak_by_average_max(adjusted_lockin_signal_average, peak_cut_off)
em_peak_cen_v = velocity_section[em_peak_amp_by_max_index]

subplot_analysis(time_section, wavelength_ab_section, velocity_section_c, velocity_section, ion_energy_ev, iodine_signal_sections, adjusted_lockin_signal_average, em_peak_cen_v)

plt.plot(velocity_section, adjusted_lockin_signal_average)
plt.title('Adjusted and averaged lock in signal on velocity with averaged max value given')
plt.axvline(x = em_peak_cen_v, color='k', linestyle = '--')
plt.axvline(x = velocity_section[em_peak_amp_by_max_index], color = 'g', linestyle = '--')
close_figure_with_keyboard_or_mouse()
plt.close()

create_excel_docs_lockin_signal_and_results(directory+name, adjusted_lockin_signal_average, velocity_section, clear_peak, 'adjusted', max_peak_vel = em_peak_cen_v)

print('\nThe ion peak maximum velocity: {:.2f} m/s'.format(em_peak_cen_v))
# print('The ion temp assuming a Maxwellian: {:.2f} K'.format(ion_temp))
# print('Note that an ion temp above room temp far from the sheath is a likely indication of line broadening due to laser'
#       'power (see Claire, Bachet, Stroth, Doveil 2006)')
# print('They claim that the ion temp should be maxwellian at room even in the sheath for the same experiment but with a plate.')