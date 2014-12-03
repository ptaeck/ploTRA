#! /usr/bin/python
from __future__ import print_function
import csv
import sys

# csv. field_size_limit(sys.maxsize)     # working with huge csv!    python 2.7.5 throws error
import wx

from matplotlib import rcParams
from random import choice
import random

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math
import pickle
import operator
from Tkinter import *
import tkSimpleDialog

import numpy as np


#==================================================================
# S E T T I N G S
#==================================================================
   
""" Defaults. """
gui         = 0                      # if gui == 0: (all files for analysis are taken from experiment_info.py) and settings below is applied
                                   
traPath = 'C:/Users/ptaeck/PY/exp/cykly-tah-sorted-nov/TRA'                # default TRA lookout folder 


""" Experiment analysis settings. """
cyclic      = 1                      # cyclic experiment ? if cyclic == 0: expecting TRA files for simple tensile test
maketscurve = 1                      # calculate envelope curve for cyclic tensile test / average tensile curve for tensile test ?
pas         = 1                      # plot averaged slopes 
angles      = 1                      # print angles in graph ?  (hardoff now)

wantpng     = 1
wantpdf     = 1


interav     = 0                      # average simple tensile experiment in interval defined by precision ? 
loadtscurve = 0                      # load curve from simple tensile test to cyclic experiment graph ? \
statistics  = 0                      # print csv table with statistical data ?


expGroups   = 7                      #groups of specimens (angles)
expCount    = 3                      #experiment count for one group of specimens

precision   = '10'                   #takes each nth point for averaging, if cyclic: precision = 1 !


dde = 1                              # displacement driven cyclic experiment
edp = [2, 0.2, 0.5]                  # cyclic experiment displacement prescription - unloading  (disp, increment below, increment above)


""" Default values for plot. """

plotdim =  '0 10 0 7'                # XY plot bounds (xmin xmax ymin ymax)

tlw = 2                              # target line width
elw = 0.8                            # experiment line width

ppd = 0                              # plot point data (intersections, locMaxs)      1 = True, 0 = False
pce = 1                              # plot color experiment
out = 1                              # plot targets with outline



rcParams['font.family'] = 'serif'
rcParams['font.sans-serif'] = 'Times'
rcParams['font.size'] = 9
rcParams['figure.figsize'] = 5,4

#==================================================================
# F U N C T I O N S  (22)   
#==================================================================

