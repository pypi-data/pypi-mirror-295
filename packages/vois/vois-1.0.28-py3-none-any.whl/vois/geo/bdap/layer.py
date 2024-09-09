"""BDAP (JRC Big Data Analytics Platform) layer creation for raster display and identify on a ipyleaflet.Map without dependencies on interapro library. Derived class of serverlayer.serverlayer."""
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

# Widgets import
import ipyleaflet
from ipywidgets import widgets, HTML, CallbackDispatcher
from ipyleaflet import Popup

# Python imports
from io import StringIO, BytesIO
import sys
import json
import requests
import numpy as np

# Local imports
import serverlayer


#####################################################################################################################################################
# Class layer
#####################################################################################################################################################
class layer(serverlayer.serverlayer):
    
    # Initialize
    def __init__(self,
                 filepath='',
                 band=1,
                 epsg=4326,
                 nodata=999999.0,
                 identify_integer=False):
        
        super().__init__(filepath=filepath, band=band, epsg=epsg, nodata=nodata, identify_integer=identify_integer)
        
        # Dict to display strings instead of integers on identify
        self.identify_dict = None

    
    # Returns an instance of ipyleaflet.TileLayer
    def tileLayer(self, max_zoom=22):
        url = self.tileUrl()
        if not url is None:
            return ipyleaflet.TileLayer(url=url, max_zoom=max_zoom, max_native_zoom=max_zoom)
    

    # Execute an identify operation server-side using HTTP call. Returns a scalar float/int/string or a list of scalars
    def identifyPoint(self, lon, lat, epsg=4326, zoomlevel=10):
        response = requests.get('https://jeodpp.jrc.ec.europa.eu/jiplib-view/?IDENTIFYEX=1&vl=%s&x=%f&y=%f&epsg=%d&zoom=%d' % (self.toLayer(), lon, lat, epsg, int(zoomlevel)))
        bio = BytesIO(response.content)
        s = bio.read()
        svalue = s.decode("utf-8").replace('Values = ','').replace('Value = ','')
        if len(svalue) > 0:
            if ',' in svalue:
                vvv = svalue.split(',')
                if len(vvv) <= len(self.ratios):
                    if self.identify_integer:
                        return [int(round(serverlayer.unscaled(float(x),r,o))) for x,r,o in zip(vvv,self.ratios,self.offsets)]
                    else:
                        return [serverlayer.unscaled(float(x),r,o) for x,r,o in zip(vvv,self.ratios,self.offsets)]
                else:
                    if self.identify_integer:
                        return [int(x) for x in vvv]
                    else:
                        return [float(x) for x in vvv]
            else:
                if len(self.ratios) >= 1 and len(self.offsets) >= 1:
                    if self.identify_integer:
                        return serverlayer.unscaled(float(svalue),self.ratios[0],self.offsets[0])
                    else:
                        return int(round(serverlayer.unscaled(float(svalue),self.ratios[0],self.offsets[0])))
                else:
                    if self.identify_integer:
                        ivalue = int(svalue)
                        if not self.identify_dict is None and ivalue in self.identify_dict:
                            return self.identify_dict[ivalue]
                        return ivalue
                    else:
                        return float(svalue)
    

    # Set-up the identify action on a map for the layer
    def identifySetup(self, m, onclick=None, identify_dict=None):

        def handle_interaction_popup(**kwargs):
            if kwargs.get('type') == 'click':
                lat = kwargs.get('coordinates')[0]
                lon = kwargs.get('coordinates')[1]
                res = self.identifyPoint(lon, lat, zoomlevel=int(m.zoom))  # res can be: None, a floating scalar, a list of float values
                if not res is None:
                    if onclick is None:
                        message = widgets.HTML()
                        message.value = "<style> p.small {line-height: 1.2; }</style><p class=\"small\">" + str(res) + "</p>"
                        popup = Popup(location=[lat,lon], child=message, close_button=True, auto_close=True, close_on_escape_key=True)
                        m.add_layer(popup)
                    else:
                        onclick(res, lon, lat)

        self.identify_dict = identify_dict
        m._interaction_callbacks = CallbackDispatcher()
        m.on_interaction(handle_interaction_popup)        