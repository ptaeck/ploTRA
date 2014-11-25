from numpy import *

# vyberte verzi s merenymi orientacemi vlaken popr. vytvorte svou vlastni
set_of_specimens_version = 1
set_of_specimens_list =  {'1':array(['0','10','20','30','40','50','60','70','80','90']),
                          '2':array(['0','15','30','45','60','75','90']),
                          '3':array(['0','45','90']),
                          '4':array(['0'])
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

# upravte delku mezi celistmi [m] u orientaci, ktere se tykaji Vaseho mereni                        
d['grip_length']      = dict()
d['grip_length']      = {'0': 0.100,
                        '10': 0.100,
                        '15': 0.100,
                        '20': 0.100,
                        '30': 0.100,
                        '40': 0.100,
                        '45': 0.100,
                        '50': 0.100,
                        '60': 0.100,
                        '70': 0.100,
                        '75': 0.100,
                        '80': 0.100,
                        '90': 0.100
                        }
                        
# upravte delku merenou extenzometrem [m] u orientaci, ktere se tykaji Vaseho mereni
d['ext_length']       = dict()
d['ext_length']       = {'0': 0.060,
                        '10': 0.060,
                        '15': 0.060,
                        '20': 0.060,
                        '30': 0.060,
                        '40': 0.060,
                        '45': 0.060,
                        '50': 0.060,
                        '60': 0.060,
                        '70': 0.060,
                        '75': 0.060,
                        '80': 0.060,
                        '90': 0.060
                        }
                        
# upravte celkovou delku vzorku [m] u orientaci, ktere se tykaji Vaseho mereni
d['total_length']     = dict()
d['total_length']     = {'0': 0.150,
                        '10': 0.150,
                        '15': 0.150,
                        '20': 0.150,
                        '30': 0.150,
                        '40': 0.150,
                        '45': 0.150,
                        '50': 0.150,
                        '60': 0.150,
                        '70': 0.150,
                        '75': 0.150,
                        '80': 0.150,
                        '90': 0.150
                        }
                        
# upravte tloustku vzorku [m] u orientaci, ktere se tykaji Vaseho mereni
d['thickness']        = dict()
d['thickness']        = {'0': 0.001,
                        '10': 0.001,
                        '15': 0.001,
                        '20': 0.001,
                        '30': 0.001,
                        '40': 0.001,
                        '45': 0.001,
                        '50': 0.001,
                        '60': 0.001,
                        '70': 0.001,
                        '75': 0.001,
                        '80': 0.001,
                        '90': 0.001
                        }
                        
# upravte sirku vzorku [m] u orientaci, ktere se tykaji Vaseho mereni
d['width']            = dict()
d['width']            = {'0': 0.010,
                        '10': 0.010,
                        '15': 0.010,
                        '20': 0.010,
                        '30': 0.010,
                        '40': 0.010,
                        '45': 0.010,
                        '50': 0.010,
                        '60': 0.010,
                        '70': 0.010,
                        '75': 0.010,
                        '80': 0.010,
                        '90': 0.010
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
