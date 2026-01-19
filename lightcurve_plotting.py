import lightkurve as lk
from pathlib import Path
import matplotlib.pyplot as plt

def plot_star_from_dir(star_directory):
    path = Path(star_directory)
    
    # 1. Gather and SORT files
    files = sorted([str(f) for f in path.rglob("*.fits")])
    
    if not files:
        print(f"No FITS files found in {path.name}")
        return None

    try:
        # 2. Read into a collection
        lc_collection = lk.read(files)

        # 3. Process the data
        # Normalize each quarter so they align at 1.0
        stitched_lc = (
            lc_collection.normalize()
                         .stitch()
                         .remove_outliers(sigma=5)
        )
        return stitched_lc

    except Exception as e:
        print(f"Error processing {path.name}: {e}")
        return None

# --- MAIN EXECUTION PART ---

data_root = Path("kepler_data")

# Pick the first folder in your data directory to test
try:
    test_folder = next(data_root.iterdir())
    print(f"Attempting to plot: {test_folder.name}")
    
    # CALL the function and save the result to 'lc'
    lc = plot_star_from_dir(test_folder)

    if lc is not None:
        # Now 'lc' exists in this scope and can be plotted
        ax = lc.plot(title=f"Test Plot: {test_folder.name}", color='black', lw=0.5)
        ax.set_xlabel("Time (BKJD)")
        ax.set_ylabel("Normalized Flux")
        plt.show()

except StopIteration:
    print("Error: The 'kepler_data' folder appears to be empty.")


#star_folders = [d for d in data_root.iterdir() if d.is_dir()]

#for folder in star_folders[:5]:
#    plot_star_from_dir(folder)
#    plt.show() 

