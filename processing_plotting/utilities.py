# -*- coding: utf-8 -*-
import numpy as np
import os
import scipy.optimize as sciopt

#------------------------------------------------------------
def clean_legend(axis, location="upper left", title=None, reverse_last=False):
    handles, labels = axis.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    
    handle_list = list(by_label.values())
    label_list  = list(by_label.keys())
    if reverse_last and len(handle_list) > 1:
        handle_list = [handle_list[-1]] + handle_list[:-1]
        label_list  = [label_list[-1]]  + label_list[:-1]
    
    axis.legend(handle_list, label_list, loc=location, title=title)

#------------------------------------------------------------
def power_fit(df, df_x_name, df_y_name, pts):
    df_nonzero = df[df[df_x_name]>0]
    #create x values from minimum to maximum numCycles in dataframe
    x    = np.linspace(df_nonzero[df_x_name].min(), df_nonzero[df_x_name].max(), pts)
    logx = np.log10(df_nonzero[df_x_name])
    logy = np.log10(df_nonzero[df_y_name])

    # define our (line) fitting function
    # fitfunc = lambda p, x: p[0] + p[1] * x   
    errfunc = lambda p, x, y: (y - (p[0] + p[1] * x ))
    pinit   = [0.15, -0.25] #initial guess
    out     = sciopt.leastsq(errfunc, pinit, args=(logx, logy))
    pfinal  = out[0]
    index   = pfinal[1]
    amp     = 10.0**pfinal[0]
    y       = amp*x**index
    return [index, amp, x, y]  
# %%
#------------------------------------------------------------
# decode file names used during runs for ability to retrieve loading paths, drainage, d_r, etc.
# function create here / used later
def decode_name(filework, start_loc=None): 
    filename = os.path.basename(filework)
    infoList = filename[:-4].split("_")   # strip .csv, split by "_"
    
    water    = infoList[0][0]   # 'u' or 'd'
    driver   = infoList[0][1:]  # 'DSS' or 'PSC'
    goal     = infoList[1]      # 'cyc', 'mono', etc.
    density  = infoList[2][2:]  # e.g., '35'
    output   = infoList[-1]     # '3', 'csrN', etc.
    
    if goal == "cyc":
        extra = infoList[-4:-1]
    elif goal in ["MRD", "vol", "rec"]:
        extra = infoList[-3:-1]
    else:
        extra = 0
    
    return [driver, goal, water, density, extra, output]

# %%
# Helper match functions for goal-specific extraInfo checks
def matches_cyc(info_extra, filter_extra):
    sigvc_vals, alpha_vals, Ko_vals = filter_extra
    sigvc = info_extra[0][3:]
    alpha = info_extra[1][1:]
    Ko    = info_extra[2][2:]

    return (
        (not sigvc_vals or sigvc in sigvc_vals) and
        (not alpha_vals or alpha in alpha_vals) and
        (not Ko_vals or Ko in Ko_vals)
    )

def matches_MRD_or_vol(info_extra, filter_extra):
    Ncyc_vals, maxg_vals = filter_extra
    Ncyc = info_extra[0][4:]
    maxg = info_extra[1][3:]  # safer than assuming single digit

    return (
        (not Ncyc_vals or Ncyc in Ncyc_vals) and
        (not maxg_vals or maxg in maxg_vals)
    )

def matches_rec(info_extra, filter_extra):
    sigvc_vals, alpha_vals = filter_extra
    sigvc = info_extra[0][3:]
    alpha = info_extra[1][1:]

    return (
        (not sigvc_vals or sigvc in sigvc_vals) and
        (not alpha_vals or alpha in alpha_vals)
    )

#------------------------------------------------------------
# driverType = 'DSS' or 'PSC'
# testType   = 'mono','MRD','vol','cyc','rec'
# drainType  = 'u' or 'd'
# density    = '35','55','75' or [] for all
# output     = single element number or summary file (e.g. peakPhi, csrN)

def create_file_list(fileList, driverType=[], testType=[], drainType=[], 
                     density=[], extraInfo=[], output=[]):

    file_list = []
    for file in fileList:
        file_info = decode_name(file)
        [driver, goal, water, dens, extra, outp] = file_info

        if (
            (not driverType or driver in driverType) and
            (not testType or goal in testType) and
            (not drainType or water in drainType) and
            (not density or dens in density) and
            (not output or outp in output)
        ):
            match = False
            if not extraInfo:
                match = True
            elif goal == 'cyc':
                match = matches_cyc(extra, extraInfo)
            elif goal in ['MRD', 'vol']:
                match = matches_MRD_or_vol(extra, extraInfo)
            elif goal == 'rec':
                match = matches_rec(extra, extraInfo)
            
            if match:
                file_list.append(file)

    return file_list
