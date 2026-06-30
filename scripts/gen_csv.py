
import sys
import os
import numpy as np
import glob
import csv
from pyMCDS_cells import pyMCDS_cells
import matplotlib.pyplot as plt

output_dirs = []

cell_cycle_duration = 443.5    # 5*T

# fig = plt.figure(figsize=(4,3), dpi=200, tight_layout=True)
# fig = plt.figure(figsize=(6,4))
# fig.subplots(1)
# ax0 = fig.gca()

# gamma_vals = np.arange(0.0, 1.0, 0.01)   # 100 samples
# print(gamma_vals)


# Time,RepID,CellID,x,y,CellType
tvals = []
cell_id = []
xval = []
yval = []
cell_type = []
# gvals = []

if True:
        # folder_name = "out_num_cells_b" + str(beta) + "_g" + str(gamma)
        data_dir = "output_checker_diag_6x6"
        print('data_dir = ',data_dir)
        if (not os.path.exists(data_dir)):
            print("--- ERROR missing dir: ", data_dir)
            sys.exit(-1)

        os.chdir(data_dir)
        xml_files = glob.glob('output*.xml')
        os.chdir('..')
        xml_files.sort()
        # print('xml_files = ',xml_files)

        ds_count = len(xml_files)
        print("ds_count = ",ds_count)
        # ds_count = 192
        # print("----- ds_count = ",ds_count)
        mcds_list = [pyMCDS_cells(xml_files[i], data_dir) for i in range(ds_count)]

        tval = np.linspace(0, mcds_list[-1].get_time(), ds_count)

        # tval /= cell_cycle_duration
        print("tval= ",tval)
        final_time = tval[-1]
        print(f'{data_dir} final time= {final_time}')

        # if final_time > 0:
        #     tvals.append(final_time)
        #     # gvals.append(gamma)
        #     gvals.append(gamma)
        # else:
        #     print(f"  --- bogus time {final_time} in {data_dir} ")


# https://docs.google.com/document/d/14h4rCwNZLw3g2-aY5ihM4maJGMjhvq0QZryJFYA-wcM/edit?tab=t.0
# Data format (James’): 
# Time 1, Cell 1 x, cell 1 y, cell 1 type, Cell 2 x … 
# Time 2, Cell 1 x
# Data format (Inge’s):
# Time : 0 1 2 3 0 1 2 3
# Replication id : 0 0 0 0 0 0 0 0 
# Cell id : 0 0 0 0 1 1 1 1
# X coordinate : x1 x2 x3 x4 …
# Y coordinate : y1 y2 y3 y4 …
# Type : t1 t2 t3 t4 …

# Time,RepID,CellID,x,y,CellType


file_out = f'pc_6x6.csv'
print("--> ",file_out)
sim = 0
with open(file_out, "w", newline="") as file:
    writer = csv.writer(file)
    # writer.writerow(['Time','Rep','CellID','x','y','CellType'])
    writer.writerow(['simID','time','cellID','cellType','x','y'])
    
# 0,10,0,5,2.02184,2.24461
# 0,10,1,0,1.83799,1.30547
    for mcds in mcds_list:
        t = mcds.get_time()
        # print("t=",mcds.get_time())
        cell_ids = mcds.get_cell_df()["ID"]
        xvals = mcds.get_cell_df()["position_x"]
        yvals = mcds.get_cell_df()["position_y"]
        cell_types = mcds.get_cell_df()["cell_type"]
        for idx in range(len(cell_types)):
            print("cell_types= ",cell_types)
            # writer.writerow([t,rep,cell_ids[idx],xvals[idx],yvals[idx],cell_types[idx]])
            writer.writerow([sim, t, int(cell_ids[idx]),int(cell_types[idx]),xvals[idx],yvals[idx]])
    # for jdx in range(len(gvals)):
        # writer.writerow([gvals[jdx],tvals[jdx]])

# ax0.plot(gvals,tvals,'.-', color='k')

# ax0.set_title("beta=0", fontsize=12)
# ax0.set_xlabel(r'$\gamma$')
# # ax0.set_xlim(0., 1.)
# ax0.set_xlim(left=-0.05, right=1.05)
# # ax0.set_ylim(0., 100.)
# ax0.set_yscale('log')
# ax0.set_ylabel('Time (calibrated for 5T)')
# # ax0.savefig(data_dir + '.png')
# plt.show()

