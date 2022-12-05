import scipy.optimize

from programs.function_files.Relative_density_plot_functions import *

#Load all function files, perhaps as dictionary
#Data_files to use

m_Ar = 6.6335e-26

analysis_path = os.path.join(os.path.dirname(os.getcwd()), 'analysis_files')
analysis_dates = list(os.listdir(analysis_path))

Exp_name_list, x_axis_list, relative_densities_list, Exp_dic_list = [],[],[], []


for date in analysis_dates:
    path = os.path.join(analysis_path, date, 'combined', 'adjusted')
    exp_names = list(os.listdir(os.path.join(analysis_path, date)))
    for name in exp_names:
        if '.csv' in name and 'adjusted' not in name:
            if date == '17_12_2020':
                if 'bottom' in name:
                    Exp_name_list.append(date+'_200_bl')
                elif 'radial' in name:
                    Exp_name_list.append(date+'_200_r')
                else:
                    Exp_name_list.append(date+'_200')
            else:
                exp_name = name[:3].replace('_','')
                Exp_name_list.append(date+'_'+exp_name)
    if date == '17_12_2020':
        options = list(os.listdir(path))
        for option in options:
            experiments = list(os.listdir(os.path.join(path, option)))
            experiments_dic = load_experiment_files_as_dic(os.path.join(path, option), experiments)
            Exp_dic_list.append(experiments_dic)
            relative_densities, positions = get_densities_normalised_to_bulk_density(experiments_dic)
            dist_positions = np.abs(np.asarray(positions) - 161)
            x_axis_list.append(dist_positions)
            relative_densities_list.append(np.asarray(relative_densities))
    else:
        experiments = list(os.listdir(path))
        experiments_dic = load_experiment_files_as_dic(path, experiments)
        Exp_dic_list.append(experiments_dic)
        relative_densities, positions = get_densities_normalised_to_bulk_density(experiments_dic)
        dist_positions = np.abs(np.asarray(positions)-161)
        x_axis_list.append(dist_positions)
        relative_densities_list.append(np.asarray(relative_densities))


pressures = [0.19, 1.9, 0.19, 0.19, 0.19, 37]

mkrsz = 5
lw = 1
label_fs = 14
t_fs = label_fs+1
ticksize = 12
a = 0.75


fig, ax = plt.subplots(figsize = (6,6))

print(Exp_name_list[5])
ax.plot(x_axis_list[5], relative_densities_list[5], color = 'grey', marker = 'D', linestyle = (0, (5, 1)), linewidth = lw, markersize = mkrsz, alpha = a, label = '$3, V=-1000,$ $p=37$,    cax')
print(Exp_name_list[0])
ax.plot(x_axis_list[0], relative_densities_list[0], color = 'b', marker = 'o', linestyle = 'dashed', linewidth = lw, markersize = mkrsz, alpha = a, label = '1, $V=-200,$   $p=0.19$, cax')


print(x_axis_list[4])
print(Exp_name_list[1])
ax.plot(x_axis_list[1], relative_densities_list[1], color = 'r', marker = 's', linestyle = (0, (5,10)), linewidth = lw, markersize = mkrsz, alpha = a, label = '2, $V=-200,$   $p=1.9$,   cax')

print(Exp_name_list[2])
ax.plot(x_axis_list[2], relative_densities_list[2], color = 'k', marker = 'x', linestyle = 'solid', linewidth = lw, markersize = mkrsz+2, alpha = a, label = '$4, V=-200,$   $p=0.19$, cax')
print(Exp_name_list[3])
ax.plot(x_axis_list[3], relative_densities_list[3], color = 'k', marker = '+', linestyle = 'dotted', linewidth = lw, markersize = mkrsz+3, alpha = a, label = '4, $V=-200,$   $p=0.19$, bax')
print(Exp_name_list[4])
ax.plot(x_axis_list[4], relative_densities_list[4], color = 'k', marker = '1', linestyle = 'dashdot', linewidth = lw, markersize = mkrsz+4,alpha = a, label = '4, $V=-200,$   $p=0.19$, rad')



ax.set_xlabel('Axial dist. from cathode edge (mm)', fontsize = label_fs)
ax.set_xlim((65, 0))
ax.set_ylabel('Relative Density', fontsize = label_fs)
# ax.set_yticklabels(fontsize = ticksize)
ax.set_title('Hollow Cathode ArII 3d $^2\mathregular{G}_{9/2}$ Density', fontsize = t_fs)

ax.legend(loc = 'upper left', fontsize = 'medium', numpoints = 2, markerfirst = True, framealpha = 0.75, handlelength=4, borderpad = 0.2, title = 'Exp, V, mTorr, pos', markerscale = 0.75, title_fontsize = 'medium')