def chooseDir(cesta, x):
    """ Gets folder name and file list in it. """
    app = wx.PySimpleApp()    
    if x == 0:
      dialog0 = wx.DirDialog(None, "Choose a directory:", defaultPath=cesta, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
      if dialog0.ShowModal() == wx.ID_OK:
          path = dialog0.GetPath()
      dialog0.Destroy()
    else:
      dialog1 = wx.DirDialog(None, "Choose a directory with CSV file of averaged TS experiment:", defaultPath=cesta, style=wx.DD_DEFAULT_STYLE)
      if dialog1.ShowModal() == wx.ID_OK:
          path = dialog1.GetPath()
      dialog1.Destroy()
    
    os.chdir(path)
    fL = os.listdir(path)
    
    for filename in fL:                                 #  renames 1.TRA to 01.TRA etc.
        if len(filename) == 5:
            os.rename(filename, "0"+filename)
    
    fL = os.listdir(path)
    fileList = []
    for i in fL: 
        fileList.append(str(i))
    folderName = path.split('\\')
    folderName = folderName[-1]
    
    return folderName, fileList, path
    
def splitDict(input_dict, chunks, keys):
    """ Splits dict by "keys". Returns lists of dictionaries by experiment group. """ 
    return_list = [dict() for idx in xrange(chunks)]    # creates empty dicts
    
    for i in range(chunks):
        for j in range(len(keys[i])):
            key = keys[i][j]
            return_list[i][key] = input_dict[key]
    return return_list    

def dump_data (dict) :
    if cyclic == 1:
       fn = 'exp.dac'
    else:
       fn = 'exp.dat'
    
    with open(fn,'wb') as data:
        pickle.dump(dict, data)
        data.close()
    

def read_info():
    import experiment_info as e_i
    
    e_c                             = {}
    e_c['info']                     = {}
    e_c['info']['set_of_specimens'] = e_i.d['set_of_specimens']
                                      
    vektor_informaci                = e_i.d.keys()
    vektor_informaci.remove('set_of_specimens') 
    
#     print(len(vektor_informaci), vektor_informaci)
            
    for iname in vektor_informaci:
        e_c['info'][iname] = {}
        for set in e_i.d['set_of_specimens']:
            e_c['info'][iname][str(set)] = e_i.d[str(iname)][str(set)]
    
    return e_c 

def print_dict_tree(d,level):
    

    empty_string=''
    for i in range(0,5*level):
        empty_string=empty_string+' '

    for key in d.keys():

        print("%s[%s]" % (empty_string,key))

        if isinstance(d[key], dict):

            print_dict_tree(d[key],level+1)

    
def getTraData( filename ):
    """ Imports TRA (CSV) data to dict of lists. """
    
    with open(filename, 'rb') as n:
        d = csv.Sniffer().sniff(n.readline(), [' ',';','; '])    #sniffs correct delimeter from suggestions in []
        n.seek(0)
        reader = csv.DictReader(n, dialect=d)
    
        results = {}
    
        for row in reader:                        #for i in kn -> i holds the value, not index
            for col in row.keys():
                coldata = row[col]
                
                results.setdefault( col, []).append( coldata )
        
        rnm = ['Sila [N]','Deformace nominalni [mm]','Deformace [mm]','Cas [s]']
        fstr = ['Standardn\xed sn\xedma\xe8 F', 'Nomin\xe1ln\xed deformace', 'Deformace', '\xc8as trv\xe1n\xed zkou\x9aky']
        kn = []
        kn = results.keys()                       #keys saved to list because dict IS orderless
#         print "kn ="
#         print kn

        for i in range(len(kn)):            
          del results[kn[i]][0]                 #removing first values of value lists (units)
        return results

def colgen():
    col = (np.random.rand(3,1))                                         #random line color
    col = tuple(col.reshape(1,-1)[0])                                   #makes rgb tuple
    return col

def easyPlot( eps, sila, n, color ):
    """ Plots curve using MatPlotLib. """
#     t = 1000
#     sila = [v/t for v in sila]
#     
#     eps = np.array(eps)
#     sila = np.array(sila)
    col = color[0]
    plt.figure(1)
    plt.plot(eps, sila, color)       #x,z,linestyle, linewidth, markersize
    plt.text(eps[-1], sila[-1], str(n), color=col, fontsize=8)

def plotPointData( eps, sila, col ):
    """ Plots colorfull background experiment curve using MatPlotLib. """
    t = 1000
    sila = map(float, sila)    #str to float
    sila = [x/t for x in sila]
    plt.figure(1)
    plt.plot(eps, sila, col, ms=3)       #x,z,linestyle, linewidth, markersize

def plot11TraData( eps, sila, col ):
    """ Plots colorfull background experiment curve using MatPlotLib. """
    t = 1000
    sila = map(float, sila)    #str to float
    sila = [x/t for x in sila]
    plt.figure(1)
    plt.plot(eps, sila, color=col, lw=elw, ms=1)       #x,z,linestyle, linewidth, markersize
    
def plot1TraData( eps, sila ):
    """ Plots grey background experiment curve using MatPlotLib. """
    t = 1000
    sila = map(float, sila)    #str to float
    sila = [x/t for x in sila]
    plt.figure(1)
    plt.plot(eps, sila, 'r-', lw=2, ms=1, color='0.85')       #x,z,linestyle, linewidth, markersize
#     plt.plot(eps, sila, 'ro', lw=5, ms=5)

def plot2ATraData( eps, sila, n ,color):
    """ Plots averaged curve using MatPlotLib. """
    t = 1000

    sila = [x/t for x in sila]
    eps  = [e*t for e in eps]     #plot in mm
    plt.figure(1)
    
#     plt.text(eps[-1], sila[-1], str(angle)+"$^\circ$", color='r', fontsize=8)
    
    if len(color) > 2:
        col = (0.0,0.0,0.0)
        if out: plt.plot(eps, sila, color=col, lw=tlw, ms=1)   # black outline
        plt.plot(eps, sila, color, lw=tlw-0.6, ms=1)
                        
    else:
        col = (0.0,0.0,0.0)
        if out: plt.plot(eps, sila, color=col, lw=tlw, ms=1)   # black outline
        plt.plot(eps, sila, color, lw=tlw-0.6, ms=1)
#         plt.plot(eps, sila, color, lw=1, ms=1) 
        
    col = color[0]
    if angles == 0:
        angle=n                                               #if angle=x plots max. value
#         plt.text(eps[-1]+0.01, sila[-1], str(angle), color='k', fontsize=8)
    else:
        angle=n*15
#         plt.text(eps[-1]+0.01, sila[-1], str(angle)+"$^\circ$", color='k', fontsize=8)
    plt.plot(eps[-1], sila[-1], 'g.')                    #ending point

def plot3Poly( eps, sila, degree ):
    """ Plots interpolated slopes for cyclic using MatPlotLib and NumPy. """
    t = 1000
    sila = [x/t for x in sila]
    x = np.array(eps)
    y = np.array(sila)
    z = np.polyfit(x, y, degree)
    p = np.poly1d(z)
    x_new = np.arange(min(x), max(x)+0.5,0.1)
    plt.figure(1)
    plt.plot(x_new, p(x_new), 'r-')       #x,z,linestyle, linewidth, markersize
#     plt.plot(x, y, 'bo',x, p(x), 'g-')
       
def makeFigure(name, path, var, png, pdf):
    """ Makes final figure and exports PNG file. """    
    os.chdir(path)
    plt.grid(True)
    plt.xlabel('$\Delta l$ [mm]')
    plt.ylabel('$F$ [kN]')
    dim = plotdim.split()
    dim = [float(pd) for pd in dim]
    plt.axis(dim)

#     plt.axis([0, 20, 0, 30]) #plot axis xmin xmax ymin ymax
#     plt.autoscale(axis='x')
    plt.suptitle(name, fontsize=12)
    if png == 1:
        plt.savefig(name+var+'.png', dpi=180, format='png')                           #SAVEFIG!
    if pdf == 1:
        plt.savefig(name+var+'.pdf', format='pdf')
    
    

def getStrPoint(eps, sila, num):
    """ Determines strength point from TS averaged data. """ 
    dict = {}
    fwidth = 12.7080                                             # highly dependent on precision! recommended. prec = 10 
    count = 0 
    index, value = max(enumerate(sila), key=operator.itemgetter(1))    # gets id and val of global maximum
    dict['strength'] = {'displacement': eps[index],'force': value}
#     easyPlot([eps[index]],[value/1000], '', 'rx')
#     print(eps,sila)
#     try:                                                 
#         testval = sila[index+1]                                  # checks if the id of max = list[-1]
#         while (abs(sila[index+count]-sila[index+count+1]) < fwidth):    # finds 'some' point after glob max - maybe later
#             count = count + 1
#     except IndexError:
#         print('') 
#                                                                     
#     easyPlot([eps[index+count]],[sila[index+count]/1000], 'o', 'rx')    
    if num==0: return dict
    else: return index

def dde_conversion(lop, edp):
    """ Takes list of list of pairs and creates single list with first values of pairs only. These are corrected according 
    cyclic experiment displacement prescription. """    # IS that correct? slope upper point xval != locMax
    
    flop = [ pair[0] for pair in lop]
    
    cunter = 1
    cunter2 = 1
    for id, xvalup in enumerate(flop):
        if round(xvalup) <= edp[0]:
           flop[id] = lastD = cunter*edp[1]
           cunter += 1
        else:
           flop[id] = lastD + cunter2*edp[2]
           cunter2 += 1 
     
    return flop      
    
        
    
def averageCyclic(dataDict, fileList, expG, expC, cG):
    """ Calculates lists of x,y for averaged envelope curve and slopes for TRA with cyclic experiment data.""" 
    avgfln = 'averaged_k.csv'
    precis = 1
    
    tradict = {}                                     # dicts for expdat pickle.dump (saves filtered TRA data)
    tardict = {}                                                 
    strdict = {}
    tendict = {}
    tecdict = {}                                     # TS envelope curve ex TC 
    tandict = {}
    
    #preparing data

    for i in range(1,expC+1):
        vars()['trD'+str(i)] = dataDict[fileList[i-1]]['Deformace']
        vars()['trD'+str(i)] =  map(float, vars()['trD'+str(i)])                #converts list to float
        vars()['trF'+str(i)] = dataDict[fileList[i-1]]['Standardn\xed sn\xedma\xe8 F']
        vars()['trF'+str(i)] =  map(float, vars()['trF'+str(i)])                #converts list to float
#         print "TRA_"+str(i)+":"
#         print vars()['tra'+str(i)]
       
    for i in range(1,expC+1):                                                   #cuts off the trF list
        vars()['cnD'+str(i)] = min(enumerate(vars()['trD'+str(i)]), key=lambda x:abs(x[1]-rand))   
        #gets closest value and its position for cutoff from trD list
        
        del vars()['trD'+str(i)][:vars()['cnD'+str(i)][0]]                      #cuts off the trD list
        del vars()['trF'+str(i)][:vars()['cnD'+str(i)][0]]
        

        #first TRA in group is master TRA trD1 
        #(takes closest values from other experiments to value in first TRA in experiment group)                                             
        #for choosing another master TRA just swap first TRA file or here swap trD1 with another trDi

    if cyclic:                                     

       x_point_data = []
       Target_sD = []
       Target_sF = []
       risingF=[]
       risingD=[]
       slope_counts = []
       lowerFbound2 = 10     # for finding the lowest point of the loop
       inf_gap = 0           # minimum gap between two infexion points, do it in LCHK!
       if pas: 
        for i in range(1,expC+1): 
          points = locMax(vars()['trD'+str(i)], vars()['trF'+str(i)], inf_gap )     #  gets locMax points (loops)
           
#           print ("trDi_inflex (risingD)")
#           print (points[0])
#           print ("trFi_inflex (risingF)")
#           print (points[1])
#           print("index")
#           print(points[2])                  
#           print("index2")
#           print(points[3])
          
          ids_to_remove_from_points23 =[]
          diffFo = 3333
          for j in range(len(points[3])):           # cycle loop check !!!      LCHK
            index = points[2][j]
            index2 = points[3][j]
            loopF = vars()['trF'+str(i)][index:index2]
            loopD = vars()['trD'+str(i)][index:index2]
#             plot2ATraData(loopD, loopF, i, 'r-')
             
#             plot2ATraData(eps_up, sila_up, j, 'r-')
            diffFc = abs(vars()['trF'+str(i)][index]-vars()['trF'+str(i)][index2])  
            #difference of sila in two following indexes
            isLoop = False
            for val in loopF:
                if val < 200 :                       # and diffFc < 2*diffFo  l_point found => loop check OK!
                   isLoop = True
                   break
            if isLoop == False:                      # l_point NOT found => bad exp data!
                   ids_to_remove_from_points23.append(j)
                   print("*Weird expdata at ",str(i+(cG)*expC),". TRA!*") 
            diffFo = diffFc
#           print ids_to_remove_from_points23
#           plt.show()
          rcount = 0           # cleans the data! arrgh! (gets rid of pseudo loops from exp data imperfections)
          for id in ids_to_remove_from_points23:
                points[2].pop(id-rcount)
                points[3].pop(id-rcount)            
                rcount +=1            
            
#           if maketscurve == 1:                      #  gets points for averaged TS curve from TC exp. data (ex locMax)
          rF = [0]+[vars()['trF'+str(i)][cv] for cv in points[2]]
          rD = [0]+[vars()['trD'+str(i)][cv] for cv in points[2]]
          
          if ppd: plotPointData(rD,rF, 'ro')                        # plots locMaxs after filtration
          
          risingD.append(rD)
          risingF.append(rF)
          
          vars()['riD'+str(i)] = rD                            # saving list for dict expdat
          vars()['riF'+str(i)] = rF
          
          Target_sD = []
          Target_sF = []
          
          lowD = []
          lowF = []
          
          for j in range(len(points[3])):           
            index = points[2][j]
            index2 = points[3][j]

            loopF = vars()['trF'+str(i)][index:index2]   #slicing out the loop
            loopD = vars()['trD'+str(i)][index:index2]
#             plot2ATraData(loopD, loopF, j, 'r-')      #plots the loop
           
            lowestF = min(enumerate(loopF), key=lambda x:abs(x[1]-lowerFbound2))
            index3 = lowestF[0]           #index of the lowest point in the loop
            loopD2 = [loopD[index3]]; loopF2 = [loopF[index3]]
            l_point = [loopD2, loopF2]    #xval, yval of lowest point of cycle loop
            
            lowD.append(loopD2)
            lowF.append(loopF2)
                    
            eps_down  = vars()['trD'+str(i)][index:(index3+index-1)]
            sila_down = vars()['trF'+str(i)][index:(index3+index-1)]
            eps_up  = vars()['trD'+str(i)][(index3+index):index2+1]
            sila_up = vars()['trF'+str(i)][(index3+index):index2+1]

#             plot2ATraData(eps_down, sila_down, j, 'g-')      #plots falling part of the loop
#             plot2ATraData(eps_up, sila_up, j, 'r-')          #plots rising part of the loop
                        
            i_point = find_intersect2(eps_down,sila_down, eps_up, sila_up)   # this is the MAGIC!
#             print cG, i, str(cG*expG+i), j
#             print l_point
#             print i_point
            
            if i_point.any() == False:      # if no intersection found > end of exp!?
                break
            else:
                x_point = [[i_point[0][0],l_point[0][0]],[i_point[0][1]/t,l_point[1][0]/t]]
                if ppd: plotPointData(x_point[0],[i_point[0][1],l_point[1][0]], 'rx')        # plots intersections and lopoints
                
# """ Here begins the slope averaging. """
            Target_sD.append(x_point[0])        
            Target_sF.append(x_point[1])            
#             print str(i)+"/"+str(j)+"."
#             print Target_sD
            vars()['sD'+str(i)] = [Target_sD]            
            vars()['sF'+str(i)] = [Target_sF]
            
            vars()['loD'+str(i)] = lowD            
            vars()['loF'+str(i)] = lowF
#             saveData( [lowD, lowF], cG, 'lodata'+str(i)+'.csv')
            csc = len(Target_sD)             # slope count in current TRA

          try:
              slope_counts.append(csc)           # slope counts in TRAs of current expGroup
          except UnboundLocalError:
              print('*No loop found - TRA files for cyclic experiment used?*')
              sys.exit(1) 
#           print(slope_counts)
#           if slope_count >= csc:
#               slope_count = csc
#               print slope_count
            
#           print 'sD'+str(i)
#           print vars()['sD'+str(i)]
#           print vars()['sF'+str(i)]
       aSlopesD = []
       aSlopesF = []
       
       for b in range(min(slope_counts)):
          avg_sD = []
          avg_sF = []
          for traa in range(1,expC+1):   
              avg_sD.append(vars()['sD'+str(traa)][0][b])
              avg_sF.append(vars()['sF'+str(traa)][0][b])
          asD = averageLists(avg_sD, expC, 0)
          asF = averageLists(avg_sF, expC, 0)
          aSlopesD.append(asD)                               # saving upper and low slope point x values
          aSlopesF.append(asF)                               # saving upper and low slope point y values
#           print asD
#           print asF
#           print b
          
          eps = np.array(asD)
          sila = np.array(asF)
    
          plt.figure(1)
#           if pas: plot2ATraData(eps, sila, b, 'r-')    
          if pas and out: plt.plot(eps, sila, color=(0.0,0.0,0.0), lw=tlw, ms=1)
          if pas: plt.plot(eps, sila, 'r-', lw=tlw-0.6, ms=1)                          # plots averaged slope  (0.0,0.44,0.75)

#        print 'asD'
#        print aSlopesD
#        print 'asF' 
#        print aSlopesF
      
       
       tar_slopes = []
       for (defo, forc) in zip(aSlopesD, aSlopesF):      # gettin k finally! and zip magic!
#            print defo, forc
           dx = defo[0]-defo[1]
           dy = forc[0]-forc[1]
           slope = dy/dx
           a0 = (defo[0],forc[0])
           a1 = (defo[1],forc[1])
           tar_slopes.append((a1, a0, slope))

       saveData( tar_slopes, cG, avgfln)       # save averaged k   0
       
      
# """ Here ends the slope averaging. """

       TS_D = averageLists(risingD, expC, 0)
       TS_F = averageLists(risingF, expC, 0)                      
                                                         
       TS_D = [ddd/1000 for ddd in TS_D]                 # converting mm to m
       tar_slopes_k = [kk[2] for kk in tar_slopes]       # list with slopes only
       

#        if dde: aSlopesDu = dde_conversion(aSlopesD)          # if displacement driven cyclic experiment - known unload points
                                                               
       if dde: unloadPointsD_exp = dde_conversion(aSlopesD, edp)    # saving only upper slope point x value and correcting to edp                                                  
       if dde: unloadPointsD_exp = [ddd/1000 for ddd in unloadPointsD_exp]
#        if dde: saveData( unloadPointsD_exp, cG, "unloadPoint_exp.csv")       
#        if dde: saveData( aSlopesD, cG, "unloadPoint_exp.csv")

       tecdict['tensile'] = {'displacement': TS_D,'force': TS_F}
       strdict['strength'] =  {'displacement': TS_D[-1],'strength': TS_F[-1]} # strenghth target ex TC
#        tandict['TANGENT'] = {'displacement': aSlopesD,'force': aSlopesF, 'slope': tar_slopes}
       tandict['tangent'] = {'displacement': unloadPointsD_exp, 'tangent': tar_slopes_k} 
       tardict['target'] = tandict       
       tardict['target'].update(strdict)
       tardict['target'].update(tecdict)
#        print(tardict)
       
       
#        expdat[dstep+cG*dstep] = tardict                      #first 0deg and last 90deg experiments are not cyclic
       expdat[str(cG*dstep)] = tardict                      #first 0deg and last 90deg experiments are cyclic

       for i in range(1,expC+1):                            # saving raw TRA data
       
           vars()['trD'+str(i)] = [ddd/1000 for ddd in vars()['trD'+str(i)]]       # converting mm to m
           vars()['riD'+str(i)] = [ddd/1000 for ddd in vars()['riD'+str(i)]]          
#            print(vars()['loD'+str(i)])
           vars()['loD'+str(i)] = [ddd[0]/1000 for ddd in vars()['loD'+str(i)]]
                       
           tradict[fileList[i-1]]= {'displacement': vars()['trD'+str(i)][0::precis] , 'force': vars()['trF'+str(i)][0::precis], 'force_top': vars()['riF'+str(i)] , 'displacement_top': vars()['riD'+str(i)], 'force_bottom': vars()['loF'+str(i)] , 'displacement_bottom': vars()['loD'+str(i)]}                                      #   , 'force_failure': , 'displacement_failure': 
           
#            expdat[dstep+cG*dstep].update(tradict)
           expdat[str(cG*dstep)].update(tradict)       
       
#        easyPlot([TS_D[-1]], [TS_F[-1]/1000], cG+1, 'rx')     #plots strength point of aproximated TC (top point of last avg. slope)

    if cyclic and maketscurve:                                     #if requested plots approximated TS curve (0.0,0.44,0.75)
          plot2ATraData (TS_D, TS_F, cG+1, 'g-')
#           plot3Poly (TS_D, TS_F, 3)                        #making interpolation does not have sense!
    
    return avgfln
    
def averageTensile(dataDict, fileList, expG, expC, cG, precision):
    """ Calculates lists of x,y for averaged tensile curve for TRA with simple tensile experiment data.""" 
    
    tradict = {}                                     # dicts for expdat pickle.dump (saves filtered TRA data)
    tardict = {} 
    strdict = {}                                                
    tendict = {}

    
    if interav ==1:                                  # accepts values < 1 for interval averaging
      precis = 1
    else:
      precis = int(precision)

    for i in range(1,expC+1):
        vars()['trD'+str(i)] = dataDict[fileList[i-1]]['Deformace']
        vars()['trD'+str(i)] =  map(float, vars()['trD'+str(i)])                #converts list to float
        vars()['trF'+str(i)] = dataDict[fileList[i-1]]['Standardn\xed sn\xedma\xe8 F']
        vars()['trF'+str(i)] =  map(float, vars()['trF'+str(i)])                #converts list to float
#         print "TRA_"+str(i)+":"
#         print vars()['tra'+str(i)]
       
    for i in range(1,expC+1):                                                   #cuts off the trF list
        vars()['cnD'+str(i)] = min(enumerate(vars()['trD'+str(i)]), key=lambda x:abs(x[1]-rand))   
        #gets closest value and its position for cutoff from trD list
        
        del vars()['trD'+str(i)][:vars()['cnD'+str(i)][0]]                      #cuts off the trD list
        del vars()['trF'+str(i)][:vars()['cnD'+str(i)][0]]
        
    vars()['trD1'] = vars()['trD1'][0::precis]       #takes every nth value for comparsion                                         
    vars()['trF1'] = vars()['trF1'][0::precis]   


        #first TRA in group is master TRA trD1 
        #(takes closest values from other experiments to value in first TRA in experiment group)                                             
        #for choosing another master TRA just swap first TRA file or here swap trD1 with another trDi
    
    if not cyclic:                                              #TS averaging begins !
      TargetD = []
      TargetF = []
#       TargetDint = []
#       TargetFint = []
      kD = []                                                    #slope for TS
      kF = []
      
#       if interav == 1:   precis = 1                              #TS interval averaging  
      if interav == 1:  
        avgfln = 'averaged_int.csv'
        pdim = plotdim.split()
        pdim = [int(pd) for pd in pdim]
        eps_range = pdim[1]
        prec = float(precision)
        chunkks = int(eps_range/prec)
        cInt = [een*prec for een in range(chunkks)] 
        print('*Using averaging TS per interval size ',str(prec),'*!')

        for n, vallue in enumerate(cInt):                         # TS interval averaging begins 
              closestD = min(enumerate(vars()['trD1']), key=lambda x:abs(x[1]-vallue))
              sumDi = closestD[1]
              sumFi = vars()['trF1'][closestD[0]]
              for a in range(2,expC+1):
                  TtraDi = min(enumerate(vars()['trD'+str(a)]), key=lambda x:abs(x[1]-vallue))
#                   print TtraDi
                  sumDi += TtraDi[1]
                  TtraFi = vars()['trF'+str(a)][TtraDi[0]] #gets adequate force - y-value at same position in TRA as dl
#                   print TtraFi
                  sumFi += TtraFi                                      
              TnDi = sumDi/expC
              TnFi = sumFi/expC
              TargetD.append(TnDi)
              TargetF.append(TnFi)      
      
      else:                                                        #TS 2D averaging (default)
        avgfln = 'averaged.csv'
        for n, value in enumerate(vars()['trD1']):                 #trD1 master for comparing values !
              sumD = value
              sumF = vars()['trF1'][n]
#               print sum                                                                         
              for a in range(2,expC+1):
                  TtraD = min(enumerate(vars()['trD'+str(a)]), key=lambda x:abs(x[1]-value))
#                   print TtraD
                  sumD += TtraD[1]
                  TtraF = vars()['trF'+str(a)][TtraD[0]] #gets adequate force - y-value at same position in TRA as deformation
#                   print TtraF
                  sumF += TtraF                                      
              TnD = (sumD/expC)/1000                               #displacement in meters!
              TnF = sumF/expC
              TargetD.append(TnD)
              TargetF.append(TnF)



    
      tar_data = [TargetD, TargetF]
      saveData( tar_data, cG, avgfln)                              #saving averaged curves to csv as a dict
      
      
      strdict = getStrPoint(TargetD, TargetF, 0)
      maxindex = getStrPoint(TargetD, TargetF, 1)   
                  
      tendict['tensile'] = {'displacement': TargetD[0:maxindex+1],'force': TargetF[0:maxindex+1]}  #saving averaged curves till max
      tardict['target'] = tendict
      tardict['target'].update(strdict)
      
#       print(tardict)
      
      expdat[cG*dstep] = tardict
      
      for i in range(1,expC+1):
      
         vars()['trD'+str(i)] = [ddd/1000 for ddd in vars()['trD'+str(i)]]   # converting mm to m
         
         tradict[fileList[i-1]]= {'displacement': vars()['trD'+str(i)][0::precis] , 'force': vars()['trF'+str(i)][0::precis]}
         expdat[cG*dstep].update(tradict)

      if maketscurve: plot2ATraData( TargetD, TargetF, cG, 'g-' )            # plots averaged tensile curve

      return avgfln
      
def func(x,a,b,c):
    return a*np.exp(-b*x)+c
    
def find_intersect(x_down, y_down, x_up, y_up):
    """Finds intersection points of cycle loops (x_point) and returns its coordinates."""
    for j in xrange(len(x_down)-1):
        p0 = np.array([x_down[j], y_down[j]])
        p1 = np.array([x_down[j+1], y_down[j+1]])
        for k in xrange(len(x_up)-1):
            q0 = np.array([x_up[k], y_up[k]])
            q1 = np.array([x_up[k+1], y_up[k+1]])
            params = np.linalg.solve(np.column_stack((p1-p0, q0-q1)),
                                     q0-p0)
            if np.all((params >= 0) & (params <= 1)):
                return p0 + params[0]*(p1 - p0)

def find_intersect2(x_down, y_down, x_up, y_up):
    """Finds intersection points of cycle loops (x_point) and returns its coordinates. Vector and far quicker form."""
    p = np.column_stack((x_down, y_down))
    q = np.column_stack((x_up, y_up))
    p0, p1, q0, q1 = p[:-1], p[1:], q[:-1], q[1:]
    rhs = q0 - p0[:, np.newaxis, :]
    mat = np.empty((len(p0), len(q0), 2, 2))
    mat[..., 0] = (p1 - p0)[:, np.newaxis]
    mat[..., 1] = q0 - q1
    mat_inv = -mat.copy()
    mat_inv[..., 0, 0] = mat[..., 1, 1]
    mat_inv[..., 1, 1] = mat[..., 0, 0]
    det = mat[..., 0, 0] * mat[..., 1, 1] - mat[..., 0, 1] * mat[..., 1, 0]
    mat_inv /= det[..., np.newaxis, np.newaxis]
    import numpy.core.umath_tests as ut
    params = ut.matrix_multiply(mat_inv, rhs[..., np.newaxis])
    intersection = np.all(np.all((params >= 0) & (params <= 1), axis=-1), axis=-1)
#     intersection = np.all((params >= 0) & (params <= 1), axis=(-1, -2))             #numpy 1.7
    p0_s = params[intersection, 0, :] * mat[intersection, :, 0]
#     print 'p0_s ',p0_s 
    return p0_s + p0[np.where(intersection)[0]]    

def averageLists(list_of_lists, expC, chk):
    """ Makes averaged list from list_of_lists. If needed, all lists are sliced to length of smallest one."""
    avgList = []
    avglen = 0
    dl = len(list_of_lists)
    check = True
    
    for k in range (dl):
      avglen += len(list_of_lists[k])  
    avglen /= dl
    
    minlen = min(len(el) for el in list_of_lists )
    maxlen = max(len(el) for el in list_of_lists )
    if minlen != maxlen:
      list_of_lists = [li[0:minlen] for li in list_of_lists]
                                
    if chk == 1:                             #  check if count of values in lists = experiment count
      if expC == avglen:
          check = True
      else:
        check = False
        print("*AvgLists Fail!*")    
    
    if check == True:
      for i in range(len(list_of_lists[0])):
        sum = 0
        for j in range (dl):
            sum += list_of_lists[j][i]
#             print sum    
        avg = sum/len(list_of_lists)
        avgList.append(avg)
    
    return avgList 
        
def makeStats(dataDict, fileList, expG, expC, cG, precision):
    """ Makes stats table with averaged Fmax, lmax and deviations."""
    maxD = []
    maxF = []                                                                #cutoff value               
    for i in range(1,expC+1):
        vars()['trD'+str(i)] = dataDict[fileList[i-1]]['Deformace']
        vars()['trD'+str(i)] =  map(float, vars()['trD'+str(i)])                #converts list to float
        vars()['trF'+str(i)] = dataDict[fileList[i-1]]['Standardn\xed sn\xedma\xe8 F']
        vars()['trF'+str(i)] =  map(float, vars()['trF'+str(i)])                #converts list to float
                                                                     
        vars()['cnD'+str(i)] = min(enumerate(vars()['trD'+str(i)]), key=lambda x:abs(x[1]-rand))   
        del vars()['trD'+str(i)][:vars()['cnD'+str(i)][0]]                                         
        del vars()['trF'+str(i)][:vars()['cnD'+str(i)][0]]
#         print "TRA_"+str(i)+":"
#         print vars()['trD'+str(i)]
        
        mD = max(vars()['trD'+str(i)])
        mF = max(vars()['trF'+str(i)])
        maxD.append(mD)
        maxF.append(mF)

    maxD = np.array(maxD)
    maxF = np.array(maxF)
#     avgF1 = [maxF.mean()/t,maxF.std()/t]
#     avgD1 = [maxD.mean(),maxD.std()]
    avgF = [math.ceil((maxF.mean()/t)*100)/100,math.ceil((maxF.std()/t)*100)/100]
    avgD = [math.ceil((maxD.mean())*100)/100,math.ceil((maxD.std())*100)/100]
    saveData( avgF+avgD, cG, "averaged_max.csv")
    
    plt.figure(1)
    plt.plot( avgD[0], avgF[0],'gx')
    if angles == 0:
        angle=cG                                               #if angle=x plots max. value
        plt.text(avgD[0], avgF[0], str(angle), color='g', fontsize=8)
    else:
        angle=cG*15
        plt.text(avgD[0], avgF[0], str(angle)+"$^\circ$", color='g', fontsize=8)
    
            
      
def saveData(data, key, name):
      w = csv.writer(open(name,"a+"))
      w.writerow([key,data])
#       print '*Saving data to '+name+' !*'

def locMax(eps, sila, n):
    """ Finds loc maxs of loops in experiment data and returns its values and indices."""
    risingF = []
    risingD = []
    loc_max_index = []
    loc_max_index2 = []
    
    # gets indices of all inflection points! yes just that!
    sila_flips = np.where(np.diff(np.diff(sila) > 0))[0] + 1 
    
#     lowerFbound = 400
    for k,val in enumerate(sila_flips):   # filtering the lower points (locMin), theese are obtained easy way
      epsC = eps[val]
      silaC =  sila[val]
      if silaC > lowerFbound :  #and val-sila_flips[k-1] >= n next inflexpoint can be first after n points, in LCHK!    
#         plt.plot( epsC, silaC/1000, 'rx')      #plot inflexpoints
        risingD.append(epsC)
        risingF.append(silaC)
        loc_max_index.append(val)
    loc_max_index2 = [(id1 - 1) for id1 in loc_max_index]
    loc_max_index2 = loc_max_index2[1:]
#     plt.show()                           # check the inflex points
    return risingD, risingF, loc_max_index, loc_max_index2

        
def minDiff(eps, sila):
    from itertools import combinations
#     for i in range(1,81):
#     closest_pair = min((abs(x-y),(i,j)) for (i,x),(j,y) in combinations(enumerate(sila), 2))

    cp = [((abs(x-y)>0.1)<0.5,(i,j)) for (i,x),(j,y) in combinations(enumerate(eps), 2) ]
    cp2 = []

    for i in range(len(cp)):
        if  cp[i][0] == True:
            cp2.append(cp[i][1])
    slopeF = []
    slopeD = []
    for n in range(len(cp2)):
            slopeF = [sila[cp2[n][0]],sila[cp2[n][1]]]
            slopeD = [eps[cp2[n][0]],eps[cp2[n][1]]]
#             print slopeF, slopeDr[0]-slopeD[1]
#             if abs(slopeD[0]-slopeD[1]) <= 0.05: 
    return slopeF, slopeD
#             plot3TraData(slopeD, slopeF)
#             print "point added"
      


#==================================================================
# G U I  C L A S S
#==================================================================

class MyDialog(tkSimpleDialog.Dialog):
    """ Triggers dialog for user input."""
    def body(self, master):
        Label(master, text="Experiment groups:").grid(row=0, sticky=W)
        Label(master, text="Specimen count:").grid(row=1, sticky=W)
        Label(master, text="Accuracy / int (TS):").grid(row=2, sticky=W)
        Label(master, text="XY bounds:").grid(row=3, sticky=W)
    
        self.e1 = Entry(master)
        self.e1.insert(0, "1")
        self.e2 = Entry(master)
        self.e2.insert(0, "3")
        self.e3 = Entry(master)
        self.e3.insert(0, "10")         #    10 is recommended (for determining strength)                
        self.e4 = Entry(master)
        self.e4.insert(0, "0 10 0 1")
#         self.e4.insert(0, "0 1 0 1")
                                                                       
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)\
        
        global interav
        global angles
        global cyclic
        global loadtscurve
        global maketscurve
        global zeroninety
        global statistics
        global wantpng
        global wantpdf
        global tslope
                
        interav = IntVar()        
        angles = IntVar()
        cyclic = IntVar()
        loadtscurve = IntVar()
        maketscurve = IntVar()
        zeroninety =  IntVar()
        statistics =  IntVar()
        wantpng =  IntVar()
        wantpdf =  IntVar()
        tslope =  IntVar()
        
        self.cb0 = Checkbutton(master, text="Average in intervals", variable=interav)
        self.cb0.grid(row=4, sticky=W)
        self.cb1 = Checkbutton(master, text="Angles", variable=angles)
        self.cb1.grid(row=4, sticky=W, column=1)
