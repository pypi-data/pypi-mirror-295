"""::
.---.  .---.   ____     __  ______     .-------.        ,-----.     ________   .---.       ,-----.    .--.      .--. 
|   |  |_ _|   \   \   /  /|    _ `''. |  _ _   \     .'  .-,  '.  |        |  | ,_|     .'  .-,  '.  |  |_     |  | 
|   |  ( ' )    \  _. /  ' | _ | ) _  \| ( ' )  |    / ,-.|  \ _ \ |   .----',-./  )    / ,-.|  \ _ \ | _( )_   |  | 
|   '-(_{;}_)    _( )_ .'  |( ''_'  ) ||(_ o _) /   ;  \  '_ /  | :|  _|____ \  '_ '`) ;  \  '_ /  | :|(_ o _)  |  | 
|      (_,_) ___(_ o _)'   | . (_) `. || (_,_).' __ |  _`,/ \ _/  ||_( )_   | > (_)  ) |  _`,/ \ _/  || (_,_) \ |  | 
| _ _--.   ||   |(_,_)'    |(_    ._) '|  |\ \  |  |: (  '\_/ \   ;(_ o._)__|(  .  .-' : (  '\_/ \   ;|  |/    \|  | 
|( ' ) |   ||   `-'  /     |  (_.\.' / |  | \ `'   / \ `"/  \  ) / |(_,_)     `-'`-'|___\ `"/  \  ) / |  '  /\  `  | 
(_{;}_)|   | \      /      |       .'  |  |  \    /   '. \_/``".'  |   |       |        \'. \_/``".'  |    /  \    | 
'(_,_) '---'  `-..-'       '-----'`    ''-'   `'-'      '-----'    '---'       `--------`  '-----'    `---'    `---`

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

# Metadata
__authors__ = "Pierre-Yves Gousenbourger, Sandra Soares-Frazao, Robin Meurice, Charles Ryckmans, Nathan Delpierre, Martin Petitjean"
__contact__ = "pierre-yves.gousenbourger@uclouvain.be"
__copyright__ = "MIT"
__date__ = "2022-09-05"
__version__= "0.0.1"

# internal modules

# external modules contained in requirements.txt
import numpy as np
import os
import sys
from scipy.interpolate import griddata
import subprocess
import shlex
import pandas as pd
from .watlab import Mesh, WatlabExport, WatlabModel, _INPUT_NAME, _MESHCHECKER_EDGES_FILE
from .utils import extract_values_from_tif, interpolate_points

_HYDROFLOW_NAME = "hydroflow"
#%%% A name for hydroflow executable
if sys.platform == "win32":
    _HYDROFLOW_EXECUTABLE = _HYDROFLOW_NAME+".exe"
elif sys.platform == "Darwin":
    raise OSError("MacOS is not yet supported")
elif sys.platform == "linux" or sys.platform == "linux2":
    raise OSError("Linux is not yet supported")
#%%% Corresponds to the initial conditions variables
_INITIAL_WATER_LEVEL = "initial_water_level"
_INITIAL_WATER_DISCHARGE = "initial_water_discharge"
_BEDROCK_LEVEL = "bedrock_level"
_FRICTION_COEFFICIENTS = "friction_coefficients"
#%%% Corresponds to the boundary conditions variables
_TRANSMISSIVE_BOUNDARIES = "transmissive_edges"
_WALL_BOUNDARIES ="wall_edges"
_BOUNDARY_WATER_LEVEL = "boundary_water_level"
_BOUNDARY_WATER_DISCHARGE = "boundary_water_discharge"
_BOUNDARY_SEDIMENTS_DISCHARGE = "boundary_sediments_discharge"
_BOUNDARY_HYDROGRAM = "boundary_hydrogram"
_BOUNDARY_LIMNIGRAM = "boundary_limnigram"
##### Default values for IO folders
##### Default values for generated files

_DATA_TEMPLATE_FILE = "data_template.txt"
_FIXED_BED_FILE ="fixedBed.txt"
_FRICTION_FILE = "friction_values.txt"
# path to hydroflow
_dir_path_to_executable = os.path.join(os.path.dirname(__file__),"bin")
_root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_hydroflow_path():
    """
    Returns
    --------
    String
    Path of the hydroflow.exe folder
    """
    return _dir_path_to_executable


def _compile_code(isParallel=False):
    """
        Compiles the C++ code using g++.
    The compilation is done using the following command:
        g++ -O3 -fopenmp -pthread -o hydroflow src/cpp/*.cpp src/cpp/writer/*.cpp src/cpp/interfaces/*.cpp src/cpp/helpers/*.cpp -std=c++20
    The compilation is done in the directory where the C++ code is located.
    The compilation is done using the subprocess module.
    The subprocess module is used to run the g++ command.
    The shlex module is used to split the command into a list of strings.
    The cwd parameter of the subprocess module is used to specify the directory 
        where the compilation is done.
    The wait() method of the subprocess module is used to wait for the 
        compilation to finish.
    """
    relpath = os.path.relpath(_dir_path_to_executable,_root_path).replace('\\','/')
    src_files =  'src/cpp/*.cpp src/cpp/writer/*.cpp src/cpp/interfaces/*.cpp src/cpp/helpers/*.cpp src/cpp/physicalmodels/*.cpp'
    if isParallel:
        compiler_opt = '-O3 -fopenmp -pthread'
    else:
        compiler_opt = ''
    try:
        subprocess.call(shlex.split('g++ '+compiler_opt+' -o '+relpath+'/'+_HYDROFLOW_NAME+ ' '+src_files+' -std=c++20 -static'),
                               stdout=subprocess.PIPE,
                               shell=True,
                               cwd=_root_path,
                               text=True,
                               stderr=subprocess.PIPE)
        print("The code has been successfully compiled: the executable has been generated.")
        if isParallel: print("(Parallel version)")
    except subprocess.CalledProcessError as e:
        print("There were compiling errors, the code can not be run:")
        print("Error:", e)
    
class HydroflowModel(WatlabModel):
    """
    Hydrodynamic simulation model. 
    The simulation model is made of a physical Mesh and is linked to the Export class \n
    This class must be used to design your problem by providing a solver, initial and boundary conditions. 
    The function solve() is used to launch the simulation by calling the C++ solver. 
    """
    def __init__(self,mesh: Mesh):
        """Builder of the Model class. 
        To build a Model object, only a Mesh object is needed. 

        :param mesh: the mesh object describing the physical environment of the problem
        :type mesh: Mesh
        :param export: the export object that will be employed to export the related model data. 
        :type export: HydroflowExport object
        :param initial_conditions_keys: the list of the initial conditions keys that can be employed in the HydroflowModel
        :type initial_conditions_keys: list
        :param boundary_conditions_keys: the list of the boundary conditions keys that can be employed in the HydroflowModel
        :type boundary_conditions_keys: list
        """
        WatlabModel.__init__(self,mesh)
        self.export = HydroflowExport(self._mesh,self)
        #Main parameters of the simulation
        self.__Cfl = 0.90
        #Algorithm parameters
        self.__physical_model = 1
        self.__flux_scheme = 1 # self.__FLUX_SCHEME
        self.__flux_order = 1
        self.__slope_limiter = 0
        #Hydrodynamic part: initialization
        self.__is_fixed_bed_level = 0
        self.__is_friction = 0
        self.initial_conditions_keys.extend([_INITIAL_WATER_LEVEL, _INITIAL_WATER_DISCHARGE, _BEDROCK_LEVEL, _FRICTION_COEFFICIENTS])
        self.boundary_conditions_keys.extend([_TRANSMISSIVE_BOUNDARIES, _BOUNDARY_WATER_LEVEL, _BOUNDARY_WATER_DISCHARGE, _BOUNDARY_HYDROGRAM, _BOUNDARY_LIMNIGRAM,_WALL_BOUNDARIES])
    
    def export_data(self) -> None: 
        """ 
        Calls the export class to export the needed files in the input folder
        Please inspect the input folder to see the designed problem.
        Informations about initial conditions, nodes, edges or eventual gauges places are included
        """
        self.export.export()

    def solve(self,display=True,isParallel=False) -> None:
        """
        Calls the C++ executable of meshchecker if the parameter meshchecking of mesh is set to True
        Calls the C++ executable and solve the current designed model
        """
        if (self._mesh.meshchecking):
            self._launch_meschecker(display,isParallel=isParallel)
        self.__launch_code(display,isParallel=isParallel)

    def resume_simulation(self,pic_file,display=True,isParallel=False,isSameMesh=True):
        """Allows the user to restart a simulation from a former pic.txt file.

        :param pic_file: pic.txt file used as initial conditions for the simulation
        :type pic_file: string
        :param display: if True shows the cpp outputed informations, defaults to True
        :type display: bool, optional
        :param isParallel: if True the parallel version of the code is used, defaults to False
        :type isParallel: bool, optional
        :param isSameMesh: if True no interpolation is performed. Initial conditions are not interpolated, defaults to True
        :type isSameMesh: bool, optional
        """
        data = np.loadtxt(pic_file,skiprows=1)
        regions = list(self._mesh.regions.values())
        h_pic, qx_pic, qy_pic = data[:,3], data[:,4], data[:,5]

        if isSameMesh : 
            h_water, qx, qy = h_pic, qx_pic, qy_pic
        else: 
            x_coord_pic,y_coord_pic = data[:,0], data[:,1]
            old_points = np.column_stack((x_coord_pic.flatten(), y_coord_pic.flatten()))  
            X_barycenters, Y_barycenters = self._mesh.get_cells_barycenters()[:,0], self._mesh.get_cells_barycenters()[:,1]
            new_points = np.column_stack((X_barycenters, Y_barycenters))
            
            nearest_grid_h = griddata(old_points, h_pic, new_points, method='nearest')
            h_water = griddata(old_points, h_pic, new_points, method='linear')
            h_water[np.isnan(h_water)] = nearest_grid_h[np.isnan(h_water)]

            nearest_grid_qx = griddata(old_points, qx_pic, new_points, method='nearest')
            qx = griddata(old_points, qx_pic, new_points, method='linear')
            qx[np.isnan(qx)] = nearest_grid_qx[np.isnan(qx)] 
            nearest_grid_qy = griddata(old_points, qy_pic, new_points, method='nearest')
            qy = griddata(old_points, qy_pic, new_points, method='linear')
            qy[np.isnan(qy)] = nearest_grid_qy[np.isnan(qy)] 
            qx[h_water<10**-1], qy[h_water<10**-1] = 0, 0
            
        discharges = np.column_stack((qx,qy))
        for region in regions:
            region_tag = self._mesh.get_region_by_name(region) if isinstance(region,str) else region
            indexes = [self._mesh.tag_to_indexes.get(tag) for tag in self._mesh.region_cells[region_tag]]
            self.set_initial_water_height(str(region),h_water[indexes].tolist())
            self.set_initial_water_discharge(str(region),discharges[indexes].tolist())
        self.export_data()
        if display: print("Input Files Generated")
        self.solve(display,isParallel=isParallel)
        
    ##############################################
    #                                            #
    # Specific properties should be written here #
    #                                            #
    ##############################################
    
    @property
    def Cfl_number(self):
        """Convergence condition by Courant-Friedrichs-Lewy
            Must always be below 1

        :getter: Returns Courant-Friedrichs-Lewy number
        :setter: Sets Courant-Friedrichs-Lewy number
        :type: float
        """
        return self.__Cfl 

    @Cfl_number.setter    
    def Cfl_number(self,Cfl):
        self.__Cfl = Cfl

    @property
    def physical_model(self):
        """Assigns a physical model : you must decide to use only hydrodynamics or sediments...

        :getter: returns the physical model tag
        :setter: Sets Physical model tag: Hydrodynamics, sediments (1, 2,..)
        :type: int
        """
        return self.__physical_model
    
    @physical_model.setter
    def physical_model(self, physical_model_tag):
        self.__physical_model = physical_model_tag
        
    @property
    def flux_scheme(self):
        """Scheme used to compute the fluxes at the interfaces of the mesh
            FOR THE MOMENT ONLY 1 CORRESPONDING TO HLLC

        :getter: returns the flux scheme
        :setter: Sets scheme used to compute the fluxes at the interfaces of each edge (1, 2 or more)
        :type: int
        """
        return self.__flux_scheme

    @flux_scheme.setter
    def flux_scheme(self,flux_scheme):
        self.__flux_scheme = flux_scheme
    
    @property
    def flux_order(self):
        """order used to compute the fluxes

        :getter: returns the order used to compute the fluxes
        :setter: Sets the order used to compute the fluxes (1 or 2)
        :type: int (default : 1)
        """
        return self.__flux_order

    @flux_order.setter
    def flux_order(self,flux_order):
        self.__flux_order = flux_order
    
    @property
    def slope_limiter(self):
        """ This function assigns slope_limiter

        :getter: returns the slope_limiter
        :setter: 1 or 2 ???
        :type: int (default : 1)
        """
        return self.__slope_limiter

    @slope_limiter.setter
    def slope_limiter(self,slope_limiter):
        self.__slope_limiter = slope_limiter

    @property 
    def is_fixed_bed_level(self):
        """Indicates to the c++ code if there is a fixed bed level
        :return: 0 or 1 
        :rtype: Boolean of type int (0,1)
        """
        return self.__is_fixed_bed_level

    @property
    def is_friction(self):
        """Indicates to the c++ code if there is friction to be considered

        :return: 0 or 1 
        :rtype: Boolean of type int (0,1)
        """
        return self.__is_friction   
     
    #############################################
    #                                           #
    # Initial conditions should be written here #
    #                                           #
    #############################################
    
    def set_initial_water_height(self,regions,water_heights):
        """Sets the initial water height to the cells in the domain.    
           If only one value is given, all cells will get the same value.

        :param regions: the regions names (string) or the regions tags (int)
        :type regions: string or int
        :param water_heights: the values to be given to the cells in the correspondant region. 
        :type water_heights: float or list
        """
        tags = []
        def __initial_water_height(tags,water_heights,region):
            region_indexes = [self._mesh.tag_to_indexes.get(tag) for tag in tags]
            initial_conditions = self.get_initial_conditions()
            if _BEDROCK_LEVEL in initial_conditions.keys():
                bedrock_level = np.asarray(initial_conditions[_BEDROCK_LEVEL][1])[region_indexes]
            else:
                bedrock_level = self._mesh.get_cells_barycenters()[region_indexes,2]
            #evaluate water levels, since water levels are the initial condition                
            if isinstance(water_heights,(int, float)) : water_levels = water_heights*np.ones(len(region_indexes))+bedrock_level
            else:                                       water_levels = water_heights+bedrock_level
            self._set_initial_conditions(region,water_levels.tolist(),_INITIAL_WATER_LEVEL)
            
        if isinstance(regions,list) or isinstance(regions,tuple):
            for index,region in enumerate(regions): 
                tags = self._mesh.region_cells[self._mesh.get_region_by_name(region)] 
                __initial_water_height(tags,water_heights[index],region)
        else:  
            tags = self._mesh.region_cells[self._mesh.get_region_by_name(regions)] 
            __initial_water_height(tags,water_heights,regions)      
        
    def set_initial_water_level(self,regions,water_levels):
        """Sets the initial water levels to the cells in the domain.
           If only one value is given, all cells will get the same value.

        :param regions: the regions names (string) or the regions tags (int)
        :type regions: string or int
        :param water_levels: the values to be given to the cells in the correspondant region. 
        :type water_levels: float or list
        """
        self._set_initial_conditions(regions,water_levels, _INITIAL_WATER_LEVEL)
    
    def set_initial_water_discharge(self,regions,discharges):
        """Sets the initial water levels to the cells in the domain.
           If only one value is given, all cells will get the same value.

        :param regions: the regions names (string) or the regions tags (int)
        :type regions: string or int
        :param discharges: the values to be given to the cells in the correspondint region. 
                           Each entry must be composed of two elements (discharge x and discharge y).
        :type discharges: List
        """
        self._set_initial_conditions(regions,discharges,_INITIAL_WATER_DISCHARGE)

    def set_bedrock_level(self,regions,bedrock_levels):
        """Sets the initial bedrock level to the cells in the domain.
        
        :param bedrock_levels: the values to be given to the cells in the corresponding region. 
        :type bedrock_levels: float or list
        """
        self.__is_fixed_bed_level = 1
        self._set_initial_conditions(regions,bedrock_levels,_BEDROCK_LEVEL)
    
    def set_friction_coefficient(self,regions,friction_coefficients):
        """Sets the friction coefficients associated to each cell in the domain.
        If only one value is given, all cells will get the same value.

        :param regions: the regions names (string) or the regions tags (int)
        :type regions: string or int
        :param friction_coefficients: the values to be given to the cells in the corresponding region. 
        :type friction_coefficients: float or list or .tif file 
        """
        self.__is_friction = 1 
        if isinstance(friction_coefficients, str):
            tif_points_coordinates, friction_coefficient_map = extract_values_from_tif(friction_coefficients)
            friction_coefficients = interpolate_points(tif_points_coordinates, friction_coefficient_map, self._mesh.get_cells_barycenters()).tolist()
        self._set_initial_conditions(regions,friction_coefficients,_FRICTION_COEFFICIENTS)
    
    ##############################################
    #                                            #
    # Boundary conditions should be written here #
    #                                            #
    ##############################################
    def set_wall_boundaries(self,boundaries):
        """Defines which edges behave like wall interfaces.


        :param boundaries: the boundary names (string) or the boundary tags (int)
                           where the edges behave like wall interfaces.
        :type boundaries: string or int
        """
        # fictive value for transmissive boundaries
        values = True if np.size(boundaries) == 1 else [True]*np.size(boundaries)
        self._set_boundary_conditions(boundaries,values,_WALL_BOUNDARIES)
        
    def set_transmissive_boundaries(self,boundaries):
        """Defines which edges behave like a transmissive interfaces.


        :param boundaries: the boundary names (string) or the boundary tags (int)
                           where the edges behave like transmissive interfaces.
        :type boundaries: string or int
        """
        # fictive value for transmissive boundaries
        values = True if np.size(boundaries) == 1 else [True]*np.size(boundaries)
        self._set_boundary_conditions(boundaries,values,_TRANSMISSIVE_BOUNDARIES)

    def set_boundary_water_level(self,boundaries,water_levels):
        """Defines the imposed water level at edges of the boundaries.
        
        :param boundaries: the boundary names (string) or the boundary tags (int)
        :type boundaries: string or tag
        :param water_levels: the values to be given to the edges in the corresponding boundary.
        :type water_levels: float or list
        """
        self._set_boundary_conditions(boundaries,water_levels,_BOUNDARY_WATER_LEVEL)

    def set_boundary_water_discharge(self,boundaries,water_discharges):
        """Defines the imposed water discharge through the edges of the boundaries.
        You must introduce the total discharge. Positive value flows in the system
        
        :param boundaries: the boundary names (string) or the boundary tags (int)
        :type boundaries: string or int
        :param water_discharges: the values to be given to the edges in the corresponding boundary.
        :type water_discharges: float or list
        """
        def __corrected_water_discharge(boundary,water_discharge):
            boundary_length = self._mesh.get_boundary_length(boundary)
            return -water_discharge/boundary_length
            
        if isinstance(boundaries,list) or isinstance(boundaries,tuple):
            for i,boundary in enumerate(boundaries):
                water_discharge = __corrected_water_discharge(boundary,water_discharges[i])
                self._set_boundary_conditions(boundary,water_discharge,_BOUNDARY_WATER_DISCHARGE)
        else:
            self._set_boundary_conditions(boundaries,__corrected_water_discharge(boundaries,water_discharges),_BOUNDARY_WATER_DISCHARGE)
        
    def set_boundary_hydrogram(self,boundaries,hydrogram_paths):
        """Sets a hydrogram type of boundary condition
        Your file must be organized as follows : 
        nData : 
        t0 -Q0
        t1 -Q1
        t2 -Q3 etc....
        
        :param boundaries: the boundary names (string) or the boundary tags (int)
        :type boundaries: string or int
        :param hydrogram_paths: the paths of the hydrograms associated to the edges 
                                in the corresponding boundary.
        :type hydrogram_paths: string or list
        """
        self._set_boundary_conditions(boundaries,hydrogram_paths,_BOUNDARY_HYDROGRAM)

    def set_boundary_limnigram(self,boundaries,limnigram_paths):
        """Sets a limnigram type of boundary condition
        
        :param boundaries: the boundary names (string) or the boundary tags (int)
        :type boundaries: string or int
        :param limnigram_paths: the paths of the limnigrams associated to the edges 
                                in the corresponding boundary.
        :type limnigram_paths: string or list
        """
        self._set_boundary_conditions(boundaries,limnigram_paths,_BOUNDARY_LIMNIGRAM)

    def get_boundary_conditions(self):
        """Returns the boundary conditions in a dictionary"""
       
        conditions = self.get_conditions(self.boundary_conditions_keys)
        keys = conditions.keys()
        if _TRANSMISSIVE_BOUNDARIES in keys:
            conditions[_TRANSMISSIVE_BOUNDARIES] = conditions[_TRANSMISSIVE_BOUNDARIES][0]
        if _WALL_BOUNDARIES in keys:
            conditions[_WALL_BOUNDARIES] = conditions[_WALL_BOUNDARIES][0]
        return conditions
    
    def __launch_code(self,display=True,isParallel=False):
        """
        This function launches the Hydroflow code.
        It first checks if the Hydroflow code exists in the Hydroflow folder.
        If it does not exist, it compiles the code.
        Then, it launches the Hydroflow code.
        The Hydroflow code is launched with the following input:
        - the path to the data.txt file
        """

        if os.path.exists(os.path.join(_dir_path_to_executable,_HYDROFLOW_EXECUTABLE)):
            if display: print(_HYDROFLOW_EXECUTABLE + " exists")
        else:
            if display: print("The code is being compiled...")
            _compile_code(isParallel=isParallel)
            
        if display: print("Launching the executable ...")  
        
        data_file_path = self.export.data_file_path
        executable_cmd = os.path.join(_dir_path_to_executable, _HYDROFLOW_EXECUTABLE)

        args = [executable_cmd, '-f', data_file_path]
        
        process = subprocess.Popen(args, 
                                   stdout = subprocess.PIPE, 
                                   stderr = subprocess.STDOUT,
                                   cwd = self._current_path,
                                   universal_newlines=True, 
                                   text = True)
        if display:
            for line in iter(process.stdout.readline, ""):
                sys.stdout.write('\r'+line[:-1])
                sys.stdout.flush()
        process.wait()

class HydroflowExport(WatlabExport):
    """Exports the input files
    
    :param mesh: a mesh object from the hydroflow lib
    :type mesh: mesh
    :param model: a model object
    :type model: model
    """
    # Class variables 

    def __init__(self, mesh: Mesh, model: HydroflowModel):
        """
        Constructs the Mesh object based on an .msh file.
        """
        WatlabExport.__init__(self,mesh,model)
        self.boundary_conditions_code =  {
            _TRANSMISSIVE_BOUNDARIES : -2,
            _BOUNDARY_WATER_LEVEL : -4, 
            _BOUNDARY_WATER_DISCHARGE : -3,
            _BOUNDARY_HYDROGRAM : -33,
            _BOUNDARY_LIMNIGRAM : -44,
            _WALL_BOUNDARIES : -5}

    def export(self):
        """Export all .txt files in the input folder:
        
        :return: self.__NODES_NAME, self.__CELLS_NAME, self.__EDGES_NAME, self.__INITIAL_CONDITIONS_NAME, self.__FRICTION_NAME
            self.__BOUNDARY_NAME, self.__PICTURE_NAME, self.__DATA_NAME, self.__SEDIMENT_LEVEL_NAME
        :rtype: .txt    
        """
        os.makedirs(self._INPUT_FOLDER_PATH,exist_ok=True)
        os.makedirs(self._OUTPUT_FOLDER_PATH,exist_ok=True)
        #Basic Watlab exports 
        self._export_watlab_basic_data()
        #Adapted exports for Hydroflow
        self._export_hydrodynamics_data()
        self.__export_data()
    
    def _export_hydrodynamics_data(self):
        """A private function that exports the boundary conditions, the initial conditions, the friction coeff. and the bedrock levels.
        """
        self._export_edges()
        self._export_initial_conditions()
        self._export_friction()
        self._export_bedrock_level()
    
    @property
    def friction_file_path(self):
        return os.path.join(self.input_folder_name,_FRICTION_FILE)
    
    @property
    def fixed_bedrock_level_path(self):
        return os.path.join(self.input_folder_name,_FIXED_BED_FILE)
    
    def _export_edges(self):
        """Exports the edges from the GSMH mesh to a file.

        :return: A text file containing the number of edges, the corresponding nodes and if requested, 
            the left and right adjacent cells.
            First line: n_edges
            Each following line is formatted as [left_cell_tag, right_cell_tag, node_tag_1, node_tag_2, boundary_condition_code, value_boundary_condition (double or string)].
        :rtype: .txt
        """
        if (self._mesh.meshchecking):
            output_path = os.path.join(self.input_folder_name,_MESHCHECKER_EDGES_FILE)
        else:
            output_path = self.edges_file_path
        f = open(output_path,'w')
        f.write(str(self._mesh.nEdges)+'\n')
        f.close()

        # preparing output
        fmt = '%d', '%d', '%d', '%d', '%s', '%s'
        tags,edge_nodes,edge_cells = self._mesh.edges
        edge_cells[edge_cells != -1] = [self._mesh.tag_to_indexes.get(tag) for tag in edge_cells[edge_cells != -1]]

        output = np.hstack((edge_cells,edge_nodes-1))

        used_boundary_conditions = self.model.get_boundary_conditions().keys()
        bc_value =  np.empty(len(tags),dtype=object)
        bc_code =  -np.ones(len(tags),dtype=int)
        bc_value[:] = np.nan

        for condition in used_boundary_conditions: 
            if condition == _TRANSMISSIVE_BOUNDARIES or condition == _WALL_BOUNDARIES:
                condition_edge = np.asarray(self.model.get_boundary_conditions()[condition])
                output[condition_edge-1,1] = self.boundary_conditions_code[condition]
            else:   
                condition_edge = np.asarray(self.model.get_boundary_conditions()[condition][0])
                condition_value = np.asarray(self.model.get_boundary_conditions()[condition][1])
                output[condition_edge-1,1] = self.boundary_conditions_code[condition]
                bc_value[condition_edge-1] = condition_value
            bc_code[condition_edge-1] = self.boundary_conditions_code[condition]
            
        output = pd.DataFrame(output)
        output['bc_code'] = bc_code
        output['bc_valeur'] = bc_value
        output.fillna(value='', inplace=True)

        with open(output_path,'ab') as f:
            np.savetxt(f,output.values, delimiter=" ", fmt=fmt)

    def _export_initial_conditions(self):
        """Exports the water and discharge initial conditions to a file

        :param tag: Negative (default): returns the initial conditions for the cells corresponding to the given data
            Positive: returns all initial conditions
        :type: int
        :return: A text file named after OUTPUT_NAME containing the initial water depth and water discharges for each cells
            Each line is formatted as [h_w, p, q].
        :rtype: .txt
        """
        fmt = '%1.6f','%1.6f','%1.6f'
        initial_conditions = self.model.get_initial_conditions()
        initial_export_conditions = np.zeros((self._mesh.nCells,3))

        if _INITIAL_WATER_LEVEL not in initial_conditions:
            pass 
        else:
            water_level = np.array([initial_conditions[_INITIAL_WATER_LEVEL][1]]).T
            water_level_cells_tags = initial_conditions[_INITIAL_WATER_LEVEL][0]
            water_level_cells_index = [self._mesh.tag_to_indexes.get(tag) for tag in water_level_cells_tags]
            initial_export_conditions[water_level_cells_index,0] = water_level.reshape(len(water_level),)

        if _INITIAL_WATER_DISCHARGE not in initial_conditions:
            pass 
        else:
            discharge = np.array(initial_conditions[_INITIAL_WATER_DISCHARGE][1])
            discharge_cells_tags = initial_conditions[_INITIAL_WATER_DISCHARGE][0]
            discharge_cells_index  = [self._mesh.tag_to_indexes.get(tag) for tag in discharge_cells_tags]
            initial_export_conditions[discharge_cells_index,1:3] = discharge.reshape(len(discharge),2)
            
        np.savetxt(self.initial_conditions_file_path,initial_export_conditions, delimiter=" ", fmt=fmt)
        
    def _export_friction(self):
        """Exports the friction coefficients to a file.
            Those coefficients are retrieved from the `initial_conditions` dictionary using the key specified in `self.model_variables_dic["FRICTION_COEFFICIENTS"]`. 
            If this key is not present in the dictionary, the function does nothing.
        
        :return: an array is saved to a file with the filename being the concatenation of the folder path, INPUT_NAME, and get_FRICTION_NAME. The output format is specified using the `fmt` variable.
        :rtype: .txt
        """
        self._export_blind_data(_FRICTION_COEFFICIENTS,self.friction_file_path)
    
    def _export_bedrock_level(self):
        """Exports the initial bedrock level to a file.
            The initial bedrock level is retrieved from the `initial_conditions` dictionary using the key specified in `self._model_variables_dic["BEDROCK_LEVEL"]`. 
            If this key is not present in the dictionary, the function does nothing.

        :return: an array is saved to a file with the filename being the concatenation of the folder path, INPUT_NAME, and BEDROCK_NAME. 
            The output format is specified using the `fmt` variable.
        :rtype: .txt
        """
        self._export_blind_data(_BEDROCK_LEVEL,self.fixed_bedrock_level_path)
        
    def __export_data(self):
        """Generates a txt file based on a template where the informations about the model and the mesh are summarized
            This function will delete the EDGES_NAME file if existing and clean all the pics in the Output folder.

        :return: A text file containing the parameters of the simulation
        :rtype: .txt
        """

        this_dir = os.path.join(os.path.dirname(__file__),"data")
        myfile_template = os.path.join(this_dir,_DATA_TEMPLATE_FILE)        
        with open(myfile_template, 'r') as f:
            template = f.read()
        
        input_data = {'Simulation Name': self.model.name,
                    't0': str(self.model.starting_time),'tend':  str(self.model.ending_time),'CFL': str(self.model.Cfl_number),
                    'output_folder': self._OUTPUT_FOLDER_NAME+"\\\\",
                    'nodes_file': self.nodes_file_path,
                    'cells_file': self.cells_file_path,
                    'interfaces_file': self.edges_file_path,
                    'physical_model': self.model.physical_model, 
                    'flux_scheme': self.model.flux_scheme,
                    'reconstruction_order': self.model.flux_order,
                    'slope_limiter': self.model.slope_limiter 
                                                if self.model.flux_order == 2 
                                                else ' '.join(["!", str(self.model.slope_limiter)]),
                    'hydrodynamic_initial_conditions':  self.initial_conditions_file_path,
                    'fixed_bed_level': self.model.is_fixed_bed_level,
                    'fixed_bed_level_file': self.fixed_bedrock_level_path
                                                if self.model.is_fixed_bed_level 
                                                else ' '.join(["!", str(self.fixed_bedrock_level_path)]),
                    'isFriction': self.model.is_friction,
                    'isFrictionFile': self.friction_file_path
                                                if self.model.is_friction 
                                                else ' '.join(["!",str(self.friction_file_path)]),
                    'is_sediment_transport': '!',
                    'is_initial_sediment_level': '!', 
                    'initial_sediment_level_file':  '!',
                    'sedimentological_parameters':'!',
                    'is_bank_failure':'!',
                    'bank_failure_tool':  '!',
                    'bank_failure_parameters': '!',
                    'fixed_bank_file':  '!',
                    'mass_conservation_check':'!',
                    'enveloppe_of_results': self.model.time_step_enveloppe,
                    'is_picture': self.model.is_picture,
                    'snapshots_of_flow': self.pictures_file_path 
                                                if self.model.is_picture 
                                                else ' '.join(["!", str(self.pictures_file_path)]),
                    'is_gauges': self.model.is_gauge,
                    'gauges':  self.gauge_file_path if self.model.is_gauge 
                                                else ' '.join(["!",str(self.gauge_file_path)])    ,
                    'is_discharge_measured': self.model.is_discharge_measurement_section,
                    'discharge_measured':  self.discharge_measurement_section_file_path
                                                if self.model.is_discharge_measurement_section 
                                                else ' '.join(["!",str(self.discharge_measurement_section_file_path)])
                    }
        
        data_file = template.format(**input_data)
        
        with open(self.data_file_path, 'w') as f:
            f.write(data_file)
# %%
