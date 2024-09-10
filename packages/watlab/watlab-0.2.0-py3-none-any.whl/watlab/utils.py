"""::

  _    _           _            __ _               
 | |  | |         | |          / _| |              
 | |__| |_   _  __| |_ __ ___ | |_| | _____      __
 |  __  | | | |/ _` | '__/ _ \|  _| |/ _ \ \ /\ / /
 | |  | | |_| | (_| | | | (_) | | | | (_) \ V  V / 
 |_|  |_|\__, |\__,_|_|  \___/|_| |_|\___/ \_/\_/  
          __/ |                                    
         |___/

This module includes functions and classes to pilot hydroflow.

Usage:
======

Insert here the description of the module


License
=======

Copyright (C) <1998 – 2024> <Université catholique de Louvain (UCLouvain), Belgique> 
	
List of the contributors to the development of Watlab: see AUTHORS file.
Description and complete License: see LICENSE file.
	
This program (Watlab) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program (see COPYING file).  If not, 
see <http://www.gnu.org/licenses/>.

"""
import rasterio 
import numpy as np 
from scipy.interpolate import griddata


def extract_values_from_tif(tif_file):
    """_summary_

    :param tif_file: _description_
    :type tif_file: _type_
    :return: _description_
    :rtype: _type_
    """
    with rasterio.open(tif_file) as dataset:
                image_data = dataset.read()
                transform = dataset.transform
                # Get the x and y coordinates of the top-left corner of the image
                x_origin = transform.c
                y_origin = transform.f
                # Get the x and y coordinates of the bottom-right corner of the image
                x_end = x_origin + (dataset.width * transform.a) + transform.a
                y_end = y_origin + (dataset.height * transform.e) + transform.e
                x_coords, y_coords = np.meshgrid(np.linspace(x_origin, x_end, dataset.width), np.linspace(y_origin, y_end, dataset.height))
                data = image_data[0]
            
    tif_points_coordinates = np.column_stack((x_coords.flatten(), y_coords.flatten()))
    tif_points_data = data.flatten()
    return tif_points_coordinates, tif_points_data

def interpolate_points(known_points_coordinates,known_points_data,desired_points,interpolation_method='nearest'):
    """_summary_

    :param known_points_coordinates: _description_
    :type known_points_coordinates: _type_
    :param known_points_data: _description_
    :type known_points_data: _type_
    :param desired_points: _description_
    :type desired_points: _type_
    :return: _description_
    :rtype: _type_
    """
    desired_points_x,  desired_points_y  = desired_points[:,0], desired_points[:,1]
    mesh_points = np.column_stack((desired_points_x.flatten(), desired_points_y.flatten()))
    return griddata(known_points_coordinates, known_points_data, mesh_points, method=interpolation_method)