#         self.cb8 = Checkbutton(master, text="Slope ex TS", variable=tslope)
#         self.cb8.grid(row=5, sticky=W, column=1)
        
        self.cb2 = Checkbutton(master, text="Cyclic experiment", variable=cyclic)
        self.cb2.grid(row=6, sticky=W)
        self.cb3 = Checkbutton(master, text="Load TS curve", variable=loadtscurve)
        self.cb3.grid(row=6, sticky=W, column=1)
        self.cb4 = Checkbutton(master, text="TS curve ex TC", variable=maketscurve)
        self.cb4.grid(row=7, sticky=W, column=1)
#         self.cb5 = Checkbutton(master, text="0, 90 ex TS", variable=zeroninety)
#         self.cb5.grid(row=7, sticky=W, column=1)
        self.cb6 = Checkbutton(master, text="Statistics", variable=statistics)
        self.cb6.grid(row=9, sticky=W)
        self.cb7 = Checkbutton(master, text="Export PNG", variable=wantpng)
        self.cb7.grid(row=10, sticky=W)
        self.cb8 = Checkbutton(master, text="Export PDF", variable=wantpdf)
        self.cb8.grid(row=10, sticky=W, column=1)        
    
        self.cb1.select()
        
        self.cb4.select()
        self.cb2.select()
        
        self.cb7.select()
        self.cb8.select()
        
    def apply(self):
        global expGroups
        global expCount
        global precision
        global plotdim
        global angles
        global cyclic
        global loadtscurve
        global maketscurve
        global interav
        global zeroninety
        global statistics
        global wantpng
        global wantpdf
        global tslope

