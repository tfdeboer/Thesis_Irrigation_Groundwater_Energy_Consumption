import os
import hydropandas as hpd
import pickle
import pprint



outputDirectory = '../../input/timeseries_gw_one_well_GLD_hydropandas/'

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)


# right top: 280500, 624805
# right bottom: -, 304612
# left bot: 9050, -
# left top: 

# test: my_extent = (137000, 138000, 458000, 459000)
# my_extent = (137000, 138000, 458000, 459000)

# my_extent = (9050, 280500, 304612, 624805)
# my_extent = (127000, 138000, 448000, 459000)
# my_extent = (137000, 138000, 458000, 459000)

# observations from extent in Rijksdriehoeks coordinates
# gw_bro = hpd.read_bro(extent=my_extent)
# gw_bro = hpd.read_lizard(extent=my_extent)

#one observation
gw_bro = hpd.GroundwaterObs.from_bro("GLD000000000006", 1) 
#gw_bro = hpd.read_dino(extent=(117850, 118180, 439550, 439900))

gw_bro.to_pickle(outputDirectory +  'gw_bro_one_well_GLD.pklz')

print(gw_bro)
# exit()

obj = pickle.load(open((outputDirectory +  'gw_bro_one_well_GLD.pklz'), "rb"))


with open((outputDirectory +  'gw_bro_one_well_GLD.txt'), "a") as f:
        pprint.pprint(obj, stream=f)

gw_bro.to_excel(outputDirectory +  'gw_bro_Netherlands.xlsx')




