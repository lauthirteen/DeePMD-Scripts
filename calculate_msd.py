#!/usr/bin/env python3
import matplotlib.pyplot as plt
import MDAnalysis as mda 
import numpy as np
from scipy.stats import linregress
import MDAnalysis.analysis.msd as msd
from MDAnalysis.tests.datafiles import RANDOM_WALK, RANDOM_WALK_TOPO
from MDAnalysis.tests.datafiles import TPR, XTC, TRR
####################################################################
trj_name = "npt.lammpstrj"
dt = 1 # ps the time of two frame
correlation_length = 50 # ps
sample_interval    = 1  # ps
msd_type =  'type 1'  # atom type number or name(e.g.  type 1 , name OW , index 1-12)
slope_begin = 10  # ps
slope_end   = correlation_length # ps
####################################################################
single_msd_frame = correlation_length / dt
sample_interval_frame = sample_interval / dt
# msd
# for lammps
u = mda.Universe(trj_name, format='LAMMPSDUMP', dt=dt)
# for gmx
#u = mda.Universe('md.tpr', 'md.trr', continuous=True)
#print(single_msd_frame)
total_frame = len(u.trajectory)
#total_frame = 100000
msd_time = (total_frame - single_msd_frame) / sample_interval_frame
MSD = msd.EinsteinMSD(u, select=msd_type, msd_type='xyz', fft=True)
##########
begin = 0
begin_frame = 0
total_msd = []
while begin <= msd_time:
    end_frame = begin_frame + single_msd_frame
    #print(begin_frame, end_frame)
    MSD.run(start=int(begin_frame), stop=int(end_frame))
    msd =  MSD.results.timeseries
    total_msd.append(msd)
    begin_frame += sample_interval_frame
    begin += 1
#'''
msd_time = np.arange(single_msd_frame)*dt # ps
total_msd_mean = (np.array(total_msd)).mean(axis=0)
#print(total_msd)
# get D
start_index = int(slope_begin / dt)
end_index = int(slope_end / dt)
linear_model = linregress(msd_time[start_index:end_index], total_msd_mean[start_index:end_index])
slope = linear_model.slope
error = linear_model.rvalue
# dim_fac is 3 as we computed a 3D msd with 'xyz'
D = slope * 1/(2*MSD.dim_fac)
print("The self-diffusivities is : %s (10e-6) cm^2/s" % round(D, 6))
# plot
fig = plt.figure()
ax = plt.axes()
ax.plot(msd_time, total_msd_mean, label=r'3D random walk')
plt.show()
#'''