# pumping data out of gui 
        
        expGroups = int(self.e1.get())                    #groups of specimens (angles)
        expCount = int(self.e2.get())                     #experiment count for one group of specimens
#         precision = int(self.e3.get())                    #takes each nth point for average line
        plotdim = self.e4.get()                           #XY plot bounds
        precision = self.e3.get()
        angles = angles.get()                             #sets avg. curve description
        cyclic = cyclic.get()
        maketscurve = maketscurve.get()                   #adds rough target curve from locMax points of TC
        loadtscurve = loadtscurve.get()                   #loads data in averaged.csv file from selected TS
        interav = interav.get()                           #avg. TS at intervals defined by accuracy
#         zeroninety = zeroninety.get()                     #TC - zero and ninety degrees present (expect no loops!)
        statistics = statistics.get()                     #create stats table containing avg. Fmax, deltalmax and st.dev
        wantpng = wantpng.get()                           #export PNG
        wantpdf = wantpdf.get()                           #export PDF        
#         tslope = tslope.get()                             #plot first slope in TS

#         


#==================================================================
# S T A R T
#==================================================================
    
if __name__ == '__main__':    
   
    import sys
    import os
    import wx
    import time
    import tkMessageBox
    import collections
#     import odict
    
    rand = 0.005                                         #cutoff value                                      
    t = 1000                                             #y-divider (N to kN)
    lowerFbound = 400                                    #defines locMax filtering!!!
    lowerFbound2 = 10                                    #for finding the lowest point of the loop
    lowerFbound3 = 200                                   #loop check - is loop? is when got point with F below this
    tslopeFcut = 400                                     #at this value is chosen h_point of the slope for TS

    global dstep
    dstep = 15                                           #degree step of measured specimens
    
    root = Tk()                                                 
    root.withdraw()
                                                         #default paths for experimental data
                                                         
