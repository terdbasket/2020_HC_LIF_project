from programs.function_files.Orthagonal_LIF_dat_file_cleaner_functions import *

#get the current working directory
cwd = os.getcwd()
#change cwd to be the project folder
cwd = os.path.dirname(cwd)

directory = os.path.join(cwd+'/experiment_files/18_12_2020/1000_1/')
experiment_files = os.listdir(directory)
name = experiment_files[1]

date, cat_vol, slit_size, viewing_position, centre_offset, no_ramps = get_experimental_parameters_orthagonal(directory+name)

column_names = ['wlr', 'iod sig', 'lock sig', 'las pow']
data, dt, wavelength_ramps, iodine_signal, lockin_signal, laser_power = create_panda_dataset_and_data_arrays(directory, name, column_names)

time = np.arange(0, len(wavelength_ramps)*dt, dt)

time_section, wavelength_ramps_sections, iodine_signal_sections, lockin_signal_sections, laser_power_sections = break_data_into_ramp_regions(time, wavelength_ramps, iodine_signal, lockin_signal, laser_power)

averaged_laser_power = []
for i in range(len(laser_power)):
    temp = []
    if i <= len(laser_power)-25:
        for j in range(50):
            temp.append(laser_power[i-(25-j)])
    else:
        for j in range(len(laser_power)-i):
            temp.append(laser_power[len(laser_power)-j-1])
    averaged_laser_power.append(np.mean(temp))
averaged_laser_power = np.asarray(averaged_laser_power)


plt.subplot(2,2,1)
plt.plot(iodine_signal)
plt.title('iodine signal')

plt.subplot(2,2,2)
plt.plot(laser_power)
plt.title('laser power')

plt.subplot(2,2,3)
plt.plot(averaged_laser_power)
plt.title('averaged_laser_power')
plt.show()
plt.close()

print(np.mean(averaged_laser_power))

name = experiment_files[2]

date, cat_vol, slit_size, viewing_position, centre_offset, no_ramps = get_experimental_parameters_orthagonal(directory+name)

column_names = ['wlr', 'iod sig', 'lock sig', 'las pow']
data, dt, wavelength_ramps, iodine_signal, lockin_signal, laser_power = create_panda_dataset_and_data_arrays(directory, name, column_names)

time = np.arange(0, len(wavelength_ramps)*dt, dt)

time_section, wavelength_ramps_sections, iodine_signal_sections, lockin_signal_sections, laser_power_sections = break_data_into_ramp_regions(time, wavelength_ramps, iodine_signal, lockin_signal, laser_power)

averaged_laser_power = []
for i in range(len(laser_power)):
    temp = []
    if i <= len(laser_power)-25:
        for j in range(50):
            temp.append(laser_power[i-(25-j)])
    else:
        for j in range(len(laser_power)-i):
            temp.append(laser_power[len(laser_power)-j-1])
    averaged_laser_power.append(np.mean(temp))
averaged_laser_power = np.asarray(averaged_laser_power)


plt.subplot(2,2,1)
plt.plot(iodine_signal)
plt.title('iodine signal 2')

plt.subplot(2,2,2)
plt.plot(laser_power)
plt.title('laser power 2')

plt.subplot(2,2,3)
plt.plot(averaged_laser_power)
plt.title('averaged_laser_power 2')
plt.show()
plt.close()

print(np.mean(averaged_laser_power))