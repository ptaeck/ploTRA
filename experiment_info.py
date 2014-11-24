from numpy import *

# vyberte verzi s merenymi orientacemi vlaken popr. vytvorte svou vlastni
set_of_specimens_version = 2
set_of_specimens_list =  {'1':array([0,10,20,30,40,50,60,70,80,90]),
                          '2':array([0,15,30,45,60,75,90]),
                          '3':array([0,45,90]),
                          '4':array([0])
                        }
d                      = dict()
# d['set_of_specimens']  = dict()
d['set_of_specimens']  = set_of_specimens_list[str(set_of_specimens_version)]

# upravte jmena zdrojovych .TRA souboru u orientaci, ktere se tykaji Vaseho mereni
d['name_of_specimens'] = dict()
d['name_of_specimens'] = {'0':('0_5.TRA', '0_4.TRA', '0_7.TRA'),
                        '10':('10_1.TRA', '10_2.TRA', '10_3.TRA'),
                        '15':('15_8.TRA', '15_9.TRA', '15_10.TRA'),
                        '20':('20_1.TRA', '20_2.TRA', '20_3.TRA'),
                        '30':('30_6.TRA', '30_7.TRA' , '30_8.TRA'),
                        '40':('40_1.TRA', '40_2.TRA', '40_3.TRA'),
                        '45':('45_5.TRA', '45_6.TRA', '45_7.TRA'),
                        '50':('50_1.TRA', '50_2.TRA', '50_3.TRA'),
                        '60':('60_6.TRA', '60_7.TRA', '60_8.TRA'),
                        '70':('70_1.TRA', '70_2.TRA', '70_3.TRA'),
                        '75':('75_6.TRA', '75_7.TRA', '75_8.TRA'),
                        '80':('80_1.TRA', '80_2.TRA', '80_3.TRA'),
                        '90':('90_5.TRA', '90_6.TRA', '90_7.TRA')
                        }

# upravte datumy mereni u orientaci, ketre se tykaji Vaseho mereni 
d['date_of_measuring'] = dict()
d['date_of_measuring'] = {'0':'1.1.2014',
                        '10':'1.1.2014',
                        '15':'1.1.2014',
                        '20':'1.1.2014',
                        '30':'1.1.2014',
                        '40':'1.1.2014',
                        '45':'1.1.2014',
                        '50':'1.1.2014',
                        '60':'1.1.2014',
                        '70':'1.1.2014',
                        '75':'1.1.2014',
                        '80':'1.1.2014',
                        '90':'1.1.2014'
                        }
                        
# upravte jmena u orientaci, ktere se tykaji Vaseho mereni   
d['name_of_tester']   = dict()
d['name_of_tester']   = {'0':'Xxx Yyy',
                        '10':'Xxx Yyy',
                        '15':'Xxx Yyy',
                        '20':'Xxx Yyy',
                        '30':'Xxx Yyy',
                        '40':'Xxx Yyy',
                        '45':'Xxx Yyy',
                        '50':'Xxx Yyy',
                        '60':'Xxx Yyy',
                        '70':'Xxx Yyy',
                        '75':'Xxx Yyy',
                        '80':'Xxx Yyy',
                        '90':'Xxx Yyy'
                        }      
                        
# upravte teplotu [C] u orientaci, ktere se tykaji Vaseho mereni
d['temperature']      = dict()
d['temperature']      = {'0': 23,
                        '10': 23,
                        '15': 23,
                        '20': 23,
                        '30': 23,
                        '40': 23,
                        '45': 23,
                        '50': 23,
                        '60': 23,
                        '70': 23,
                        '75': 23,
                        '80': 23,
                        '90': 23
                        }

# upravte delku mezi celistmi [mm] u orientaci, ktere se tykaji Vaseho mereni                        
d['grip_length']      = dict()
d['grip_length']      = {'0': 100,
                        '10': 100,
                        '15': 100,
                        '20': 100,
                        '30': 100,
                        '40': 100,
                        '45': 100,
                        '50': 100,
                        '60': 100,
                        '70': 100,
                        '75': 100,
                        '80': 100,
                        '90': 100
                        }
                        
# upravte delku merenou extenzometrem [mm] u orientaci, ktere se tykaji Vaseho mereni
d['ext_length']       = dict()
d['ext_length']       = {'0': 60,
                        '10': 60,
                        '15': 60,
                        '20': 60,
                        '30': 60,
                        '40': 60,
                        '45': 60,
                        '50': 60,
                        '60': 60,
                        '70': 60,
                        '75': 60,
                        '80': 60,
                        '90': 60
                        }
                        
# upravte celkovou delku vzorku [mm] u orientaci, ktere se tykaji Vaseho mereni
d['total_length']     = dict()
d['total_length']     = {'0': 150,
                        '10': 150,
                        '15': 150,
                        '20': 150,
                        '30': 150,
                        '40': 150,
                        '45': 150,
                        '50': 150,
                        '60': 150,
                        '70': 150,
                        '75': 150,
                        '80': 150,
                        '90': 150
                        }
                        
# upravte tloustku vzorku [mm] u orientaci, ktere se tykaji Vaseho mereni
d['thickness']        = dict()
d['thickness']        = {'0': 1,
                        '10': 1,
                        '15': 1,
                        '20': 1,
                        '30': 1,
                        '40': 1,
                        '45': 1,
                        '50': 1,
                        '60': 1,
                        '70': 1,
                        '75': 1,
                        '80': 1,
                        '90': 1
                        }
                        
# upravte sirku vzorku [mm] u orientaci, ktere se tykaji Vaseho mereni
d['width']            = dict()
d['width']            = {'0': 10,
                        '10': 10,
                        '15': 10,
                        '20': 10,
                        '30': 10,
                        '40': 10,
                        '45': 10,
                        '50': 10,
                        '60': 10,
                        '70': 10,
                        '75': 10,
                        '80': 10,
                        '90': 10
                        }
                        
# upravte mereny material u orientaci, ktere se tykaji Vaseho mereni
d['material']         = dict()
d['material']         = {'0':'skelna tkanina',
                        '10':'skelna tkanina',
                        '15':'skelna tkanina',
                        '20':'skelna tkanina',
                        '30':'skelna tkanina',
                        '40':'skelna tkanina',
                        '45':'skelna tkanina',
                        '50':'skelna tkanina',
                        '60':'skelna tkanina',
                        '70':'skelna tkanina',
                        '75':'skelna tkanina',
                        '80':'skelna tkanina',
                        '90':'skelna tkanina',
                        }

# upravte poznamku k mereni u orientaci, ktere se tykaji Vaseho mereni
d['notes']            = dict()
d['notes']            = {'0':'poznamka',
                        '10':'poznamka',
                        '15':'poznamka',
                        '20':'poznamka',
                        '30':'poznamka',
                        '40':'poznamka',
                        '45':'poznamka',
                        '50':'poznamka',
                        '60':'poznamka',
                        '70':'poznamka',
                        '75':'poznamka',
                        '80':'poznamka',
                        '90':'poznamka',
                        }   
