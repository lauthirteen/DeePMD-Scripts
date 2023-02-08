import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
from matplotlib.pyplot import MultipleLocator


def File_2_List(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
    return lines

def Parse_Energy_Out(FileName):
    Lines = File_2_List(FileName)
    all_data = []
    data_e, pred_e = [], []
    for line in Lines[1:]:
        tmp = line.split()
        if tmp[0] == "#":
            data_e, pred_e = np.array(data_e), np.array(pred_e)
            all_data.append([data_e, pred_e])
            data_e, pred_e = [], []
        else:
            data_e.append(float(tmp[0]))
            pred_e.append(float(tmp[1]))
    data_e, pred_e = np.array(data_e), np.array(pred_e)
    all_data.append([data_e, pred_e])
    return all_data

def Plot_Energy(filename,Natom,RMSE):
    all_data = Parse_Energy_Out(filename)
    Nsys = len(Natom)
    for i in range(0,Nsys):
        #print(i)
        data_e_0, pred_e_0 = all_data[i][0],all_data[i][1]
        data_e_0, pred_e_0 = data_e_0/Natom[i], pred_e_0/Natom[i]
        #print(data_e_0, pred_e_0)
        fig, ax = plt.subplots(1, 1, figsize=(12,12))
        ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='-', c='k', label="1:1 line")
        ax.plot(data_e_0, pred_e_0, 'o', c='royalblue')

        corr = np.corrcoef(data_e_0, pred_e_0)[0,1]
        bbox = dict(boxstyle='round', fc='1', alpha=0.5)
        plt.text(0.05, 0.85, '$R^2=%.5f$\nAtom: %s\nRMSE: %.5e' %(corr**2,Natom[i],RMSE[i]), transform=ax.transAxes, size=25, bbox=bbox)
        ax.set_xlabel('data_E (eV/atom)', fontsize=25)
        ax.set_ylabel('pred_E (eV/atom)', fontsize=25)
        ax.tick_params(labelsize=15) 
        plt.show()
        fig.savefig("Energy_atom%s.jpg" % Natom[i],dpi=300)

def Parse_Force_Out(FileName):
    Lines = File_2_List(FileName)
    all_data = []
    data_f, pred_f = [], []
    for line in Lines[1:]:
        tmp = line.split()
        if tmp[0] == "#":
            data_f, pred_f = np.array(data_f), np.array(pred_f)
            all_data.append([data_f, pred_f])
            data_f, pred_f = [], []
        else:
            data_f.append(float(tmp[0])) # x
            data_f.append(float(tmp[1])) # y
            data_f.append(float(tmp[2])) # z
            pred_f.append(float(tmp[3])) # x
            pred_f.append(float(tmp[4])) # y
            pred_f.append(float(tmp[5])) # z
    data_f, pred_f = np.array(data_f), np.array(pred_f)
    all_data.append([data_f, pred_f])
    return all_data

def Plot_Force(filename,Natom,RMSE):
    all_data = Parse_Force_Out(filename)
    Nsys = len(Natom)
    for i in range(0,Nsys):
        #print(i)
        data_f_0, pred_f_0 = all_data[i][0],all_data[i][1]
        data_f_0, pred_f_0 = data_f_0/Natom[i], pred_f_0/Natom[i]
        #print(data_e_0, pred_e_0)
        fig, ax = plt.subplots(1, 1, figsize=(12,12))
        ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='-', c='k', label="1:1 line")
        ax.plot(data_f_0, pred_f_0, 'o', c='royalblue')

        corr = np.corrcoef(data_f_0, pred_f_0)[0,1]
        bbox = dict(boxstyle='round', fc='1', alpha=0.5)
        plt.text(0.05, 0.85, '$R^2=%.5f$\nAtom: %s\nRMSE: %.5e' %(corr**2,Natom[i],RMSE[i]), transform=ax.transAxes, size=25, bbox=bbox)
        ax.set_xlabel('data_F (eV/A)', fontsize=25)
        ax.set_ylabel('pred_F (eV/A)', fontsize=25)
        ax.tick_params(labelsize=15) 
        plt.show()
        fig.savefig("Force_atom%s.jpg" % Natom[i],dpi=300)
        
if __name__ == '__main__':
    #  dp_test_file  sys_atom_num  sys_energy_rmse
    Plot_Energy("out.e.out", [64,72],[6.246492e-03,5.727013e-03])
    # dp_test_file  sys_atom_num  sys_force_rmse
    Plot_Force("out.f.out", [64,72],[1.454664e-01,1.544947e-01])