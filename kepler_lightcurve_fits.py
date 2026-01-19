import pandas as pd
import lightkurve as lk
from astropy.coordinates import SkyCoord
import astropy.units as u
from pathlib import Path
from tqdm import tqdm  # Added for a nice progress bar

mega_targets = pd.read_csv("ASTR502_Mega_Target_List.csv")
master_targets = pd.read_csv("ASTR502_Master_Target_List.csv")
kepler_mini = pd.read_csv("Kepler_Mini_Test.csv")
kepler_data = []

stars = kepler_mini
results = []


base_dir = Path("kepler_data")
base_dir.mkdir(exist_ok=True)

print(f"Starting download of {len(stars)} targets...")

for _, row in tqdm(stars.iterrows(), total=len(stars)):
    ra, dec = row["ra"], row["dec"]
    coord = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame="icrs")
    
    star_name = f"target_{ra:.4f}_{dec:.4f}"
    star_dir = base_dir / star_name
    
    try:
        search_result = lk.search_lightcurve(coord, mission="Kepler", author="Kepler", exptime="long")

        if len(search_result) == 0:
            results.append({"ra": ra, "dec": dec, "status": "no_data"})
            continue

        if star_dir.exists() and list(star_dir.glob("*.fits")):
            results.append({"ra": ra, "dec": dec, "status": "already_exists"})
            continue

        star_dir.mkdir(exist_ok=True)

        lc_collection = search_result.download_all(download_dir=str(star_dir))
        
        results.append({"ra": ra, "dec": dec, "n_lcs": len(lc_collection),"target_id": search_result.table['targetid'][0],"status": "downloaded"})

    except Exception as e:
        results.append({"ra": ra, "dec": dec, "status": f"error: {str(e)}"})

# Save summary
pd.DataFrame(results).to_csv("download_log.csv", index=False)