fig.tight_layout()

plt.show()
plt.close()


###############################################################################################################
# CREATING THE MEAN VELOCITY DIC

var_len = 300
StoN_lim = 4.5

dist_positions_lists, y_mean_lists, y_peak_lists = [], [], []

for dic in Exp_dic_list:
    nerds, positions = get_densities_normalised_to_bulk_density(dic)
    dist_positions = np.abs(np.asarray(positions)-161)
    dist_positions_lists.append(dist_positions)
    keys = list(dic.keys())
    x_axis_list, y_axis_list = [], []
    for key in keys:
        df = dic[key]
        column_headers = list(dic[key].columns.values)
        x_axis_list.append(np.asarray(df[column_headers[1]]))
        y_axis_list.append(np.asarray(df[column_headers[0]]))
    mean_vels, peak_vels = [], []
    for i in range(len(keys)):
        mean_back = np.mean(y_axis_list[i][:var_len])
        std_dev = np.std(y_axis_list[i][:var_len])
        peak_vel = x_axis_list[i][y_axis_list[i]==max(y_axis_list[i])]
        if peak_vel >=1380:
            max_val = 3.2*peak_vel
            if peak_vel >= 10000:
                bottom = find_nearest_index_in_array(x_axis_list[i], peak_vel-5000)
            elif peak_vel >= 3500:
                bottom = find_nearest_index_in_array(x_axis_list[i], 1500)
            else:
                bottom = find_nearest_index_in_array(x_axis_list[i], 500)
            top = find_nearest_index_in_array(x_axis_list[i], max_val)
            x_averaging, y_averaging = x_axis_list[i][bottom:top], y_axis_list[i][bottom:top]
        else:
            max_vel = 2500
            min_vel = -750
            bottom =find_nearest_index_in_array(x_axis_list[i], min_vel)
            top = find_nearest_index_in_array(x_axis_list[i], max_vel)
            x_averaging, y_averaging = x_axis_list[i][bottom:top], y_axis_list[i][bottom:top]
        try:
            mean_vel = np.sum(x_averaging[y_averaging>=StoN_lim*std_dev+mean_back]*y_averaging[y_averaging>=StoN_lim*std_dev+mean_back])/np.sum(y_averaging[y_averaging>=StoN_lim*std_dev+mean_back])
            mean_vels.append(mean_vel)
        except RuntimeWarning:
            mean_vels.append(peak_vel)

        peak_vels.append(peak_vel)
        # plt.plot(x_axis_list[i], y_axis_list[i])
        # plt.plot(x_axis_list[i][:var_len], y_axis_list[i][:var_len], 'r--')
        # plt.plot(x_averaging[y_averaging>=StoN_lim*std_dev+mean_back], y_averaging[y_averaging>=StoN_lim*std_dev+mean_back], 'k-')
        # plt.axvline(x=peak_vel, color = 'green', linestyle = 'dashed', alpha = 0.5)
        # plt.axvline(x=mean_vel, color = 'k', linestyle = 'dashed', alpha = 0.5)
        # plt.axvline(x=1500, color = 'yellow', linestyle = ':')
        # plt.axvline(x=500, color = 'yellow', linestyle =':')
        # plt.show()
        # plt.close()
    y_mean_lists.append(np.asarray(mean_vels))
    y_peak_lists.append(np.asarray(peak_vels))

fig2, ax2 = plt.subplots(ncols = 1, figsize = (6,6))

print(Exp_name_list[5])
ax2.plot(dist_positions_lists[5], y_mean_lists[5]*1e-3, color = 'grey', marker = 'D', linestyle = (0, (5, 1)), linewidth = lw, markersize = mkrsz, alpha = a, label = '$3, V=-1000,$ $p=37$,    cax')
print(Exp_name_list[0])
ax2.plot(dist_positions_lists[0], y_mean_lists[0]*1e-3, color = 'b', marker = 'o', linestyle = 'dashed', linewidth = lw, markersize = mkrsz, alpha = a, label = '$1, V=-200,$   $p=0.19$, cax')
print(Exp_name_list[1])
ax2.plot(dist_positions_lists[1][:-2], y_mean_lists[1][:-2]*1e-3, color = 'r', marker = 's', linestyle = (0, (5,10)), linewidth = lw, markersize = mkrsz, alpha = a, label = '$2, V=-200,$   $p=1.9$,   cax')

