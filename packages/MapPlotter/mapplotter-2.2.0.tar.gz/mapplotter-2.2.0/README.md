[![Build status](https://github.com/ArnauMiro/MapPlotter/actions/workflows/build_python.yml/badge.svg)](https://github.com/ArnauMiro/MapPlotter/actions)
[![License](https://img.shields.io/badge/license-GPL3-orange)](https://opensource.org/license/gpl-3-0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10598154.svg)](https://doi.org/10.5281/zenodo.10598154)

# Map Plotter

Map Plotter is a toolkit that provides a framework for 2D map plots of data and NetCDF files. It consists of a python class (_MapPlotter_) that interfaces with [cartopy](https://scitools.org.uk/cartopy/docs/latest/) to generate beautiful maps.

This tool depends on:
* the [PROJ library](https://proj.org/)
* [Cartopy](https://scitools.org.uk/cartopy/docs/latest/)
* the [requests](https://pypi.org/project/requests/) module

Two examples (_example_MapPlotter_1.py_ and _example_MapPlotter_2.py_) are provided as a reference.

For any issues please contact: [arnau.miro(at)upc(dot)edu](mailto:arnau.miro@upc.edu).

## Installation

A _Makefile_ is provided within the tool to automate the installation for easiness of use for the user. To install the tool simply create a virtual environment as stated below or use the system Python. Once this is done simply type:
```bash
make
```
This will install all the requirements and install the package to your active python. To uninstall simply use
```bash
make uninstall
```

The previous operations can be done one step at a time using
```bash
make requirements
```
to install all the requirements and
```bash
make install
```
to install the tool.

### Virtual environment

The package can be installed in a Python virtual environement to avoid messing with the system Python installation.
Next, we will use [Conda](https://docs.conda.io/projects/conda/en/latest/index.html) for this purpose.
Assuming that Conda is already installed, we can create a virtual environment with a specific python version and name (`my_env`) using
```bash
conda create -n my_env python=3.8
```
The environment is placed in `~/.conda/envs/my_env`.
Next we activate it be able to install packages using `conda` itself or another Python package manager in the environment directory:
```bash
conda activate my_env
```
Then just follow the instructions as stated above.

### Get cartopy

Cartopy can be installed using the pip tool by doing:
```bash
pip install cartopy
```
Sometimes a segmentation fault can appear when running some projections. In that case the following fixes the issue:
```bash
pip uninstall shapely
pip install --no-binary :all: shapely
```

## Usage

### The MAPPLOTTER class

Plot NETCDF data using CARTOPY. Example python snippets:

```python
import MapPlotter as mp

# Define class instance
plotter = mp.MapPlotter(projection='PlateCarree')
params  = plotter.defaultParams() # Create basic parameters dictionary

# To plot already loaded fields
plotter.plot(lon,lat,data,params=params)

# To plot data from NetCDF data
plotter.plot_from_file(filename,varname,lonname,latname,iTime=0,iDepth=0,params=params)

# To see the data
plotter.save('outfile.png',dpi=300)
plotter.show() # wrapper of plt.show()
```

### MAPPLOTER plot types

The following plotting functions are available:
* Basic empty plot
```python
def plot_empty(self,params=None,clear=True):
	'''
	Plot the map with all the settings and without data.

	Outputs:
		> Figure object
	'''
```
* Main plotting function based on pcolormesh
```python
def plot(self,lon,lat,data,params=None,clear=True,projection='PlateCarree',**kwargs):
	'''
	Main plotting function. Plots given the longitude, latitude and data.
	An optional params dictionary can be inputted to control the plot.

	Inputs:
		> lon:        Longitude vector or matrix
		> lat:        Latitude vector or matrix
		> data:       Data matrix
		> params:     (Optional) parameter dictionary
		> clear:      (Optional) Clear axes before plotting
		> Projection: Type of projection that the data is
						using (default assumes PlateCarree)

	Outputs:
		> Figure object
	'''
```
* Plotting directly from NetCDF files
```python
def plot_from_file(self,filename,varname,lonname,latname,iTime=0,iDepth=0,params=None,clear=True,projection='PlateCarree',**kwargs):
	'''
	Plot function. Plots data given a NetCDF file and the names of the variables
	as well as the current depth and time index.

	Inputs:
		> filename:   NetCDF file path
		> varname:    Name of the NetCDF variable to plot
		> lonname:    Name of the longitude dimension
		> latname:    Name of the latitude dimension
		> iTime:      Time index for NetCDF (default: 0)
		> iDepth:     Depth index for NetCDF (default: 0)
		> params:     (Optional) parameter dictionary
		> clear:      (Optional) Clear axes before plotting
		> Projection: Type of projection that the data is
						using (default assumes PlateCarree)

	Outputs:
		> Figure object
	'''
```
```python
def plot_from_file_and_mask(self,filename,varname,maskfile,iTime=0,iDepth=0,
	masklon='glamt',masklat='gphit',params=None,clear=True):
	'''
	Plot function. Plots data given a NetCDF file, a mask file, the names of 
	the variables as well as the current depth and time index.

	Inputs:
		> filename:   NetCDF file path
		> varname:    Name of the NetCDF variable to plot
		> maskfile:   Path to the mask file
		> iTime:      Time index for NetCDF (default: 0)
		> iDepth:     Depth index for NetCDF (default: 0)
		> masklon:    Name of the longitude dimension (default: 'glamt')
		> masklat:    Name of the latitude dimension (default: 'gphit')
		> params:     (Optional) parameter dictionary
		> clear:      (Optional) Clear axes before plotting
		> Projection: Type of projection that the data is
						using (default assumes PlateCarree)

	Outputs:
		> Figure object		
	'''
```
* Scatter plot
```python
def scatter(self,xc,yc,data=np.array([]),params=None,clear=True,marker=None,size=None,projection='PlateCarree',**kwargs):
	'''
	Main plotting function. Plots given the longitude, latitude and data.
	An optional params dictionary can be inputted to control the plot.

	Inputs:
		> xc:     Scatter x points
		> yc:     Scatter y points
		> data:   Color data to be plotted
		> params: Optional parameter dictionary
		> clear:  Clear axes before plotting
		> marker: Marker for scatter plot
		> size:   Size for the scatter plot

	Outputs:
		> Figure object
	'''
```
* Line plot (note that it does not allow to map it to a colormap)
```python
def line(self,xc,yc,fmt='-',params=None,clear=True,size=None,projection='PlateCarree',**kwargs):
	'''
	Main plotting function. Plots given the longitude, latitude and data.
	An optional params dictionary can be inputted to control the plot.

	Inputs:
		> xc:     Scatter x points
		> yc:     Scatter y points
		> data:   Color data to be plotted
		> params: Optional parameter dictionary
		> clear:  Clear axes before plotting
		> marker: Marker for scatter plot
		> size:   Size for the scatter plot

	Outputs:
		> Figure object
	'''
```
* Contour plot
```python
def contour(self,lon,lat,data,levels=10,labelsize=None,linewidth=None,params=None,clear=True,projection='PlateCarree',**kwargs):
	'''
	Main plotting function. Plots given the longitude, latitude and data.
	An optional params dictionary can be inputted to control the plot.

	Inputs:
		> lon:        Longitude vector or matrix
		> lat:        Latitude vector or matrix
		> data:       Data matrix
		> levels:     Number and positions of the contour lines / regions
		> linewidth:  (Optional) The line width of the contour lines
		> labelsize:  (Optional) Label font size for contour plot
		> params:     (Optional) Parameter dictionary
		> clear:      (Optional) Clear axes before plotting
		> Projection: Type of projection that the data is
						using (default assumes PlateCarree)

	Outputs:
		> Figure object
	'''
```
* Quiver plot
```python
def quiver(self,xc,yc,uc,vc,dsample=1,data=None,params=None,clear=True,scale=None,color=None,projection='PlateCarree',**kwargs):
	'''
	Main plotting function. Plots given the longitude, latitude and data.
	An optional params dictionary can be inputted to control the plot.

	Inputs:
		> xc:      X position of the arrow
		> yc:      Y position of the arrow
		> uc:      U component for the quiver
		> yc:      V component for the quiver
		> dsample: Downsample (>1 to downsample, use integers)
		> data:    Color data to be plotted. If not provided the modulus is used
		> params:  Optional parameter dictionary
		> clear:   Clear axes before plotting
		> color:   Color to plot (dones not work when data is specified)

	Outputs:
		> Figure object
	'''
```

### Parameters dictionary
The parameters dictionary includes the following modifiable variables.

Figure and axes handles
* _fig_ (default: None): store/give the figure handle
* _ax_  (default: None): store/give the axes handle

Figure and axes creation
* _size_ (default: (8,6)): figure size for creation
* _dpi_  (default: 100): figure dpi for creation
* _style_ (default: None): plot style according to matplotlib styles 

Axes definition and parameters
* _xlim_ (default: [-180,180]): map limits in degrees of longitude
* _ylim_ (default: [-90,90]): map limits in degrees of latitude
* *max_div* (default: 4): maximum number of divisions on the axes
* *axis_format* (default: '.1f'): format of the latitude and logitude axis
* *top_label* (default: False): activate/deactivate axes label on top
* *bottom_label* (default: True): activate/deactivate axes label on bottom
* *right_label* (default: False): activate/deactivate axes label on right
* *left_label* (default: True): activate/deactivate axes label on left
* _grdstyle_ (default: {}): style for the plot grid
* _grdargs_ (default: {'draw_labels':True,'linewidth':0}): arguments for the grid style
* _features_ (default: ['coastline','continents','rivers','image']): features to be added on the plot. Available options are:
	* _coastline_: draw the lines of the coast
	* _continents_: draw the lines of the continents
	* _rivers_: draw the rivers
	* _image_: use an image as background
	* _tilemap_: use a tilemap as background
* _res_ (default: '50m'): resolution for the *tilemap* option
* _img_ (default: None): image to be loaded for the *image* option
* *img_format* (default: 'png'): image format to be loaded for the *image* option
* *map_zoom* (default: 9): zoom for the *tilemap* option
* *map_kind* (default: {'tile':'GoogleTiles','arguments':{'style':'satellite'}}): options for the *tilemap* option

Title and labels
* _title_  (default: []): Plot title in the format of [title,kwargs]
* _xlabel_ (default: []): Plot longitude axis label in the format of [title,kwargs]
* _ylabel_ (default: []): Plot latitude axis label in the format of [title,kwargs]
			
Plot params
* _alpha_ (default: 1.): Transparency control
			
Colormap and colorbar
* _cmap_ (default: 'coolwarm'): colormap for the plot. Any value from matplotlib or cmocean are valid
* _ncol_ (default: 256): number of colors of the colorbar
* *draw_cbar* (default: True): activate/deactivate the colorbar
* _orientation_ (default: 'horizontal'): colorbar orientation, either _horizontal_ or _vertical_
* _extend_ (default: None): whether to extend the colorbar or not
* _shrink_ (default: 1.0): shrinking factor for the colorbar
* _aspect_ (default: 20.): aspect ratio for the colorbar
* _bounds_ (default: [-1e30, 1e30]): bounds, setting as [min,max]
* _numticks_ (default: 10): number of ticks for the colorbar
* *tick_format* (default: '%.2f'): tick format for the colorbar
* *tick_font* (default: None): specific font for the colorbar
* _label_ (default: {'label':'','weight':None,'style':None}): label and specifications for the colorbar


### Command line tool

A command line tool is also provided so that maps can easily be generated from NetCDF files through the command prompt. It can be accessed as:
```bash
map_plotter [-h] -f FILE -v VAR [-m MASK] [--lon LON] [--lat LAT] 
			[-t TIME] [-d DEPTH] [-c CONF] -o OUT [--dpi DPI]
```
Arguments:
* -h, --help               show this help message and exit
* -f FILE, --file FILE     NetCDF file path
* -v VAR, --var VAR        Variable to plot
* -m MASK, --mask MASK     Mask file
* --lon LON                Longitude variable name (default: glamt)
* --lat LAT                Latitude variable name (default: gphit)
* -t TIME, --time TIME     Time index for NetCDF (default: 0)
* -d DEPTH, --depth DEPTH  Depth index for NetCDF (default: 0)
* -c CONF, --conf CONF     Configuration file path
* -o OUT, --outfile OUT    Output file name
* --dpi DPI                Output file DPI (default: 300)