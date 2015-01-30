from numpy import *
import sys
import collections
import textwrap
from time import gmtime, strftime

# vyberte verzi s merenymi orientacemi vlaken popr. vytvorte svou vlastni
set_of_specimens_version = 3
set_of_specimens_list =  {'1':['0','10','20','30','40','50','60','70','80','90'],
                          '2':['0','15','30','45','60','75','90'],
                          '3':['0','45','90'],
                          '4':['0']
                        }

d = collections.OrderedDict()
# d['default'] = {}
# zadejte jmena .TRA souboru (upravte pouze ty radky, ktere se tykaji vaseho experimentu)
d['name_of specimens'] = {'0':('0_1.TRA', '0_2.TRA', '0_3.TRA', '0_4.TRA'),
                         '10':('10_1.TRA', '10_2.TRA', '10_3.TRA'),
                         '15':('15_8.TRA', '15_9.TRA', '15_10.TRA'),
                         '20':('20_1.TRA', '20_2.TRA', '20_3.TRA'),
                         '30':('30_6.TRA', '30_7.TRA', '30_8.TRA'),
                         '40':('40_1.TRA', '40_2.TRA', '40_3.TRA'),
                         '45':('45_5.TRA', '45_6.TRA', '45_7.TRA'),
                         '50':('50_1.TRA', '50_2.TRA', '50_3.TRA'),
                         '60':('60_6.TRA', '60_7.TRA', '60_8.TRA'),
                         '70':('70_1.TRA', '70_2.TRA', '70_3.TRA'),
                         '75':('75_6.TRA', '75_7.TRA', '75_8.TRA'),
                         '80':('80_1.TRA', '80_2.TRA', '80_3.TRA'),
                         '90':('90_5.TRA', '90_6.TRA', '90_7.TRA')
                         }
# zadejte nejcastejsi konfiguraci

d['default'] = {'date_of_measuring'  :     '1.1.2015' ,
               'name_of_tester'     :     'Frantisek Tester' ,
               'material'           :     'skelna tkanina' ,
               'notes'              :     'Tkanina 3x Aeroglass 390g/m2, 0/90, matrice Epicote HGS LR285 + LH286' ,
               'temperature'        :     21 ,
               'grip_length'        :     100e-3 ,   # m
               'ext_length'         :     60e-3 ,    
               'total_length'       :     135e-3 ,   
               'thickness'          :     11e-4 ,    
               'width'              :     15e-3 ,
               'weigth'             :     15e-3,     # kg
               'cykly_spodni_uvrat' :     100.0,     # N
               'cykly_horni_uvrat'  :     1.0e-3 }   #'[0.2:0.2:2] mm'            



saveout = sys.stdout                      # redirecting output to file exp_info.py
sys.stdout = open('exp_info.py', 'w')

print textwrap.dedent("""#!/usr/bin/python    
#exp_info.py - editable template for ploTRA experiment analysis
#This file was generated on %s""") %strftime("%Y-%m-%d %H:%M:%S", gmtime()) 

print '\nimport collections'
print 'd0 = collections.OrderedDict()'
print 'd1 = collections.OrderedDict()'

for id in set_of_specimens_list[str(set_of_specimens_version)]:
    print '\n#==================='
    print '# %s GROUP EXP INFO ' %(id)
    print '#===================\n'
    for tra in d['name_of specimens'][id]:
#         print  '#*** %s ***' %(tra)
        print 'd1[\'%s\'] = {' %tra
        for key in d['default']:
            if type(d['default'][key])==type(str()):
                print '                 \'%s\' :\'%s\',' %(key,d['default'][key])
            else:
                print '                 \'%s\' :%s,' %(key,d['default'][key])  
        print '                 }'

    print '\nd0[\'%s\'] = d1' %id
    print 'd1 = collections.OrderedDict()' 
# print '\nprint  d0[\'0\'][\'0_4.TRA\'].keys()'
# print '\nprint  d0[\'90\'].keys() '
# print '\nprint  d0[\'90\'][\'90_7.TRA\'].keys()'
sys.stdout = saveout
