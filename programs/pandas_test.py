import pandas as pd
import numpy as np

file_string = r'C:\Users\nran6184\PycharmProjects\2020_HC_LIF_project\experiment_files\16_12_2020\200_1\100_0_3.dat'


data = pd.read_csv(file_string,delimiter='\t',skiprows=3,header=None)
data.columns = ['wl','iodine sig','lockin sig','laser power']

dt = np.array(data['wl'][0])
data_wl = np.array(data['wl'][1:])
print(data_wl)

print(dt)