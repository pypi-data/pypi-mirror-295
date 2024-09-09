"""Class to display and query raster datasets from BDAP (JRC Big Data Analytics Platform) using the interapro library MapnikRaster class."""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2022-2023
# 
# Licensed under the EUPL, Version 1.2 or as soon they will be approved by 
# the European Commission subsequent versions of the EUPL (the "Licence");
# 
# You may not use this work except in compliance with the Licence.
# 
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS"
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# 
# See the Licence for the specific language governing permissions and
# limitations under the Licence.

from jeodpp import inter

# Python imports
from io import StringIO
import sys



#####################################################################################################################################################
# Class raster
#####################################################################################################################################################
class raster:
    
    # Initialization
    def __init__(self,
                 filepath,
                 band=1,
                 epsg=4326,
                 nodata=999999.0):

        self.filepath = filepath
        self.band     = band
        self.epsg     = epsg
        self.nodata   = nodata

        self.r = inter.MapnikRaster()
        self.r.file(self.filepath, band=self.band, epsg=self.epsg, nodata=self.nodata)
        
    
    # Representation
    def __repr__(self):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        self.r._print()
        sys.stdout = old_stdout
        return mystdout.getvalue()
        
        
    # Create a symbolizer: see https://github.com/mapnik/mapnik/wiki/RasterSymbolizer
    def symbolizer(self,
                   scaling="near",
                   opacity=1.0,
                   composition=""):
        self.r.rasterSymbolizer(scaling, opacity, composition)
        
        
    # Create a colorizer: see https://github.com/mapnik/mapnik/wiki/RasterColorizer
    def colorizer(self,
                  default_mode="linear",
                  default_color="transparent",
                  epsilon=1.5e-07):
        
        self.r.rasterColorizerInit(default_mode,default_color,epsilon)
        

    # Add a colorizer step: see https://github.com/mapnik/mapnik/wiki/RasterColorizer#example-xml
    def color(self,
              value,            # Numerical value
              color="red",      # name of color or "#rrggbb"
              mode=""):         # "discrete", "linear" or "exact"
        
        self.r.rasterColorizerStep(value, color, mode)
        
        
    # Return the ImageProcess instance 
    @property
    def ip(self):
        return self.r
    
    # Return the XML string containing the Mapnik map
    def xml(self):
        return self.r.getXML()
    
    
    # Save the layer in Redis and returns the procid
    def toLayer(self):
        self.r.setXML()
        return self.r.toLayer()
    
    # Return the JSON string defining the raster layer
    def toJson(self):
        self.r.setXML()
        return self.r.toJson()    