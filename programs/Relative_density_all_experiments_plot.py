from programs.function_files.Relative_density_plot_functions import *

#Load all function files, perhaps as dictionary
#Data_files to use

analysis_path = os.path.join(os.path.dirname(os.getcwd()), 'analysis_files')
analysis_dates = list(os.listdir(analysis_path))

Exp_name_list, x_axis_list, relative_densities_list = [],[],[]

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
            relative_densities, positions = get_densities_normalised_to_bulk_density(experiments_dic)
            dist_positions = np.abs(np.asarray(positions) - 161)
            x_axis_list.append(dist_positions)
            relative_densities_list.append(np.asarray(relative_densities))
    else:
        experiments = list(os.listdir(path))
        experiments_dic = load_experiment_files_as_dic(path, experiments)
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
ax.plot(x_axis_list[5], relative_densities_list[5], color = 'grey', marker = 'D', linestyle = (0, (5, 1)), linewidth = lw, markersize = mkrsz, alpha = a, label = '$V=-1000,$ $p=37$,    cax')
print(Exp_name_list[0])
ax.plot(x_axis_list[0], relative_densities_list[0], color = 'b', marker = 'o', linestyle = 'dashed', linewidth = lw, markersize = mkrsz, alpha = a, label = '$V=-200,$   $p=0.19$, cax')


print(x_axis_list[4])
print(Exp_name_list[1])
ax.plot(x_axis_list[1], relative_densities_list[1], color = 'r', marker = 's', linestyle = (0, (5,10)), linewidth = lw, markersize = mkrsz, alpha = a, label = '$V=-200,$   $p=1.9$,   cax')

print(Exp_name_list[2])
ax.plot(x_axis_list[2], relative_densities_list[2], color = 'k', marker = 'x', linestyle = 'solid', linewidth = lw, markersize = mkrsz+2, alpha = a, label = '$V=-200,$   $p=0.19$, cax')
print(Exp_name_list[3])
ax.plot(x_axis_list[3], relative_densities_list[3], color = 'k', marker = '+', linestyle = 'dotted', linewidth = lw, markersize = mkrsz+3, alpha = a, label = '$V=-200,$   $p=0.19$, bax')
print(Exp_name_list[4])
ax.plot(x_axis_list[4], relative_densities_list[4], color = 'k', marker = '1', linestyle = 'dashdot', linewidth = lw, markersize = mkrsz+4,alpha = a, label = '$V=-200,$   $p=0.19$, rad')



ax.set_xlabel('Axial dist. from cathode edge (mm)', fontsize = label_fs)
ax.set_xlim((65, 0))
ax.set_ylabel('Relative Density', fontsize = label_fs)
# ax.set_yticklabels(fontsize = ticksize)
ax.set_title('Hollow Cathode ArII 3d $^2\mathregular{G}_{9/2}$ Density', fontsize = t_fs)

ax.legend(loc = 'upper left', fontsize = 'medium', numpoints = 2, markerfirst = True, framealpha = 0.75, handlelength=4, borderpad = 0.2, title = 'V, mTorr, pos', markerscale = 0.75, title_fontsize = 'medium')

fig.tight_layout()

figure_path = os.path.join(os.path.dirname(os.getcwd()), 'figures', 'paper_figures')
plt.savefig(os.path.join(figure_path, 'Relative_density_plot.eps'), format = 'eps')
plt.savefig(os.path.join(figure_path, 'Relative_density_plot.png'), format = 'png')

plt.show()
plt.close()
