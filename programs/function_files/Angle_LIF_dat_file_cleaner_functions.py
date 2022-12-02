from Orthagonal_LIF_dat_file_cleaner_functions import *

def get_experimental_parameters_angle(filename):
    directories_list = filename.split('/') #breaks up directories after the 2020 folder
    date = directories_list[2] #date of experiment
    temp = directories_list[3].replace('-','.').split('_')
    cat_vol = int(temp[0])
    slit_size = float(temp[1])
    temp = directories_list[-1].replace('.dat', '').replace('-','.').split('_')
    pole_pos = float(temp[0])
    towards = float(temp[1])
    sidewards = float(temp[2])
    rotation = float(temp[3])
    return date, cat_vol, slit_size, pole_pos, towards, sidewards, rotation