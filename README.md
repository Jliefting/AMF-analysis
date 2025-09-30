# AMF-analysis
Anaconda 3 is required to open the notebooks (https://www.anaconda.com/download)
In anaconda execute the following lines one by one:

conda create -n AMF_analysis_env python=3.10 numpy pandas matplotlib seaborn notebook jupyterlab ipykernel scipy scikit-learn scikit-image networkx imageio opencv shapely tifffile zarr dask cython natsort --yes
conda activate AMF_analysis_env
pip install Cython nd2reader pygeoops nd2 bioio bioio-czi bioio-bioformats pyimagej jpype1 napari[all] segmentation

Then to open jupyter notebook: jupyter notebook