#     traPath = 'C:/Users/ptaeck/PY/exp/cykly-tah-sorted-nov'    #C:/Users/ptaeck/abaqus/PY/vysl/plotting/forexport/cykly/ex C:/Users/ptaeck/abaqus/PY/vysl/plotting/cykly-tah-sorted/90 testKunc-2012_10_22-tah-AU,  cykly/Kunc-2013_01_07-cykly-tah-CP0-90  C:/Users/ptaeck/abaqus/PY/vysl/plotting/cykly/testKunc-2013_01_07-cykly-tah-CP0-90
    tsPath = 'C:/Users/ptaeck/PY/exp/2012_11_01-tah-CP'

    dataDict = {}
    expdat = collections.OrderedDict()                            #dict for pickle.dump
#     expdat = odict.OrderedDict()
    
    fileInfo = chooseDir(traPath, 0)    #dirname, filelist, path
#     fileInfo = ['45', ['45_5.TRA','45_6.TRA','45_7.TRA'],'/server/home/kunc/documents/PY/plotra/45']

#     print fileInfo[2]              #path
    fileList = fileInfo[1]           #filelist
#     print fileList

    rn = []
    results = 0
                                                                 # DATACHECK!
    for filename in fileList:
        if filename.lower().endswith(('.csv','.png','.pdf','.dat','.dac','.txt')):
          results = 1
          rn.append(filename)
    
    if results == 1:
          if tkMessageBox.askyesno("Result files already present!", "Overwrite exp.dat file and result files ?"):
            print('Result data will be overwritten!')
            for resultName in rn:
                fileList.remove(resultName)
                os.remove(resultName)
          else:
            sys.exit(1)

   
    if gui:
        root.title("ploTra settings:")
        d = MyDialog(root)                                                          #triggers dialog for data input

        
         
    if expGroups*expCount ==  len(fileList):                                 #simple file check
        print("*TRA match!*")
    else:
        print("*TRA fail!*")
        sys.exit(1)
        


    for i,tra in enumerate(fileInfo[1]):
        col = colgen()
        vysl = getTraData(fileInfo[2]+'/'+tra)
        
        dataDict[tra] = vysl         #makes dict of dict (keys: 01.TRA, 02.TRA, ...)
