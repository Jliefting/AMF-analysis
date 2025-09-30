# AMF-analysis
Anaconda 3 is required to open the notebooks (https://www.anaconda.com/download)
In anaconda execute the following lines one by one:
conda create -n AMF_analysis_env python=3.8 numpy pandas matplotlib seaborn notebook jupyterlab ipykernel scipy scikit-learn scikit-image networkx imageio opencv shapely tifffile zarr dask cython natsort --yes
conda activate AMF_analysis_env
pip install Cython nd2reader pygeoops nd2 bioio bioio-czi bioio-bioformats pyimagej jpype1 napari[all] segmentation
(Python 3.8 is required instead of the current 3.10 due to the segmentation package losing support)

Then to open jupyter notebook: jupyter notebook

The notebooks are categorized into processing, FISH analysis and growth analysis. 
Processing:
Processing DAPI files.ipynb
Processing Files Jurr small files.ipynb (if Zeiss brightfield files are already binned)
Processing Files.ipynb
rebinning_data.ipynb

FISH analysis:
Correlating SSU5670 and empty channels.ipynb
FISH exposure time from metadata.ipynb (In imagej open metadata using ctrl + I and save the metadata into a .txt file)
Opening and displaying images.ipynb
Plot max values per image.ipynb
Ribosome localization.ipynb

Growth analysis:
Extract Graphs Bulk function Jurr.ipynb
Napari corrected.ipynb
Growth graphs from CSV data.ipynb