print(Exp_name_list[2])
ax2.plot(dist_positions_lists[2], y_mean_lists[2]*1e-3, color = 'k', marker = 'x', linestyle = 'solid', linewidth = lw, markersize = mkrsz+2, alpha = a, label = '$4, V=-200,$   $p=0.19$, cax')
# print(Exp_name_list[3])
# ax2[0].plot(dist_positions_lists[3], y_mean_lists[3]*1e-3, color = 'k', marker = '+', linestyle = 'dotted', linewidth = lw, markersize = mkrsz+3, alpha = a, label = '$V=-200,$   $p=0.19$, bax')
print(Exp_name_list[4])
ax2.plot(dist_positions_lists[4], y_mean_lists[4]*1e-3, color = 'k', marker = '1', linestyle = 'dashdot', linewidth = lw, markersize = mkrsz+4,alpha = a, label = '$4, V=-200,$   $p=0.19$, rad')



ax2.set_xlabel('Axial dist. from cathode edge (mm)', fontsize = label_fs)
ax2.set_xlim((65, 0))
ax2.set_ylabel('Mean velocity (km/s)', fontsize = label_fs)
# ax.set_yticklabels(fontsize = ticksize)
ax2.set_title('Hollow Cathode ArII 3d $^2\mathregular{G}_{9/2}$ $<\mathbf{v}>$', fontsize = t_fs)

ax2.legend(loc = 'upper left', fontsize = 'medium', numpoints = 2, markerfirst = True, framealpha = 0.75, handlelength=4, borderpad = 0.2, title = 'Exp, V, mTorr, pos', markerscale = 0.75, title_fontsize = 'medium')
fig2.tight_layout()


plt.show()
plt.close()


fig3, ax3 = plt.subplots(figsize = (6,6))

print(Exp_name_list[5])
ax3.plot(dist_positions_lists[5], y_peak_lists[5]*1e-3, color = 'grey', marker = 'D', linestyle = (0, (5, 1)), linewidth = lw, markersize = mkrsz, alpha = a, label = '$V=-1000,$ $p=37$,    cax')
print(Exp_name_list[0])
ax3.plot(dist_positions_lists[0], y_peak_lists[0]*1e-3, color = 'b', marker = 'o', linestyle = 'dashed', linewidth = lw, markersize = mkrsz, alpha = a, label = '$V=-200,$   $p=0.19$, cax')
print(Exp_name_list[1])
ax3.plot(dist_positions_lists[1][:-2], y_peak_lists[1][:-2]*1e-3, color = 'r', marker = 's', linestyle = (0, (5,10)), linewidth = lw, markersize = mkrsz, alpha = a, label = '$V=-200,$   $p=1.9$,   cax')

print(Exp_name_list[2])
ax3.plot(dist_positions_lists[2], y_peak_lists[2]*1e-3, color = 'k', marker = 'x', linestyle = 'solid', linewidth = lw, markersize = mkrsz+2, alpha = a, label = '$V=-200,$   $p=0.19$, cax')
# print(Exp_name_list[3])
# ax2[1].plot(dist_positions_lists[3], y_peak_lists[3], color = 'k', marker = '+', linestyle = 'dotted', linewidth = lw, markersize = mkrsz+3, alpha = a, label = '$V=-200,$   $p=0.19$, bax')
print(Exp_name_list[4])
ax3.plot(dist_positions_lists[4], y_peak_lists[4]*1e-3, color = 'k', marker = '1', linestyle = 'dashdot', linewidth = lw, markersize = mkrsz+4,alpha = a, label = '$V=-200,$   $p=0.19$, rad')



ax3.set_xlabel('Axial dist. from cathode edge (mm)', fontsize = label_fs)
ax3.set_xlim((65, 0))
ax3.set_ylabel('Peak Velocity (m/s)', fontsize = label_fs)
# ax.set_yticklabels(fontsize = ticksize)
ax3.set_title('Hollow Cathode ArII 3d $^2\mathregular{G}_{9/2}$ $\mathbf{v}_\mathregular{pk}$', fontsize = t_fs)

ax3.legend(loc = 'upper left', fontsize = 'medium', numpoints = 2, markerfirst = True, framealpha = 0.75, handlelength=4, borderpad = 0.2, title = 'V, mTorr, pos', markerscale = 0.75, title_fontsize = 'medium')


fig3.tight_layout()

plt.show()
plt.close()

#Starting Riemann function plotter
V_0 = 5
Exp_1_positions, Exp_1_vels, Exp_1_pots = dist_positions_lists[0][:-4], y_mean_lists[0][:-4], V_0-0.5*m_Ar*y_mean_lists[0][:-4]**2/const.e
Exp_2_positions, Exp_2_vels, Exp_2_pots = dist_positions_lists[1][:-2], y_mean_lists[1][:-2], V_0-0.5*m_Ar*y_mean_lists[1][:-2]**2/const.e
Exp_3_positions, Exp_3_vels, Exp_3_pots = dist_positions_lists[5][:-2], y_mean_lists[5][:-2], V_0-0.5*m_Ar*y_mean_lists[5][:-2]**2/const.e
Exp_4_positions, Exp_4_vels, Exp_4_pots = dist_positions_lists[2][:-5], y_mean_lists[2][:-5], V_0-0.5*m_Ar*y_mean_lists[2][:-5]**2/const.e