#         print dataDict.keys()
#         plot1TraData( vysl['Deformace [mm]'], vysl['Sila [N]'] )
        if pce: plot11TraData( vysl['Deformace'], vysl['Standardn\xed sn\xedma\xe8 F'], col )       #plots raw data (greyed out)
        else: plot1TraData( vysl['Deformace'], vysl['Standardn\xed sn\xedma\xe8 F'] )
    group_keys=[fileList[x:x+expCount] for x in xrange(0, len(fileList), expCount)]   #split fileList to experiment groups
#     print group_keys
#     print dataDict
    dataGroupDict = splitDict(dataDict, expGroups, group_keys)                        #split dataDict to experiment groups
#     print dataGroupDict[0]
    
#     dump_data(dataGroupDict)

    if statistics == 1:
        
        for i in range(expGroups):
              suff = '_max'
              makeStats(dataGroupDict[i], group_keys[i], expGroups, expCount, i, precision)
        print('*Data saved to averaged_max.csv !*')
    
       
    for i in range(expGroups):
          suff = '_1'         
          if cyclic: avg = averageCyclic(dataGroupDict[i], group_keys[i], expGroups, expCount, i)
          if not cyclic: avg = averageTensile(dataGroupDict[i], group_keys[i], expGroups, expCount, i, precision)
    print('*Data saved to',avg,'!*')
        
        
    expinf = read_info()                      # reading file experiment_info.py

    expdic = {}
    expdic['data'] = expdat                   # saving exp dat dictionary to expdic
    expdic.update(expinf)                     # updating expdic dictionary with exp info

    saveout = sys.stdout                      # redirecting output for dict tree file exp.txt
    sys.stdout = open('exp.txt', 'w')
    print_dict_tree(expdic,0)
    sys.stdout = saveout
        
    dump_data(expdic)
 
              

    if cyclic == 1 and loadtscurve == 1:                                #loads TS curves to cyclic experiments
          ts_curve = chooseDir(tsPath,1)
          csvis = 0
          for filename in ts_curve[1]:
            if "csv" in filename: csvfile = filename; csvis = 1
          if csvis == 0: print("*CSV file not found!*")
          
          ts_data = {}
          for key, val in csv.reader(open(csvfile, "r")):
	          ts_data[key] = val
          for key in ts_data:
#             minus1 = -15
#             minus2 = -5
#             if key == "1":                                              #modding the line description position
#                ts = eval(ts_data[key])
#                plot2ATraData( ts[0][:minus1], ts[1][:minus1], int(key), 'g-' ) 
#             elif key == "2":                                              #modding the line description position
#                ts = eval(ts_data[key])
#                plot2ATraData( ts[0][:minus2], ts[1][:minus2], int(key), 'g-' )     
#             else:
               ts = eval(ts_data[key])
               plot2ATraData( ts[0], ts[1], int(key), 'g-' )
               
#           ts_curve = chooseDir(tsPath,1)                                #loading TS data from exp.dat
#           datis = 0
#           for filename in ts_curve[1]:
#             if "dat" in filename: datfile = filename; datis = 1
#           if csvis == 0: print("*DAT file not found!*")
#           
#           ts_data = {}
#           
#           f = open(datfile, "r")            
#           expdat = pickle.load(f)
#           f.close()
#           else:
#             expdat   = {}
#           print 'DAT not loaded.'          
             
              
    makeFigure(fileInfo[0], fileInfo[2], suff, wantpng, wantpdf)       #filename, path,  suffix, make png?
    #~ plt.show()
    print('*ploTra fin!*')
    
