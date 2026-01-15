import pandas as pd
import lightkurve as lk
from astropy.coordinates import SkyCoord
import astropy.units as u

mega_targets = pd.read_csv("ASTR502_Mega_Target_List.csv")
master_targets = pd.read_csv("ASTR502_Master_Target_List.csv")
mini_sample = pd.read_csv("mini_test_sample(in).csv")
kepler_data = []



stars = mega_targets
results = []

for _, row in stars.iterrows():
    if row['mission_source'] == "Kepler":
        ra = row['ra']
        dec = row['dec']
        coord = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame="icrs")

        search_result = lk.search_lightcurve(coord, mission="Kepler", radius=5 * u.arcmin)

        print(f"RA={ra}, DEC={dec}, N_results={len(search_result)}")
        print(row)

        results.append({"ra": ra,"dec": dec,"n_kepler_lcs": len(search_result),"has_kepler_data": len(search_result) > 0})
    

kepler_df = pd.DataFrame(results)

kepler_df.to_csv("kepler_megatargets_ids.csv", index=False)

