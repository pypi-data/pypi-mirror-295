#!/usr/bin/env python
#
# Map Plotter Class
#
# Plot map Data using CARTOPY
#
# Fix Cartopy blowup errors:
#	pip uninstall shapely
#	pip install --no-binary :all: shapely
#
# Arnau Miro, Elena Terzic (2023)
from __future__ import print_function, division

import json, numpy as np, matplotlib, matplotlib.pyplot as plt, netCDF4 as NC, cmocean
import cartopy.crs as ccrs, cartopy.feature as cfeature, cartopy.io.img_tiles as cimgt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from datetime import datetime


class MapPlotter():
	'''
	MAPPLOTTER class

	Plot data using CARTOPY. Therefore Cartopy must be installed
	on your system.

	Example usage:

		# Define class instance
		plotter = mp.MapPlotter(projection='PlateCarree')
		params  = plotter.defaultParams() # Create basic parameters dictionary

		# To plot already loaded fields
		plotter.plot(lon,lat,data,params=params)

		# To plot data from NetCDF data
		plotter.plot_from_file(filename,varname,lonname,latname,iTime=0,iDepth=0,params=params)

		# To plot data from NetCDF data with meshmask
		plotter.plot_from_file_and_mask(filename,varname,maskfile,iTime=0,iDepth=0,masklon="glamt",masklat="gphit",params=params)

		# To see the data
		plotter.save('outfile.png',dpi=300)
		plotter.show() # wrapper of plt.show()

	'''
	def __init__(self,projection='PlateCarree',**kwargs):
		'''
		Class constructor. Define a MapPlotter instance.

		Inputs:
			> Projection: Type of projection according to cartopy
						  as a string 
				https://scitools.org.uk/cartopy/docs/latest/crs/projections.html

			Additional arguments for the projection can be added
			as kwargs to this function.

		Output:
			> MapPlotter class instance
		'''
		self._projection = getattr(ccrs,projection)(**kwargs)
		# Class variables
		self._fig  = None
		self._ax   = None
		self._gl   = None
		self._plot = None

	@property
	def projection(self):
		return self._projection

	@staticmethod
	def loadNC(fname,varname,mask_value=np.nan):
		'''
		Load data from NETCDF file. This function is identical to
		bit.sea commons.netcdf4 readfile. It will also filter any
		fill value with a mask value.

		Inputs:
			> fname:      NetCDF file name
			> varname:    Variable name inside NetCDF file
			> mask_value: Value to replace the fill value (default: NaN)

		Output:
			> variable as a numpy array.
		'''
		D = NC.Dataset(fname,'r')
		v = np.array(D.variables[varname][:].filled(mask_value))
		D.close()
		return v

	@staticmethod
	def defaultParams():
		'''
		Return default plot params dictionary.

		Outputs:
			> params dictionary
		'''
		params = {
			# Figure and axes params
			'fig'         : None,
			'ax'          : None,
			# Figure params
			'size'        : (8,6),
			'dpi'         : 100,
			'style'       : None, #'ggplot'
			# Axes params
			'xlim'        : [-180,180],
			'ylim'        : [-90,90],
			'max_div'     : 4,
			'axis_format' : '.1f',
			'top_label'   : False,
			'bottom_label': True,
			'right_label' : False,
			'left_label'  : True,
			'grdstyle'    : {},
			'grdargs'     : {'draw_labels':True,'linewidth':0},
			'features'    : ['coastline','continents','rivers','image'],
			'res'         : '50m',
			'img'         : None,
			'img_format'  : 'png',
			'map_zoom'    : 9,
			'map_kind'    : {'tile':'GoogleTiles','arguments':{'style':'satellite'}},
			# Title and labels
			'title'       : [], # [title,kwargs]
			'xlabel'      : [],
			'ylabel'      : [],
			# Plot params
			'alpha'       : 1.,
			# Colormap and colorbar
			'cmap'        : 'coolwarm',
			'ncol'        : 256, 
			'draw_cbar'   : True,
			'orientation' : 'horizontal',
			'extend'      : None,
			'shrink'      : 1.0,
			'aspect'      : 20.,
			'bounds'      : [-1e30, 1e30], # [min,max]
			'numticks'    : 10,
			'tick_format' : '%.2f',
			'tick_font'   : None,
			'label'       : {'label':'','weight':None,'style':None}
		}
		return params

	@staticmethod
	def loadParams(filename):
		'''
		Load params dictionary from file
		'''
		file   = open(filename,'r')
		params = json.load(file)
		file.close() 
		return params

	@staticmethod
	def saveParams(filename,params):
		'''
		Save params dictionary to file
		'''
		file = open(filename,'w')
		json.dump(params,file)
		file.close()

	@staticmethod
	def show():
		'''
		Wrapper to matplotlib.pyplot.show()
		'''
		plt.show()

	@staticmethod
	def suptitle(t,**kwargs):
		'''
		Wrapper to matplotlib.pyplot.suptitle(t,**kwargs)
		'''
		plt.suptitle(t,**kwargs)
	
	@staticmethod
	def close():
		'''
		Wrapper to matplotlib.pyplot.close()
		'''
		plt.close()

	@staticmethod
	def fmin(f,x):
		return (1.-f if x > 0 else 1.+f)*x
		
	@staticmethod
	def fmax(f,x):
		return (1.+f if x > 0 else 1.-f)*x

	def save(self,filename,dpi=300,margin='tight'):
		'''
		Save figure to disk.

		Inputs:
			> filename: Output file name
			> dpi:      Pixel depth (default: 300)
			> margin;   Bbox margins
		'''
		if self._fig and self._ax:# and self._plot:
			self._fig.savefig(filename,dpi=dpi,bbox_inches=margin)

	def clear():
		'''
		Wrapper to matplotlib.pyplot.clf()
		'''
		self._fig.clf()

	def createFigure(self,sz=(8,6),dpi=100,style=None):
		'''
		Create a new figure.

		Inputs:
			> sz:    Figure size (default: (8,6))
			> dpi:   Pixel depth (default: 100)
			> style: Name of a matplotlib style sheet
				https://matplotlib.org/3.1.1/gallery/style_sheets/style_sheets_reference.html

		Outputs:
			> Figure object
		'''
		fig = None
		if style:
			plt.style.use(style)
			fig = plt.figure(figsize=sz,dpi=dpi)
		else:
			fig = plt.figure(figsize=sz,dpi=dpi,facecolor='w',edgecolor='k')
		return fig

	def createAxes(self):
		'''
		Create new axes.

		Outputs:
			> Axes object
		'''
		return plt.axes(projection=self._projection)

	def createSubplot(self, *args, **kwargs):
		'''
		Create new subplot axes.

		Outputs:
			> Axes object		
		'''
		kwargs['projection'] = self._projection
		return plt.subplot(*args,**kwargs)

	def createGridlines(self,xlim=[-180,180],ylim=[-90,90],axis_format='.1f',top=False,bottom=True,left=True,right=False,max_div=4,style={},gridlines_kwargs={'draw_labels':True,'linewidth':0}):
		'''
		Create gridlines for the current axes.

		Inputs:
			> xlim:             Minimum and maximum extend for the x axis (default: [-180,180])
			> ylim:             Minimum and maximum extend for the y axis (default: [-90,90])
			> top:              Display labels at the top (default: False)
			> right:            Display labels at the right (default: False)
			> max_div:          Maximum number of divisions on the axes (defaut: 4).
			> style:            Style dictionary for the axis labels.
			> gridlines_kwargs: Extra gridlines arguments dictionary.

		Outputs:
			> Gridlines object
		'''
		gl = None
		if self._ax:
			# Axes limits