rfig, rax = plt.subplots(ncols=2, figsize = (12,6))

rax[0].plot(Exp_1_positions, Exp_1_vels*1e-3, label = '1')
rax[0].plot(Exp_2_positions, Exp_2_vels*1e-3, label = '2')
rax[0].plot(Exp_3_positions, Exp_3_vels*1e-3, label = '3')
rax[0].plot(Exp_4_positions, Exp_4_vels*1e-3, label = '4')

rax[0].set_xlabel('Dist from cathode lip')
rax[0].set_ylabel('Mean velocity (km/s)')
rax[0].set_title('Presheath velocities')
rax[0].legend()

rax[1].plot(Exp_1_positions, Exp_1_pots, label = '1')
rax[1].plot(Exp_2_positions, Exp_2_pots, label = '2')
rax[1].plot(Exp_3_positions, Exp_3_pots, label = '3')
rax[1].plot(Exp_4_positions, Exp_4_pots, label = '4')

rax[1].set_xlabel('Dist from cathode lip')
rax[1].set_ylabel('Presheath potential diff (V)')
rax[1].set_title('Presheath potential diffs')
rax[1].legend()

rfig.tight_layout()
plt.show()
plt.close()


def Reimann_func(x, x_0, l, T_ec):
    return V_0-T_ec + T_ec*np.sqrt((x-x_0)/l)

Exp_1_fits, nerds = scipy.optimize.curve_fit(Reimann_func, Exp_1_positions[Exp_1_positions<=31], Exp_1_pots[Exp_1_positions<=31], bounds = ((3,10,0.5), (10,28, 5)))
Exp_2_fits, nerds = scipy.optimize.curve_fit(Reimann_func, Exp_2_positions[Exp_2_positions<=31], Exp_2_pots[Exp_2_positions<=31], bounds = ((0,5,0.5),(5,25, 5)))
Exp_4_fits, nerds = scipy.optimize.curve_fit(Reimann_func, Exp_4_positions[Exp_4_positions<=25], Exp_4_pots[Exp_4_positions<=25], bounds = ((5,7,0.5),(10,25, 5)))

fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (10,10))

ax[0,0].plot(Exp_1_positions, Exp_1_pots, 'bx')
ax[0,0].plot(Exp_1_positions, Reimann_func(Exp_1_positions, Exp_1_fits[0], Exp_1_fits[1], Exp_1_fits[2]), 'r')
ax[0,0].axvline(x=Exp_1_fits[0], color = 'k', linestyle = '--', alpha = 0.5)
ax[0,0].axvline(x=Exp_1_fits[0]+Exp_1_fits[1], color = 'k', linestyle = '--', alpha = 0.5)
ax[0,0].set_title('Exp 1 T_ec = {:.3f} eV'.format(Exp_1_fits[2]))
ax[0,0].set_xlabel('Distance from cathode (mm)')

ax[0,1].plot(Exp_2_positions, Exp_2_pots, 'bx')
ax[0,1].plot(Exp_2_positions, Reimann_func(Exp_2_positions, Exp_2_fits[0], Exp_2_fits[1], Exp_2_fits[2]), 'r')
ax[0,1].axvline(x=Exp_2_fits[0], color = 'k', linestyle = '--', alpha = 0.5)
ax[0,1].axvline(x=Exp_2_fits[0]+Exp_2_fits[1], color = 'k', linestyle = '--', alpha = 0.5)
ax[0,1].set_title('Exp 2 T_ec = {:.3f} eV'.format(Exp_2_fits[2]))
ax[0,1].set_xlabel('Distance from cathode (mm)')

ax[1,0].plot(Exp_4_positions, Exp_4_pots, 'bx')
ax[1,0].plot(Exp_4_positions, Reimann_func(Exp_4_positions, Exp_4_fits[0], Exp_4_fits[1], Exp_4_fits[2]), 'r')
ax[1,0].axvline(x=Exp_4_fits[0], color = 'k', linestyle = '--', alpha = 0.5)
ax[1,0].axvline(x=Exp_4_fits[0]+Exp_4_fits[1], color = 'k', linestyle = '--', alpha = 0.5)
ax[1,0].set_title('Exp 4 T_ec = {:.3f} eV'.format(Exp_4_fits[2]))
ax[1,0].set_xlabel('Distance from cathode (mm)')

fig.tight_layout()

plt.show()
plt.close()
