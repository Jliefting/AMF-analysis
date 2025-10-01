# AMF-analysis
This repository contains the code used for analysis and custom 3D print STL files. <br>
**3D print** <br>
Chip image platform V6 magnets 6.2x3.2 16cm.stl: Ibidi µ-Slide I Luer(Cat.No:80161) chip holder with holder for fisherbrand 1ml plastic syringe (Cat.no: 14955462). <br>
Zeiss platform cut.stl: Platform to place under a ZEISS Axio Imager 2 that holds the chip holder. 6mm x 3mm Magnets are used to prevent movement during imaging. <br>
ibidi caps prevent drying out.stl: Caps to slide into a Elbow Luer Connector Male (Cat.No: 10802), to prevent the chip from drying out. <br>

**Code** <br>
Anaconda 3 is required to open the notebooks (https://www.anaconda.com/download) <br>
In anaconda execute the following lines one by one: <br>
conda create -n AMF_analysis_env python=3.10 numpy pandas matplotlib seaborn notebook jupyterlab ipykernel scipy scikit-learn scikit-image networkx imageio opencv shapely tifffile zarr dask cython natsort --yes <br>
conda activate AMF_analysis_env <br>
pip install Cython nd2reader pygeoops nd2 bioio bioio-czi bioio-bioformats pyimagej jpype1 napari[all] <br>

(Python 3.8 is required for the segmentation package used in the processing and Extract Graphs Bulk function. Downgrade to python 3.8, you might have to remove the bioio packages for this). <br>

Then to open jupyter notebook: jupyter notebook <br>

The notebooks are categorized into processing, FISH analysis and growth analysis.  <br>
Processing: <br>
Processing DAPI files.ipynb <br>
Processing Files Jurr small files.ipynb (if Zeiss brightfield files are already binned) <br>
Processing Files.ipynb <br>
rebinning_data.ipynb <br>

FISH analysis: <br>
Correlating SSU5670 and empty channels.ipynb <br>
FISH exposure time from metadata.ipynb (In imagej open metadata using ctrl + I and save the metadata into a .txt file) <br>
Opening and displaying images.ipynb <br>
Plot max values per image.ipynb <br>
Ribosome localization.ipynb <br>

Growth analysis: <br>
Extract Graphs Bulk function Jurr.ipynb <br>
Napari corrected.ipynb <br>
Growth graphs from CSV data.ipynb <br>