#			self._ax.set_xlim(xlim)
#			self._ax.set_ylim(ylim)
			self._ax.set_extent(xlim+ylim,crs=ccrs.PlateCarree())
			# Grid lines
			gl = self._ax.gridlines(crs=ccrs.PlateCarree(),**gridlines_kwargs)
			gl.xlocator      = matplotlib.ticker.FixedLocator(np.arange(xlim[0],xlim[1],(xlim[1]-xlim[0])/max_div))
			gl.ylocator      = matplotlib.ticker.FixedLocator(np.arange(ylim[0],ylim[1],(ylim[1]-ylim[0])/max_div))
			gl.xformatter    = LongitudeFormatter(number_format=axis_format,
												  degree_symbol='$^\circ$')
			gl.yformatter    = LatitudeFormatter(number_format=axis_format,
												 degree_symbol='$^\circ$')
			gl.top_labels    = top
			gl.bottom_labels = bottom
			gl.xlabel_style  = style
			gl.xlabel_style  = style
			gl.left_labels   = left
			gl.right_labels  = right
			gl.ylabel_style  = style
			gl.ylabel_style  = style
		return gl

	def setTitle(self,title,**kwargs):
		'''
		Set the title on the current axes.

		Inputs:
			> title:  Title string.

		Any kwargs to format the title are also accepted by this function.
		'''
		if self._ax:
			self._ax.set_title(title,**kwargs)

	def setXAxis(self,label,**kwargs):
		'''
		Set the x axis label on the current axes.

		Inputs:
			> label:  Label string.

		Any kwargs to format the label are also accepted by this function.
		'''
		if self._ax:
			self._ax.set_xlabel(label,**kwargs)

	def setYAxis(self,label,**kwargs):
		'''
		Set the y axis label on the current axes.

		Inputs:
			> label:  Label string.

		Any kwargs to format the label are also accepted by this function.
		'''
		if self._ax:
			self._ax.set_ylabel(label,**kwargs)

	def setAxisExtent(self,ext,projection='PlateCarree',**kwargs):
		'''
		Set the limits for the x and y axis
		'''
		if self._ax:
			transform = getattr(ccrs,projection)(**kwargs)
			self._ax.set_extent(ext,transform)

	def drawCoastline(self,res='50m',color=(0,0,0,1),linewidth=.75):
		'''
		Draws the coastline using Natural Earth Features.

		Inputs:
			> res:       Resolution (default: 50m)
			> color:     Color of the coastline (default (0,0,0,1))
			> linewidth: Width of the coastline (default .75)
		'''
		if self._ax:
			self._ax.add_feature(
				cfeature.NaturalEarthFeature('physical', 'coastline', res, 
					edgecolor=color, facecolor='none', linewidth=linewidth)
				)

	def drawContinentBorders(self,res='50m',color=(0,0,0,.6),linewidth=.75):
		'''
		Draws the continent borders using Natural Earth Features.

		Inputs:
			> res:       Resolution (default: 50m)
			> color:     Color of the border line (default (0,0,0,.6))
			> linewidth: Width of the border line (default .75)
		'''
		if self._ax:
			self._ax.add_feature(
				cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', res, 
					edgecolor=color, facecolor='none', linewidth=linewidth)
				)

	def drawRivers(self,res='50m',color=(0,0,.545,.75),linewidth=.5):
		'''
		Draws the rivers using Natural Earth Features.

		Inputs:
			> res:       Resolution (default: 50m)
			> color:     Color of the rivers (default (0,0,.545,.75))
			> linewidth: Width of the rivers (default .5)
		'''
		if self._ax:
			self._ax.add_feature(
				cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', res, 
					edgecolor=color, facecolor='none', linewidth=linewidth)
				)

	def drawBackground(self,img=None,img_fmt='png',extent=[-180, 180, -90, 90],projection='PlateCarree',**kwargs):
		'''
		Draw a background image. If no image is provided it uses cartopy's stock image.

		Inputs:
			> img: URL or full path to a high resolution image.
		'''
		if self._ax:
			if not img is None or img == '':
				transform  = getattr(ccrs,projection)(**kwargs)
				# Use the transform to correct the extent
				if not projection == 'PlateCarree':
					out = transform.transform_point(extent[0],extent[2],ccrs.PlateCarree())
					extent[0],extent[2] = out[0],out[1]
					out = transform.transform_point(extent[1],extent[3],ccrs.PlateCarree())
					extent[1],extent[3] = out[0],out[1]
				# Dependencies for images
				from PIL import Image
				Image.MAX_IMAGE_PIXELS = 18446744073709551616
				# Detect if we are dealing with a URL or a path
				if 'https://' in img or 'http://' in img:
					# Dependencies for URL
					import io, requests
					self._ax.imshow(plt.imread(io.BytesIO(requests.get(img).content),format=img_fmt), 
						origin='upper', transform=transform, extent=extent)
				else:
					self._ax.imshow(plt.imread(img), origin='upper', 
						transform=transform, extent=extent)
			else:
				self._ax.stock_img()

	def drawTileMap(self,zoom,kind):
		'''
		Draw a tile using a cartopy tile service
		'''
		tile = getattr(cimgt,kind['tile'])(**kind['arguments'])
		self._ax.add_image(tile,zoom)

	def setColormap(self,cmap='coolwarm',ncol=256):
		'''
		Set the colormap.
		
		Inputs:
			> cmap: Colormap name (default: 'coolwarm') or object
				    https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html

				    For cmocean colormaps start with cmo (eg. cmo.algae)
				    https://matplotlib.org/cmocean/

			> ncol: Number of colors on the colormap (default: 256)

		Outputs:
			> Colormap object
		'''
		if isinstance(cmap,str):
			# Check if we are using cmocean or matplotlib
			module = cmocean if cmap in cmocean.cm.cmapnames else matplotlib
			# Get the colormap from the module
			cmap = getattr(module.cm,cmap).resampled(ncol)
			cmap.set_bad(color='k',alpha=0.)
		return cmap

	def setColorbar(self,orientation='horizontal',extend='neither',shrink=1.0,aspect=20,
		numticks=10,tick_format='%.2f',tick_font=None,label={}):
		'''
		Set the colorbar.

		Inputs:
			> orientation: Orientation of the colorbar (default: 'horizontal')
			> extend:      Extend of the colorbar (default: 'neither')
			> numticks:    Number of ticks on the colorbar (default: 10)
			> tick_format: Format of the colorbar ticks (default: "%.2f")
			> tick_font:   Tick font size
			> label:       Label dictionary for the colorbar

		Outputs:
			> Colorbar object
		'''
		cbar = None
		if self._fig and self._plot:
			cbar = self._fig.colorbar(self._plot,orientation=orientation,extend=extend,shrink=shrink,aspect=aspect)
			cbar.set_label(**label)
			if tick_font: cbar.ax.tick_params(labelsize=tick_font)
			cbar.locator   = matplotlib.ticker.LinearLocator(numticks=numticks)
			if tick_format == 'datetime':
				cbar.formatter = matplotlib.ticker.FuncFormatter(lambda x, pos: datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
			elif isinstance(tick_format,list):
				cbar.formatter = matplotlib.ticker.FixedFormatter(tick_format)
			else:
				cbar.formatter = matplotlib.ticker.FormatStrFormatter(tick_format)
			cbar.update_ticks()
		return cbar

	def plot_empty(self,params=None,clear=True):
		'''
		Plot the map with all the settings and without data.

		Outputs:
			> Figure object
		'''
		if clear: self.clear
		if params is None:
			params = self.defaultParams()
		# Do we have figure and axes?
		if not params['fig'] and not params['ax']:
			self._fig = self.createFigure(sz=params['size'],dpi=params['dpi'],style=params['style'])
			self._ax  = self.createAxes()
		if params['fig'] and not params['ax']:
			self._fig = params['fig']
			self._ax  = self.createAxes()
		if params['fig'] and params['ax']:
			self._fig = params['fig']
			self._ax  = params['ax']

		# Axes grid lines
		self._gl = self.createGridlines(xlim=params['xlim'],ylim=params['ylim'],axis_format=params['axis_format'],
		 	top=params['top_label'],bottom=params['bottom_label'],right=params['right_label'],left=params['left_label'],
			max_div=params['max_div'],style=params['grdstyle'],gridlines_kwargs=params['grdargs'])

		# Title and axis labels
		if not params['title'] == []:
			if len(params['title']) == 1:
				self.setTitle(params['title'][0])
			else:
				self.setTitle(params['title'][0],**params['title'][1])

		if not params['xlabel'] == []:
			if len(params['xlabel']) == 1:
				self.setXAxis(params['xlabel'][0])
			else:
				self.setXAxis(params['xlabel'][0],**params['xlabel'][1])

		if not params['ylabel'] == []:
			if len(params['ylabel']) == 1:
				self.setYAxis(params['ylabel'][0])
			else:
				self.setYAxis(params['ylabel'][0],**params['ylabel'][1])

		# Add features
		if 'coastline' in params['features']:
			self.drawCoastline(res=params['res'])
		if 'continents' in params['features']:
			self.drawContinentBorders(res=params['res'])
		if 'rivers' in params['features']:
			self.drawRivers(res=params['res'])
		if 'image' in params['features']:
			self.drawBackground(img=params['img'],img_fmt=params['img_format'])
		if 'tilemap' in params['features']:
			self.drawTileMap(params['map_zoom'],kind=params['map_kind'])

		return self._fig

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
		self.plot_empty(params=params,clear=clear)

		# Set maximum and minimum
		z_min, z_max = np.nanmin(data), np.nanmax(data)
		
		cbar_min = params['bounds'][0] if params['bounds'][0] >= -1e20 else z_min
		cbar_max = params['bounds'][1] if params['bounds'][1] <= 1e20  else z_max

		# Set extend
		if params['extend'] is None:
			params['extend'] = 'neither'
			if (cbar_min > z_min):                      params['extend'] = 'min'
			if (cbar_max < z_max):                      params['extend'] = 'max'
			if (cbar_min > z_min and cbar_max < z_max): params['extend'] = 'both'

		# Plot
		transform  = getattr(ccrs,projection)(**kwargs)
		self._plot = self._ax.pcolormesh(lon,lat,data,
					cmap=self.setColormap(cmap=params['cmap'],ncol=params['ncol']),
					norm=matplotlib.colors.Normalize(cbar_min,cbar_max),
					alpha=params['alpha'],
					shading='auto',
					transform=transform
					 		 )

		# Colorbar
		if params['draw_cbar']:
			self.setColorbar(orientation=params['orientation'],
							 extend=params['extend'],
							 shrink=params['shrink'],
							 aspect=params['aspect'],
							 numticks=params['numticks'],
							 tick_format=params['tick_format'],
							 tick_font=params['tick_font'],
							 label=params['label']
							)

		return self._fig

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
		# Load longitude and latitude
		lon  = self.loadNC(filename,lonname)
		lat  = self.loadNC(filename,latname)
		# Load data
		data = self.loadNC(filename,varname)
		if len(data.shape) == 4:
			data = data[iTime,iDepth,:,:]
		else:
			if iDepth < 0:
				data = data[iTime,:,:]
			else:
				data = data[iDepth,:,:]
		# Plot
		return self.plot(lon,lat,data,params=params,clear=clear,projection=projection,**kwargs)

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
		# Load longitude and latitude
		lon  = self.loadNC(maskfile,masklon)
		if len(lon.shape) == 4:
			lon = lon[0,0,:,:]
		else:
			lon = lon[0,:,:]
		lat  = self.loadNC(maskfile,masklat)
		if len(lat.shape) == 4:
			lat = lat[0,0,:,:]
		else:
			lat = lat[0,:,:]
		# Load data
		data = self.loadNC(filename,varname)
		if len(data.shape) == 4:
			data = data[iTime,iDepth,:,:]
		else:
			data = data[iDepth,:,:]
		# Plot
		return self.plot(lon,lat,data,params=params,clear=clear,projection=projection,**kwargs)

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
		self.plot_empty(params=params,clear=clear)

		# Plot
		transform  = getattr(ccrs,projection)(**kwargs)
		if len(data) == 0 : 
			self._plot = self._ax.scatter(xc,yc,transform=transform,marker=marker,s=size)
		else:
			self._plot = self._ax.scatter(xc,yc,transform=transform,marker=marker,s=size,
											c=data,
											cmap=self.setColormap(cmap=params['cmap'],ncol=params['ncol']))
			params['extend'] = 'neither'
			# Colorbar
			if params['draw_cbar']:
				self.setColorbar(orientation=params['orientation'],
							 	extend=params['extend'],
							 	shrink=params['shrink'],
							 	aspect=params['aspect'],
							 	numticks=params['numticks'],
							 	tick_format=params['tick_format'],
							 	tick_font=params['tick_font'],
							 	label=params['label']
								)
		return self._fig

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
		self.plot_empty(params=params,clear=clear)

		# Plot
		transform  = getattr(ccrs,projection)(**kwargs)
		self._plot = self._ax.plot(xc,yc,fmt,transform=transform,s=size)

		return self._fig

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
		self.plot_empty(params=params,clear=clear)

		# Set maximum and minimum
		z_min, z_max = np.nanmin(data), np.nanmax(data)
		
		cbar_min = params['bounds'][0] if params['bounds'][0] >= -1e20 else z_min
		cbar_max = params['bounds'][1] if params['bounds'][1] <= 1e20  else z_max

		# Set extend
		if params['extend'] is None:
			params['extend'] = 'neither'
			if (cbar_min > z_min):                      params['extend'] = 'min'
			if (cbar_max < z_max):                      params['extend'] = 'max'
			if (cbar_min > z_min and cbar_max < z_max): params['extend'] = 'both'

		# Plot
		transform  = getattr(ccrs,projection)(**kwargs)
		self._plot = self._ax.contour(lon,lat,data,levels,
					cmap=self.setColormap(cmap=params['cmap'],ncol=params['ncol']),
					norm=matplotlib.colors.Normalize(cbar_min,cbar_max),
					linewidths=linewidth,
					alpha=params['alpha'],
					transform=transform
					 		 )
		
		# Contour plot labels
		if not labelsize is None:
			self._ax.clabel(self._plot, inline=True, fontsize=labelsize)

		# Colorbar
		if params['draw_cbar']:
			self.setColorbar(orientation=params['orientation'],
							 extend=params['extend'],
							 shrink=params['shrink'],
							 aspect=params['aspect'],
							 numticks=params['numticks'],
							 tick_format=params['tick_format'],
							 tick_font=params['tick_font'],
							 label=params['label']
							)

		return self._fig

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
		self.plot_empty(params=params,clear=clear)

		# Plot
		transform  = getattr(ccrs,projection)(**kwargs)
		if data is None: 
			self._plot = self._ax.quiver(xc[::dsample],yc[::dsample],uc[::dsample,::dsample],vc[::dsample,::dsample],
										 transform=transform,scale=scale,color=color,
										 cmap=self.setColormap(cmap=params['cmap'],ncol=params['ncol']))
		else:
			self._plot = self._ax.quiver(xc[::dsample],yc[::dsample],uc[::dsample,::dsample],vc[::dsample,::dsample],data[::dsample,::dsample],
				                         transform=transform,scale=scale,
										 cmap=self.setColormap(cmap=params['cmap'],ncol=params['ncol']))

			# Colorbar
			#params['extend'] = 'neither'
			if params['draw_cbar']:
				self.setColorbar(orientation=params['orientation'],
								 extend=params['extend'],
								 shrink=params['shrink'],
								 aspect=params['aspect'],
								 numticks=params['numticks'],
								 tick_format=params['tick_format'],
								 tick_font=params['tick_font'],
								 label=params['label']
								)

		return self._fig