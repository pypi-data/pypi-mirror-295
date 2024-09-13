import argparse
import os
from sage_lib.partition.Partition import Partition 
from sage_lib.IO.structure_handling_tools.AtomPosition import AtomPosition 
from sage_lib.IO.EigenvalueFileManager import EigenvalueFileManager 
from sage_lib.IO.DOSManager import DOSManager 

from sage_lib.IO.OutFileManager import OutFileManager 
from typing import List, Tuple, Optional

def generate_test():
    """
    ( 0 )
    """
    from sage_lib.test import test 
    test.test()

def generate_export_files(path:str, source:str=None, forces_tag:str=None, energy_tag:str=None, index:int=None, 
                        subfolders:bool=False, output_path:str=None, output_source:str=None, verbose:bool=False, 
                        bond_factor:float=None):
    """
    ( 1 )
    Export atomic position files from a specified source format to another format.

    This function is used to convert the format of atomic position files, which is often necessary for compatibility with different simulation tools or visualization software.

    Parameters:
    path (str): Path to the directory containing source format files.
    source (str, optional): Source format of the files (e.g., 'VASP').
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the converted files will be saved.
    output_source (str, optional): Target format for exporting (e.g., 'PDB').
    verbose (bool, optional): If True, provides detailed output during execution.

    Returns:
    None
    """
    PT = Partition(path)
    PT.read_files( file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)
    PT.export_files(file_location=output_path, source=output_source, label='enumerate', bond_factor=bond_factor, verbose=verbose)

def generate_plot(  path:str, source:str=None, forces_tag:str=None, energy_tag:str=None, index:int=None,
                    subfolders:bool=False, output_path:str=None, output_source:str=None, verbose:bool=False, 
                    plot:str=None, 
                    fermi:float=None, emin:float=None, emax:float=None,
                    cutoff:float=None, number_of_bins:int=None):
    """
    ( 2 )
    Generate plots from simulation data.

    This function processes simulation data and generates plots, such as band structure or molecular structures, based on the data and specified plot type.

    Parameters:
    path (str): Path to the directory containing the simulation data files.
    source (str, optional): Source of the files (e.g., 'VASP').
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the plots will be saved.
    plot (str, optional): Type of plot to generate (e.g., 'band').
    verbose (bool, optional): If True, provides detailed output during execution.
    fermi (float, optional): Fermi level energy, important for certain types of plots.

    Returns:
    None
    """
    output_path = output_path if output_path is not None else '.'
    PT = Partition(path)
    PT.read_files( file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)

    if plot.upper() == 'BANDS':

        if fermi is None:
            # === read DOCAR === #
            DM = DOSManager(path + "/DOSCAR")
            DM.read_DOSCAR()
            fermi = DM.fermi

        # === read EIGENVAL === #
        EFM = EigenvalueFileManager(file_location=path+"/EIGENVAL", fermi=fermi )
        EFM.read_EIGENVAL()

        EFM.plot(subtract_fermi=True, save=True, emin=emin, emax=emax)

    elif plot.upper() == 'RBF':
        if isinstance(index,int): 
            file_location = output_path+f'/frame{index}'
            PT.create_directories_for_path(file_location)
            PT.containers[index].AtomPositionManager.plot_RBF(periodic_image=0, cutoff=cutoff, number_of_bins=number_of_bins, output_path=file_location,
                                                        bin_volume_normalize=True, number_of_atoms_normalize=True, density_normalize=True)
        else:
            for index, conteiner in enumerate(PT.containers):
                file_location = output_path+f'/frame{index}'
                PT.create_directories_for_path(file_location)
                conteiner.AtomPositionManager.plot_RBF(periodic_image=0, cutoff=cutoff, number_of_bins=number_of_bins, output_path=file_location,
                                                        bin_volume_normalize=True, number_of_atoms_normalize=True, density_normalize=True)

def generate_AbInitioThermodynamics(path: str, source: Optional[str] = None, forces_tag: Optional[str] = None, energy_tag: Optional[str] = None, subfolders: bool = False, output_path: Optional[str] = None,
                                    output_source: Optional[str] = None, verbose: bool = False, index: Optional[int] = None,
                                    plot: Optional[str] = None, reference: Optional[List] = None, k: Optional[int] = None, optimize: Optional[bool] = None,
                                    r_cut: float = 4.0, n_max: int = 12,l_max: int = 12, sigma: float = 0.01, regularization: float = 1e-5, 
                                    components: int = 10, compress_model: str = 'umap', cluster_model: str = 'dbscan', eps: float = 0.7, min_samples: int = 2 ):
    """
    ( 3 )
    """
    output_path = output_path if output_path is not None else '.'
    PT = Partition(path)
    PT.read_files( file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)

    value = {
        plot: {
            'reference': reference,
            'k': k,
            'optimize': optimize,
            'output_path': output_path,
            'verbose': verbose,
            'cache': True,

            'r_cut': r_cut,
            'n_max': n_max,
            'l_max': l_max,
            'sigma': sigma,
            'regularization': regularization,
            'components': components,
            'compress_model': compress_model,
            'cluster_model': cluster_model,
            'eps': eps,
            'min_samples': min_samples
        }
    }

    if plot.upper() in ['PHASE_DIAGRAM', 
                        'ENSEMBLE_ANALYSIS',
                        'COMPOSITION_ANALYSIS',
                            ]: 
        PT.handleABITAnalysis( values=value  )

    else:
        assert False, "Unsupported plot type encountered: {}".format(plot)

def generate_BLENDER(   path:str, source:str=None, forces_tag:str=None, energy_tag:str=None, index:int=None,
                        subfolders:bool=False, output_path:str=None, output_source:str=None, verbose:bool=False, 
                plot:str=None, resolution:list=None, samples:int=None, fog:bool=None, render:bool=False, 
                sigma:float=None, scale:float=None, camera:list=None, repeat:list=None, 
                ):
    # ( 4 )
    # Initialize the DFTPartition object
    PT = Partition()

    # Read files and apply configurations
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)
    
    values = {
        'samples': samples,
        'resolution_x': resolution[0],
        'resolution_y': resolution[1],
        'fog': fog,
        'render':render,
        'sigma': sigma,
        'scale': scale,
        'camera': camera,
        'repeat': repeat,
        'verbose': verbose,
    }

    PT.handleBLENDER( values={f'{plot}':values}  )

def generate_config(path: str, source: Optional[str] = None, forces_tag: Optional[str] = None, 
                    energy_tag: Optional[str] = None, index: Optional[int] = None,
                    subfolders: bool = False, output_path: Optional[str] = None, 
                    output_source: Optional[str] = None, verbose: bool = False, 

                    config_path: Optional[str] = None, config_source: Optional[str] = None):
    """
    ( 5 )
    Generates a configuration by reading, processing, and exporting files.

    This function orchestrates the workflow of partitioning data, reading configuration setup, 
    and exporting files with enumeration. It provides verbose output for debugging and tracking.

    :param path: Path to the data files
    :param source: Source identifier for the data files (optional)
    :param forces_tag: Tag to identify forces data in the files (optional)
    :param energy_tag: Tag to identify energy data in the files (optional)
    :param index: Index to use for the container (optional)
    :param subfolders: Flag to include subfolders in the data reading process (default: False)
    :param output_path: Path for exporting the processed files (optional)
    :param output_source: Source identifier for the exported files (optional)
    :param verbose: Flag for verbose output (default: False)
    :param config_path: Path to the configuration setup files (optional)
    :param config_source: Source identifier for the configuration files (optional)

    :return: None
    """
    PT = Partition(path)
    
    # Step 1: Read input files
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, 
                  forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, 
                  container_index=index)
    
    # Step 2: Read configuration setup (if provided)
    if config_path:
        PT.read_config_setup(file_location=config_path, source=config_source, verbose=verbose)
    
    # Step 3: Export processed files
    if output_path:
        PT.export_files(file_location=output_path, source=output_source, 
                        label='enumerate', verbose=verbose)
    
    if verbose:
        print(f">> Config generated successfully.")
        print(f"Position: {path}({source})(subfolders: {subfolders}) + \n"
              f"InputFiles: {config_path}({config_source}) >> Output: \n"
              f"{output_path}({output_source})")

def generate_MD(path:str, source:str=None, subfolders:bool=False, forces_tag:str=None, energy_tag:str=None, output_path:str=None, output_source: str = None,
                    plot:str=None, reference:str=None, ff_energy_tag:str=None, ff_forces_tag:str=None, sigma:float=None, topology:str=None, wrap:bool=None,
                    T:float=None, q:float=None, chemical_ID:list=None, dt:float=None,
                    verbose:bool=False, index:int=None, tranparency:bool=None, bins:int=None, save:bool=None):
    """
    Generate plots from simulation data.

    This function processes simulation data and generates plots, such as band structure or molecular structures, based on the data and specified plot type.

    Parameters:
    path (str): Path to the directory containing the simulation data files.
    source (str, optional): Source of the files (e.g., 'VASP').
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the plots will be saved.
    plot (str, optional): Type of plot to generate (e.g., 'band').
    verbose (bool, optional): If True, provides detailed output during execution.
    fermi (float, optional): Fermi level energy, important for certain types of plots.

    Returns:
    None
    """
    # 'count_species', 'displacements', 'RBF', 'evaluate_ff', 'bond_distance_tracking', 'molecule_formation_tracking'
    output_path = output_path if output_path is not None else '.'
    PT = Partition(path)
    PT.read_files( file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)


    if plot.upper() == 'PATH_TRACKING':
        PT.handleMDAnalysis( values= {'PATH_TRACKING':{'wrap':wrap, 'tranparency':tranparency, 'bins':bins, 'verbose':verbose, 'save':save} }  )

    elif plot.upper() == 'RBF':
        PT.handleMDAnalysis( values= {'RBF':{'output_path':output_path, 'verbose':verbose} }  )

    elif plot.upper() == 'COUNT_SPECIES':
        PT.handleMDAnalysis( values= {'COUNT_SPECIES':{'output_path':output_path, 'verbose':verbose, 'sigma':sigma} }  )

    elif plot.upper() == 'EVALUATE_FF':
        PT.handleMDAnalysis( values= {'EVALUATE_FF':{'output_path':output_path, 'ff_energy_tag':ff_energy_tag, 'ff_forces_tag':ff_forces_tag, 'verbose':verbose} }  )

    elif plot.upper() == 'BOND_DISTANCE_TRACKING':
        PT.handleMDAnalysis( values= {'BOND_DISTANCE_TRACKING':{'reference':reference, 'sigma':sigma, 'output_path':output_path, 'verbose':verbose} }  )
    
    elif plot.upper() == 'MOLECULE_FORMATION_TRACKING':
        PT.handleMDAnalysis( values= {'MOLECULE_FORMATION_TRACKING':{'sigma':sigma, 'topology':topology, 'verbose':verbose} }  )
        PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)
    
    elif plot.upper() == 'FORCES':
        PT.handleMDAnalysis( values= {'FORCES':{'reference':reference, 'sigma':sigma, 'output_path':output_path, 'verbose':verbose} }  )
    
    elif plot.upper() == 'DIFFUSION':
        assert isinstance(T, (int, float)), "Error: Temperature (T) must be a number (int or float)."
        assert T > 0, "Error: Temperature (T) must be greater than zero."

        assert isinstance(q, list), "Error: Charge (q) must be a number (int or float)."

        assert isinstance(chemical_ID, list), "Error: Chemical ID (ID) must be a string."
        assert chemical_ID, "Error: Chemical ID (ID) cannot be empty."

        PT.handle_conductivity_analysis( analysis_parameters= {'analysis':{'T':T, 'q':q, 'dt':dt, 'ID':chemical_ID,'output_path':output_path, 'verbose':verbose} } )

def generate_defects(path:str, source:str=None, forces_tag:str=None, energy_tag:str=None, subfolders:bool=False, index:int=None, output_path:str=None, output_source:str=None, verbose:bool=False,  
                    species:list=None, new_species:list=None, defect:str=None, Nw:int=None,
                    distribution:str=None, fill:bool=None, atom_groups:list=None, group_numbers:list=None, repetitions:bool=None,
                    iterations:int=None):
    """
    Generate configurations with vacancies for computational chemistry simulations.

    Parameters:
    - path (str): Path to the directory containing input files.
    - source (str, optional): Type of source files, default is 'VASP'.
    - subfolders (bool, optional): Flag to include subdirectories in the search.
    - verbose (bool, optional): If True, prints additional information during execution.

    Uses the Partition class from the sage_lib to read, process, and generate
    DFT (Density Functional Theory) variants with vacancies.
    """
    # Initialize a Partition object with the given path
    PT = Partition(path)
    # Read files and generate DFT variants with vacancies
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, index=index)

    #PT.generate_variants('DEFECTS', values= [ {'defect':defect, 'species':species, 'new_species':new_species} ] )
    
    values = {  'iterations': iterations, 
                'repetitions': repetitions,
                'distribution':distribution, 
                'fill':fill, 
                'atom_groups':atom_groups, 
                'group_numbers':group_numbers,
                'Nw':Nw, }
                
    PT.generate_configurational_space(values=values, verbose=verbose) 
    
    # Export the generated files back to the specified path
    PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)

def generate_disassemble_surface(path, steps=5, final_distance=5.0, atoms_to_remove=None, subfolders=False, verbose=False):
    """
    Generate configurations for disassembling the surface.

    Parameters:
    - path (str): Path to the VASP files directory.
    - steps (int): Number of steps in the disassembly process.
    - final_distance (float): Final distance between layers or atoms.
    - atoms_to_remove (int or None): Specific number of atoms to remove.
    - verbose (bool): If True, prints additional information.
    """
    SSG = SurfaceStatesGenerator(path)
    read_files(partition=SSG, path=path, subfolders=subfolders)

    SSG.generate_disassemble_surface(steps=steps, final_distance=final_distance, atoms_to_remove=atoms_to_remove)
    SSG.exportVaspPartition()

def generate_dimers(path: str = None, source: str = None, forces_tag:str=None, energy_tag:str=None, subfolders: bool = None, 
                    labels: list = None, steps: int = 10, initial_distance: float = None, final_distance: float = None, 
                    vacuum_tolerance: float = 18.0, 
                    output_path: str = None, output_source: str = None, index:int=None, verbose: bool = False):
    """
    Generate configurations for a dimer search in a computational chemistry context.

    This function is designed to set up and export multiple configurations of dimers (pairs of atoms or molecules) 
    based on specified parameters. It is useful in simulations where interactions between two specific atoms or molecules
    are of interest, particularly in the context of Density Functional Theory (DFT) or similar computational methods.

    Parameters:
    - path (str, optional): Path to the directory containing the initial data files.
    - source (str, optional): Source type of the initial data files (e.g., 'VASP', 'xyz').
    - subfolders (bool, optional): Flag to include subfolders in the search for data files.
    - labels (list of str, optional): List of atom labels to include in the dimer search. 
      For example, ['O', 'H'] to create dimers involving oxygen and hydrogen.
    - steps (int, optional): Number of iterative steps in the generation process. 
      Determines the granularity of the dimer configuration changes (default: 10).
    - initial_distance (float, optional): Initial distance between atoms in the dimer configuration.
    - final_distance (float, optional): Final distance after configuration adjustments.
    - vacuum_tolerance (float, optional): The vacuum distance around the dimer structure (default: 18.0 Ångströms).
    - output_path (str, optional): Path for exporting the generated dimer configuration files.
    - output_source (str, optional): Format for exporting the files (e.g., 'VASP', 'POSCAR').
    - verbose (bool, optional): If set to True, enables verbose output for debugging purposes.

    The function initializes a Partition object, reads files, generates dimer variants with specified distances,
    and exports the files to the specified output path. It utilizes the Partition class's methods to handle
    the file operations and variant generations.

    Example Usage:
    generate_dimers(path='./data', source='VASP', labels=['H', 'O'], steps=5, 
                    initial_distance=0.7, final_distance=1.5, output_path='./output', output_source='VASP')
    """
    # Initialize the Partition object with the given path
    PT = Partition(path)

    # Read files from the specified location, considering subfolders if specified
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)

    # Generate dimer variants based on the provided parameters
    PT.handleDimers(values=[{'AtomLabels': labels, 'initial_distance': initial_distance, 
                                    'final_distance': final_distance, 'steps': steps, 
                                    'vacuum_tolerance': vacuum_tolerance}], 
                    file_location=output_path)

    # Export the generated files to the specified output location and format
    PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)


def generate_band_calculation(path:str, points:int, special_points:str, source:str=None, subfolders:bool=False, output_path:str=None, verbose:bool=False):
    """
    Generate and export band structure calculation files.

    This function creates the necessary files for performing band structure calculations using Density Functional Theory (DFT) data. It sets up the calculation parameters and exports them in a format suitable for VASP.

    Parameters:
    path (str): Path to the directory containing VASP files.
    points (int): Number of k-points in each segment of the band path.
    special_points (str): String representing high-symmetry points in the Brillouin zone.
    source (str, optional): Source of the files (default is None, typically set to 'VASP').
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the output files will be saved.
    verbose (bool, optional): If True, provides detailed output during execution.

    Returns:
    None
    """
    DP = Partition(path)
    read_files(partition=DP, path=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)

    DP.generate_variants('band_structure', values=[{'points':points, 'special_points':special_points}])
    DP.exportVaspPartition()

def generate_json_from_bands(path:str, fermi:float, source:str=None, forces_tag:str=None, energy_tag:str=None, subfolders:bool=False, output_path:str=None, verbose:bool=False):
    """
    Generate a JSON file from band structure data.

    This function reads the band structure data from VASP output files, processes it, and exports it to a JSON file. This is useful for further analysis or visualization of the band structure.

    Parameters:
    path (str): Path to the directory containing VASP files.
    fermi (float): Fermi level energy. If not provided, it will be read from the DOSCAR file.
    source (str, optional): Source of the files ('VASP' is a common option).
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the JSON file will be saved.
    verbose (bool, optional): If True, provides detailed output during execution.

    Returns:
    None
    """
    if source.upper() == 'VASP':
        # read fermi level from DOSCAR
        if fermi is None:
            # === read DOCAR === #
            DM = DOSManager(path + "/DOSCAR")
            DM.read_DOSCAR()
            fermi = DM.fermi

        # === read POSCAR === #
        PC = AtomPosition(path + "/POSCAR")
        PC.read_POSCAR()
        cell = PC.latticeVectors

        # === read EIGENVAL === #
        EFM = EigenvalueFileManager(file_location=path + "/EIGENVAL", fermi=fermi, cell=cell)
        EFM.read_EIGENVAL()

    EFM.export_as_json(output_path+'/band_structure.json')

def generate_edit_positions(path: str, source: str = None, forces_tag:str=None, energy_tag:str=None, subfolders: bool = False, output_path: str = None, index:int=None,
                            output_source: str = None, verbose: bool = False, edit: str = None, N: int = None, direction:str=None, 
                            std: float = None, repeat: list = None, compress_min: list = None, compress_max: list = None,
                            init_index:int=None, mid_index:int=None, end_index:int=None, degree:int=None, first_neighbor:bool=None):
    """
    Modifies and exports atomic positions based on specified editing operations.

    This function applies various editing operations like 'rattle', 'supercell', or 'compress' to the atomic positions
    in the provided path and exports the modified structures.

    Parameters:
        path (str): Path to the input files.
        source (str, optional): Source type of the input files.
        subfolders (bool, optional): Flag to include subfolders in file reading.
        output_path (str, optional): Path for exporting the edited files.
        output_source (str, optional): Source type for exporting files.
        verbose (bool, optional): Enables verbose output.
        edit (str, optional): Type of editing operation ('rattle', 'supercell', 'compress').
        N (int, optional): Parameter specific to the 'rattle' and 'compress' edit.
        std (float, optional): Standard deviation parameter for the 'rattle' edit.
        repeat (list, optional): Repetition vector for the 'supercell' edit.
        compress_min (list, optional): Minimum compression factor for the 'compress' edit.
        compress_max (list, optional): Maximum compression factor for the 'compress' edit.
    
    Raises:
        ValueError: If required parameters for specific edits are not provided.
    """
    # Initialize the DFTPartition object
    PT = Partition(path)

    # Read files from the specified path
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)

    # Apply the specified movement to the atomic positions
    if edit.lower() == 'rattle':
        # Ensure that N and std are provided for the 'rattle' move
        if N is None or std is None:
            raise ValueError("For the 'rattle' edit, both 'N' and 'std' parameters must be provided.")
        
        values = {'N': N, 'std': [std]}
        PT.containers = PT.handleRattle(values=values)
        PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)

    elif edit.lower() == 'supercell':
        # Ensure that N and std are provided for the 'rattle' move
        if repeat is None:
            raise ValueError("For the 'supercell' edit, the 'repeat' parameter must be provided.") 

        for container in PT.containers:
            container.AtomPositionManager.generate_supercell(repeat=repeat)
            name  = '_'.join( [ str(r) for r in repeat ] )
            container.file_location += f'/{name}'
        PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)

    elif edit.lower() == 'compress':
        #
        if compress_min is None and compress_max is None:
            raise ValueError("For the 'compress' edit, the 'compress_factor' parameter must be provided.") 

        PT.generate_variants(parameter='compress', values={'N': N, 'compress_min': compress_min, 'compress_max': compress_max} )
        PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)

    elif edit.lower() == 'widening':
        #
        PT.containers = PT.handleWidening(values=[{'direction': direction, 'N':N, 'init_index': init_index, 'mid_index': mid_index, 'end_index': end_index}])
        PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)

    elif edit.lower() == 'interpolation':
        ''' 
        '''
        value = {'images':N, 'degree':degree, 'first_neighbor':first_neighbor}
        PT.containers = PT.handleInterpolation(values=value)
        PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)

def generate_edit_configuration(path:str, source:str=None, forces_tag:str=None, energy_tag:str=None, subfolders:bool=False, output_path:str=None, output_source:str=None, verbose:bool=False, edit:str=None,
                            atom_index:list=None, atom_ID:list=None, new_atom_ID:list=None, weights:list=None, N:int=None, search:str=None, seed:int=None):
    """
    Edits the configuration of atomic structures by changing atomic IDs and exports the modified structures.

    This function changes the IDs of atoms in the provided structures based on the specified edit operations and 
    then exports these modified structures to the defined output path.

    Parameters:
        path (str): Path to the input files.
        source (str, optional): Source type of the input files.
        subfolders (bool, optional): Flag to include subfolders in file reading.
        output_path (str, optional): Path for exporting the edited files.
        output_source (str, optional): Source type for exporting files.
        verbose (bool, optional): Enables verbose output.
        edit (str, optional): Type of editing operation ('ATOM_ID').
        atom_ID (list, optional): Original atom ID to be changed.
        new_atom_ID (list, optional): New atom ID to replace the original.
        weights (list, optional): New atom wrights probabilities to replace the original.
    Raises:
        ValueError: If required parameters for specific edits are not provided.
    """

    # Initialize the DFTPartition object
    PT = Partition(path)

    # Read files based on provided parameters
    PT.read_files( file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)

    values = {
        'search': search,
        'atom_index': atom_index,
        'atom_ID': atom_ID,
        'new_atom_ID': new_atom_ID,
        'N': N,
        'weights':weights,
        'seed':seed,
        'verbose':verbose
                }

    PT.handleAtomIDChange( values={f'{edit}':values} )

    # Export the edited files
    PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)

def generate_filter(path:str, source:str=None, forces_tag:str=None, energy_tag:str=None, subfolders:bool=False, output_path:str=None, output_source:str=None, verbose:bool=False, 
                    keep:str=None, container_property:str=None, value:float=None, T:float=None, ID:str=None, N:int=None, 
                    ):
    """
    Filters atomic structures based on specified criteria and exports the filtered structures.

    This function applies filtering operations to atomic structures based on various properties like class,
    type, value, etc., and then exports these filtered structures to the defined output path.

    Parameters:


    Raises:
        ValueError: If required parameters for specific filters are not provided.
    """
    # Initialize the DFTPartition object
    PT = Partition(path)

    # Read files and apply filters
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)

    PT.filter_conteiners(filter_function=keep, container_property=container_property,  
                        value=value, temperature=T, selection_number=N, ID=ID, verbose=verbose)

    # Export the filtered files
    PT.export_files(file_location=output_path, source=source, label='enumerate', verbose=verbose)

def generate_dataset(path:str, source:str=None, forces_tag:str=None, energy_tag:str=None, subfolders:bool=False, output_path:str=None, output_source:str=None, verbose:bool=False, index:int=None, 
                    operation:str=None, ):
    """
    """
    # Initialize the DFTPartition object
    PT = Partition(path)

    # Read files and apply filters
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)
    if operation.upper() == 'SORT':
        PT.handleDataset( values= {'sort':{'verbose':verbose} }  )

    # Export the filtered files
    PT.export_files(file_location=output_path, source=source, label='enumerate', verbose=verbose)

def generate_solvent(path:str, source:str=None, forces_tag:str=None, energy_tag:str=None, subfolders:bool=False, index:int=None, output_path:str=None, output_source:str=None, verbose:bool=False, 
                    density:float=None, solvent:list=None, slab:bool=None, 
                    shape:str=None, size:list=None, vacuum_tolerance:float=None, 
                    seed:float=None,
                    colition_tolerance:float=None, translation:list=None, wrap:bool=None):
    """
    Generates a solvent environment for molecular dynamics or quantum mechanics simulations.

    Parameters:
    - path (str): Path to the directory containing input files for the simulation.
    - source (str, optional): Source format of the input files (e.g., 'VASP', 'OUTCAR', etc.).
    - subfolders (bool, optional): If True, includes subfolders in the file search.
    - index (int, optional): Index of the container to apply the solvent generation.
    - output_path (str, optional): Path for exporting the modified files with the solvent environment.
    - output_source (str, optional): Format for exporting the modified files (e.g., 'VASP', 'xyz').
    - verbose (bool, optional): If True, provides detailed output during execution.

    Solvent-related parameters:
    - density (float, optional): Density of the solvent, important for accurately modeling liquid environments.
    - solvent (list, optional): List of solvents to use (e.g., ['H2O', 'H2'] for water and hydrogen).
    - slab (bool, optional): Indicates whether the simulation involves a slab geometry, typically used in surface studies.
    - shape (str, optional): Shape of the simulation region ('box' or 'sphere').
    - size (list, optional): Dimensions of the simulation box (length, width, height), applicable if shape is 'box'.
    - vacuum_tolerance (float, optional): Tolerance for vacuum spaces in the simulation, usually in Angstroms.
    - colition_tolerance (float, optional): Collision tolerance, defining the minimum distance between atoms or molecules.
    - translation (list, optional): Translation vector for positioning the system within the simulation box.
    - wrap (bool, optional): If True, enables wrapping of atoms within the simulation boundaries, useful for periodic boundary conditions.

    This function initializes a DFTPartition object, reads files, applies solvent-related configurations,
    generates variants based on these configurations, and exports the results.
    """
    # Initialize the DFTPartition object
    PT = Partition()

    # Read files and apply configurations
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)
    
    values = {
        'density': density,
        'solvent': solvent,
        'slab': slab,
        'shape': shape,
        'size': size,
        'vacuum_tolerance': vacuum_tolerance,
        'colition_tolerance': colition_tolerance,
        'translation': translation,
        'wrap': wrap,
        'seed':seed,
        'verbose':verbose
    }
    PT.handleCLUSTER( values= {'ADD_SOLVENT':values}  )

    # Export the modified files
    PT.export_files(file_location=output_path, source=output_source, label='enumerate', verbose=verbose)

def generate_conductivity(path:str, source:str=None, subfolders:bool=False, forces_tag:str=None, energy_tag:str=None, output_path:str=None, 
                T:float=None, ions:list=None, charge:list=None,
                verbose:bool=False, index:int=None):

    # Initialize the DFTPartition object
    PT = Partition()

    # Read files and apply configurations
    PT.read_files(file_location=path, source=source, energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose, container_index=index)
    
    values = { 
        'T': T,
        'ions': ions,
        'charge': charge,
    }

    PT.handle_conductivity_analysis( values={f'{plot}':values}  )

def add_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add common arguments to the given subparser.

    This function adds arguments for file paths, verbosity, and other common settings
    used across various sub-commands in the theoretical calculations tool.

    Args:
        parser (argparse.ArgumentParser): The parser to which arguments will be added.
    """
    structure_list = ['VASP', 'OUTCAR', 'xyz', 'traj', 'cif', 'AIMS', 'gen', 'POSCAR', 'ASE', 'PDB', 'DUMP', 'LAMMPS']
    
    parser.add_argument('--path', type=str, default='.', help='Path to the files directory')
    parser.add_argument('--source', type=str, choices=structure_list, 
                        help='Source of calculation files (e.g., VASP, molecular_dynamics, force_field)')
    parser.add_argument('--forces-tag', type=str, default='forces', help='Tag to identify forces data in files')
    parser.add_argument('--energy-tag', type=str, default='E', help='Tag to identify energy data in files')
    parser.add_argument('--output_path', type=str, default='.', 
                        help='Path for exporting processed files and results')
    parser.add_argument('--output_source', type=str, choices=structure_list,
                        help='Format for exporting processed files and results')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--subfolders', action='store_true', 
                        help='Include all subfolders under the specified path')
    parser.add_argument('--index', type=int, help='Index for specific file selection')



def parse_dynamic_groups(args: argparse.Namespace) -> Tuple[List[Optional[List[str]]], List[Optional[int]]]:
    """
    Parse dynamic group arguments from command line args.

    This function extracts group-related arguments (g1, g2, ..., gn1, gn2, ...) from the
    parsed command line arguments and organizes them into lists of atom groups and group numbers.

    Args:
        args (argparse.Namespace): Parsed command line arguments.

    Returns:
        Tuple[List[Optional[List[str]]], List[Optional[int]]]: A tuple containing two lists:
            1. List of atom groups (each group is a list of strings or None)
            2. List of group numbers (integers or None)
    """
    atom_groups = [None] * 10  # Assuming up to 10 groups
    group_numbers = [None] * 10

    for key, value in vars(args).items():
        if key.startswith('g') and not key.startswith('gn') and value is not None:
            index = int(key[1:]) - 1
            atom_groups[index] = value
        elif key.startswith('gn') and value is not None:
            index = int(key[2:]) - 1
            group_numbers[index] = value

    # Remove None values
    atom_groups = [group for group in atom_groups if group is not None]
    group_numbers = [num for num in group_numbers if num is not None]

    return atom_groups, group_numbers

def main():
    """
    Main function to handle command line arguments and execute respective functions.

    This function sets up the argument parser, defines subparsers for various commands,
    parses the command line arguments, and calls the appropriate function based on the
    specified command.
    """

    # Set up the main argument parser
    parser = argparse.ArgumentParser(description='Tool for theoretical calculations in quantum mechanics and molecular dynamics.')
    subparsers = parser.add_subparsers(dest='command', help='Available sub-commands')
    
    # =========== Sub-command TEST  ===========
    parser_export_position = subparsers.add_parser('test', help='')
    
    # =========== Sub-command EXPORT  ===========
    parser_export_position = subparsers.add_parser('export', help='Export atomic positions from a specified source format to a desired output format. This is useful for converting file formats for compatibility with various simulation and visualization tools.')
    add_arguments(parser_export_position)
    parser_export_position.add_argument('--bond_factor', type=float, default=1.1, required=False, help='')

    # ========== AbInitioThermodynamics ( 3 ) ===========
    parser_AbIT = subparsers.add_parser('thermodynamic', help='')
    add_arguments(parser_AbIT)

    parser_AbIT.add_argument('--plot', type=str, choices=['phase_diagram', 'ensemble_analysis', 'composition_analysis'], help='Type of plot to generate')
    parser_AbIT.add_argument('--reference', nargs='+', help='Reference values for analysis')
    parser_AbIT.add_argument('--k', type=int, default=6, help='Number of nearest neighbors')
    parser_AbIT.add_argument('--optimize', default=False, action='store_true', help='Optimize the analysis')

    parser_AbIT.add_argument('--r_cut', type=float, default=4.0, help='Cutoff radius for SOAP analysis')
    parser_AbIT.add_argument('--n_max', type=int, default=12, help='Maximum number of radial basis functions for SOAP')
    parser_AbIT.add_argument('--l_max', type=int, default=12, help='Maximum degree of spherical harmonics for SOAP')
    parser_AbIT.add_argument('--sigma', type=float, default=0.01, help='Width of Gaussian functions in SOAP')
    parser_AbIT.add_argument('--regularization', type=float, default=1e-5, help='Regularization parameter for linear analysis')
    parser_AbIT.add_argument('--components', type=int, default=10, help='Number of components for dimensionality reduction')
    parser_AbIT.add_argument('--compress_model', type=str, default='umap', help='Model used for dimensionality reduction')
    parser_AbIT.add_argument('--cluster_model', type=str, default='dbscan', help='Model used for clustering')
    parser_AbIT.add_argument('--eps', type=float, default=0.7, help='Epsilon parameter for DBSCAN clustering')
    parser_AbIT.add_argument('--min_samples', type=int, default=2, help='Minimum samples parameter for DBSCAN clustering')

    # ========== BLENDER ( 4 ) ===========
    parser_blender = subparsers.add_parser('blender', help='')
    add_arguments(parser_blender)
    parser_blender.add_argument('--plot', type=str, choices=['render'], default='xyz', required=False, help='')
    parser_blender.add_argument('--resolution', type=int, nargs=2, default=[1920, 1920], required=False, help='')
    parser_blender.add_argument('--samples', type=int, default=15, required=False, help='')
    parser_blender.add_argument('--fog', action='store_true', default=False, required=False, help='')
    parser_blender.add_argument('--render', action='store_true', default=False, required=False, help='')
    parser_blender.add_argument('--sigma', type=float, default=1.1, required=False, help='')
    parser_blender.add_argument('--scale', type=float, default=1.0, required=False, help='')
    parser_blender.add_argument('--camera', type=str, nargs='+', default=['x', 'y', 'z'], choices=['x', '-x', 'y', '-y', 'z', '-z'], required=False, help='')
    parser_blender.add_argument('--repeat', type=int, nargs=3, default=[0,0,0], required=False, help='')
   
    # =========== MD analisis ===========
    parser_MD = subparsers.add_parser('MD', help='')
    add_arguments(parser_MD)
    parser_MD.add_argument('--plot', type=str, required=True, choices=[
            'path_tracking', 'count_species', 'RBF', 'evaluate_ff', 'bond_distance_tracking', 'molecule_formation_tracking', 'forces', 'diffusion'], help='')
    parser_MD.add_argument('--specie', type=str, required=False, help='')
    parser_MD.add_argument('--sigma', type=float, required=False, default=1.2, help='bonda factor')
    parser_MD.add_argument('--reference', type=str, required=False, help='')
    parser_MD.add_argument('--topology', type=str, required=False, help='')
    parser_MD.add_argument('--ff-forces-tag', type=str, required=False, help='')
    parser_MD.add_argument('--ff-energy-tag', type=str, required=False, help='')
    parser_MD.add_argument('--wrap', default=False, action='store_true', help='.')
    parser_MD.add_argument('--save', default=False, action='store_true', help='.')
    parser_MD.add_argument('--tranparency', default=False, action='store_true', help='.')
    parser_MD.add_argument('--bins', type=int, default=100, required=False, help='')

    parser_MD.add_argument('--T', type=float, default=298, required=False, help='')
    parser_MD.add_argument('--q', type=float, nargs='+', required=False, help='')
    parser_MD.add_argument('--ID', type=str, nargs='+', required=False, help='')
    parser_MD.add_argument('--dt', type=float, default=1, required=False, help='time step in fs')
   
    # =========== Sub-command to generate vacancy directory ===========
    parser_defects = subparsers.add_parser('defect', help='Generate configurations for defects in materials.')
    add_arguments(parser_defects)
    parser_defects.add_argument('--defect', choices=['substitution'], type=str, help='')
    parser_defects.add_argument('--species', nargs='+', help=' .')
    parser_defects.add_argument('--new_species', nargs='+', help=' .')
    parser_defects.add_argument('--distribution', type=str, choices=['uniform', 'distance', 'distance-1', 'random'], help=' .')
    parser_defects.add_argument('--fill', default=False, action='store_true', help=' .')
    parser_defects.add_argument('--repetitions', default=1, type=int, help=' .')
    parser_defects.add_argument('--iterations', default=1, type=int, help=' .')
    parser_defects.add_argument('--Nw', type=int, help=' .')

    for i in range(1, 10):  # Assuming up to 10 groups
        parser_defects.add_argument(f'--g{i}', nargs='+', help=f'List of atom indices for group {i}')

    for i in range(1, 10):  # Assuming up to 10 groups
        parser_defects.add_argument(f'--gn{i}', type=int, help=f'Number of atoms in group {i}')

    # =========== Sub-command to generate configurations for disassembling the surface ===========
    parser_disassemble = subparsers.add_parser('disassemble', help='Generate configurations for disassembling surfaces or layers in a material.')
    add_arguments(parser_disassemble)
    parser_disassemble.add_argument('--steps', type=int, default=5, help='Number of steps in the disassembly process (default: 5)')
    parser_disassemble.add_argument('--final_distance', type=float, default=5.0, help='Final distance between layers or atoms after disassembly (default: 5.0)')
    parser_disassemble.add_argument('--atoms_to_remove', type=int, help='Number of atoms to remove during disassembly.')

    # =========== Sub-command: dimer ===========
    parser_dimer = subparsers.add_parser('dimer', help='Search for optimal dimer configurations in a material.')
    add_arguments(parser_dimer)
    parser_dimer.add_argument('--labels', nargs='+', help='List of atom labels to include in the dimer search. This option allows the specification of which types of atoms are to be considered for forming dimers.')
    parser_dimer.add_argument('--steps', type=int, default=10, help='Number of iterative steps in the dimer search. This parameter determines the resolution of the search process, with a higher number of steps providing finer detail in exploring dimer configurations (default: 10).')
    parser_dimer.add_argument('--vacuum', type=float, default=6.0, help='Specifies the vacuum distance (in Ångströms) around the dimer structure. This distance is used to define the amount of empty space surrounding the dimer in simulations, important for accurate electronic structure calculations (default: 6.0 Å).')
    parser_dimer.add_argument('--d0', type=float, default=None, help='Initial distance between the two atoms in a dimer (in Ångströms). If not specified, a default value based on atomic properties will be used. This parameter sets the starting point for the search process.')
    parser_dimer.add_argument('--df', type=float, default=None, help='Final distance between the two atoms in a dimer (in Ångströms). This value defines the end point of the distance range to be explored during the dimer search. If not specified, a reasonable default based on the atomic properties will be used.')

    # =========== Sub-comando para generar script ===========
    parser_config = subparsers.add_parser('config', help='Read Position data from "path", read Configurtion data from "config_path" and export to "output_path".')
    add_arguments(parser_config)
    parser_config.add_argument('--config_path', type=str, required=True, help='')
    parser_config.add_argument('--config_source', type=str, required=True, help='')

    # =========== Sub-comando para generar BAND files ===========
    parser_bands = subparsers.add_parser('bands', help='Configure parameters for generating band calculation files from VASP data.')
    add_arguments(parser_bands)
    parser_bands.add_argument('--points', type=int, help='Specifies the number of k-points in each segment of the band path. It should be an integer value representing the total number of k-points along the path.')
    parser_bands.add_argument('--special_points', type=str, required=True, default='GMMLLXXG', help='Defines special points in the Brillouin zone for band calculations. Should be a character string representing points, for example, "GMXLG", indicating the high-symmetry points along the band path.')

    # =========== Sub-command for ganerate .JSON files from EIGENVAL ===========
    parser_bands2json = subparsers.add_parser('bands2json', help='Configure parameters for generating band calculation files from VASP data.')
    add_arguments(parser_bands2json)
    parser_bands2json.add_argument('--fermi', type=float, help='Specifies the energy of the fermi level.')

    # =========== Sub-command for PLOT files from SOURCE format to OUTPUT format ===========
    parser_plot = subparsers.add_parser('plot', help='Generates plots based on data from a specified source. This can include plotting energy bands, density of states, or molecular structures, depending on the input data and specified plot type.')
    add_arguments(parser_plot)
    parser_plot.add_argument('--plot', type=str, required=True, choices=['bands', 'RBF'], help='Specifies the type of plot to generate. "bands" for band structure plots and "RBF" for radial basis function (RBF) plots.')
    parser_plot.add_argument('--fermi', type=float, help='Specifies the Fermi energy level (in eV). This is crucial for accurate band structure plots as it sets the reference energy level around which the band structure is visualized.')
    parser_plot.add_argument('--emin', type=float, help='Specifies the minimum energy (in eV) for the plot range. Used to limit the plot to a specific energy range, enhancing focus on regions of interest.')
    parser_plot.add_argument('--emax', type=float, help='Specifies the maximum energy (in eV) for the plot range. Similar to --emin, it allows focusing on a specific energy interval in the plot.')
    parser_plot.add_argument('--cutoff', type=float, default=6.0, help='Defines the cutoff distance (in Ångströms) for RBF plots. This parameter is crucial for determining the extent of spatial interactions to be considered in the plot.')
    parser_plot.add_argument('--number_of_bins', type=int, default=100, help='Sets the number of bins for the histogram in RBF plots. A higher number of bins can lead to finer details in the plot, but may also increase computational load.')


    
    # ========== Sub-command: edit_positions ===========
    parser_edit = subparsers.add_parser('edit_positions', help='Modify atomic positions in the input files, allowing operations like "rattling" to introduce small random displacements.')
    add_arguments(parser_edit)
    parser_edit.add_argument('--edit', type=str, choices=['rattle', 'compress', 'supercell', 'widening', 'interpolation'], default='rattle', help='Type of modification to apply to atomic positions. E.g., "rattle" for random displacements.')
    parser_edit.add_argument('--std', type=float, required=False, help='Standard deviation for displacement distribution in "rattle" operation, defining displacement magnitude.')
    parser_edit.add_argument('--N', type=int, required=False, help='Number of applications of the selected operation. Defaults to 1 if not specified.')
    parser_edit.add_argument('--repeat', type=int, nargs=3, default=[1, 1, 1], help='Repeat the unit cell in x, y, z dimensions respectively. Format: x y z')
    parser_edit.add_argument('--direction', type=str, choices=['x', 'y', 'z'], required=False, default='z', help='')
    parser_edit.add_argument('--compress_min', type=float, nargs=3, default=[1, 1, 1], help='Minimum compression factors in x, y, z for the "compress" operation. Format: x y z')
    parser_edit.add_argument('--compress_max', type=float, nargs=3, default=[1, 1, 1], help='Maximum compression factors in x, y, z for the "compress" operation. Format: x y z')
    parser_edit.add_argument('--init_index', type=int, required=False, help='')
    parser_edit.add_argument('--mid_index', type=int, required=False, help='')
    parser_edit.add_argument('--end_index', type=int, required=False, help='')
    parser_edit.add_argument('--degree', type=int, required=False, default=1, help='')
    parser_edit.add_argument('--first_neighbor', required=False, default=False, action='store_true', help='')

    # ========== Sub-command: edit_configuration ===========
    parser_edit_config = subparsers.add_parser('edit_configuration', help='Modify the configuration settings of your simulation or calculation process.')
    add_arguments(parser_edit_config)
    parser_edit_config.add_argument('--edit', type=str, choices=['atom_id', 'atom_index'], help='Specify the type of configuration modification.')
    parser_edit_config.add_argument('--search', type=str, choices=['full', 'random', 'exact'], required=False, help='')
    parser_edit_config.add_argument('--atom_index', type=int, nargs='+', required=False, help='')
    parser_edit_config.add_argument('--ID', type=str, nargs='+', required=False, help='Identifier for the configuration element to modify.')
    parser_edit_config.add_argument('--new_ID', type=str, nargs='+', required=False, help='New identifier to assign to the configuration element.')
    parser_edit_config.add_argument('--weights', type=float, nargs='+', required=False, help='')
    parser_edit_config.add_argument('--N', default=1, type=int, required=False, help='.')
    parser_edit_config.add_argument('--seed', default=1, type=int, required=False, help='.')

    # ========== Sub-command: filter ===========
    parser_filter = subparsers.add_parser('filter', help='Apply filters to select specific data based on various criteria.')
    add_arguments(parser_filter)
    parser_filter.add_argument('--keep', choices=['over', 'below', 'close', 'far'], type=str, help='Type of filter to apply: random, flat_histogram, or binary.')
    parser_filter.add_argument('--property', choices=['E', 'E/N', 'forces', 'ID'], type=str, help='Property to use for filtering: Energy (E), forces, or atom IDs.')
    parser_filter.add_argument('--value', type=float, required=False, help='Value to compare against for the filter.')
    parser_filter.add_argument('--T', type=float, required=False, help='.')
    parser_filter.add_argument('--ID', default=False, action='store_true', help='Enable trajectory-based filtering.')
    parser_filter.add_argument('--N', default=1, type=float, help='Number of elements to select when filtering.')

    # ========== Sub-command: dataset ===========
    parser_dataset = subparsers.add_parser('dataset', help='Apply filters to select specific data based on various criteria.')
    add_arguments(parser_dataset)
    parser_dataset.add_argument('--operation', choices=['sort'], type=str, help='')

    # ========== ADD - solvent ===========
    parser_solvent = subparsers.add_parser('solvent', help='Configure solvent environment for molecular dynamics or quantum mechanics simulations. This includes setting solvent type, density, and the geometry of the simulation environment.')
    add_arguments(parser_solvent)
    parser_solvent.add_argument('--density', type=float, default='.', help='Specify the density of the solvent in the simulation. The unit of density should align with the simulation system.')
    parser_solvent.add_argument('--solvent', type=str, nargs='+', choices=['H2O', 'H2'], default='H2O', help='Select the type of solvent to be used. Options include "H2O" for water and "H2" for hydrogen. Multiple solvents can be specified.')
    parser_solvent.add_argument('--slab', default=False, action='store_true', help='Enable this flag to indicate a slab geometry in the simulation, typically used in surface studies.')
    parser_solvent.add_argument('--shape', type=str, choices=['box', 'sphere', 'cell', 'parallelepiped'], default='cell', help='Define the shape of the simulation box. Options are "box" for a rectangular prism and "sphere" for spherical geometry.')
    parser_solvent.add_argument('--size', type=float, nargs=3, default=[10, 10, 10], help='Set the dimensions of the simulation box, specified as length, width, and height. Applicable when the shape is "box".')
    parser_solvent.add_argument('--vacuum_tolerance', type=float, default=0.0, help='Set the vacuum tolerance for the simulation, defining the minimum allowed spacing between atoms or molecules.')
    parser_solvent.add_argument('--colition_tolerance', type=float, default=1.6, help='Specify the collision tolerance, which is the minimum distance allowed between atoms or molecules to avoid overlaps.')
    parser_solvent.add_argument('--seed', type=float, default=0, help='')
    parser_solvent.add_argument('--translation', type=float, nargs=3, default=[0, 0, 0], help='Provide a translation vector to adjust the position of the system within the simulation box. Format: x-offset y-offset z-offset.')
    parser_solvent.add_argument('--wrap', default=True, action='store_true', help='Enable or disable wrapping of atoms or molecules within the simulation box boundaries. Useful for periodic boundary conditions.')

    # ========== EXTRACT ===========
    parser_extract = subparsers.add_parser('extract', help='')
    add_arguments(parser_extract)
    #parser_extract.add_argument('--plot', type=str, choices=['correlation'], default='xyz', required=False, help='')
    #parser_extract.add_argument('--resolution', type=int, nargs=2, default=[1920, 1920], required=False, help='')
    parser_extract.add_argument(f'--g', nargs='+', help=f'List of atom indices for group')
    parser_extract.add_argument(f'--f', type=str, choices=['h5'], help=f'')
    parser_extract.add_argument('--last', default=False, action='store_true', help='')    

    args = parser.parse_args()

    # Handle execution based on the specified sub-command
    if args.command == 'export':
        generate_export_files(  path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                                index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                                bond_factor=args.bond_factor
                                )

    elif args.command == 'test':
        generate_test()

    elif args.command == 'thermodynamic':
        generate_AbInitioThermodynamics(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                                        index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                                        plot=args.plot, k=args.k, optimize=args.optimize, reference=args.reference,
                                        r_cut=args.r_cut, n_max=args.n_max, l_max=args.l_max, sigma=args.sigma,
                                        regularization=args.regularization,
                                        components=args.components, compress_model=args.compress_model,
                                        cluster_model=args.cluster_model, eps=args.eps, min_samples=args.min_samples)

    elif args.command == 'blender':
        generate_BLENDER(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                        index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                        plot=args.plot, resolution=args.resolution, samples=args.samples, fog=args.fog, render=args.render,
                        scale=args.scale, camera=args.camera, repeat=args.repeat, 
                        sigma=args.sigma, )

    elif args.command == 'plot':
        generate_plot(  path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                        index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                        plot=args.plot, fermi=args.fermi, emin=args.emin, emax=args.emax, cutoff=args.cutoff, number_of_bins=args.number_of_bins
                        )

    elif args.command == 'MD':
        generate_MD(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                    index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                    plot=args.plot,  sigma=args.sigma, topology=args.topology, wrap=args.wrap,
                    T=args.T,       q=args.q,          chemical_ID=args.ID,          dt=args.dt,
                    reference=args.reference, ff_energy_tag=args.ff_energy_tag, ff_forces_tag=args.ff_forces_tag, 
                    tranparency=args.tranparency, save=args.save
                    )

    if args.command == 'defect':
        atom_groups, group_numbers = parse_dynamic_groups(args)
        generate_defects(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                         index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
            defect=args.defect, species=args.species, new_species=args.new_species, 
            Nw=args.Nw,
            atom_groups=atom_groups, group_numbers=group_numbers, fill=args.fill, repetitions=args.repetitions, iterations=args.iterations, distribution=args.distribution)
 
    elif args.command == 'disassemble':
        generate_disassemble_surface(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                                     index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                                     steps=args.steps, final_distance=args.final_distance, atoms_to_remove=args.atoms_to_remove
                                     )
    
    elif args.command == 'dimer':
        generate_dimers(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                        index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                        labels=args.labels, steps=args.steps, initial_distance=args.d0, final_distance=args.df, vacuum_tolerance=args.vacuum,
                        )
        
    elif args.command == 'config':
        generate_config(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                        index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                        config_path=args.config_path, config_source=args.config_source,
                        )
    
    elif args.command == 'bands':
        generate_band_calculation(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                                index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source,  
                                points=args.points, special_points=args.special_points, 
                                )
    
    elif args.command == 'bands2json':
        generate_json_from_bands(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                                 index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                                 fermi=args.fermi,
                                )

    elif args.command == 'edit_positions':
        generate_edit_positions(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                                index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                                edit=args.edit, std=args.std, N=args.N, direction=args.direction, repeat=args.repeat, compress_min=args.compress_min, compress_max=args.compress_max,
                                init_index=args.init_index, mid_index=args.mid_index, end_index=args.end_index, degree=args.degree, first_neighbor=args.first_neighbor
                                )

    elif args.command == 'edit_configuration':
        generate_edit_configuration(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                                    index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                                    edit=args.edit, search=args.search, atom_index=args.atom_index, atom_ID=args.ID, new_atom_ID=args.new_ID, weights=args.weights, N=args.N, seed=args.seed
                                    )

    elif args.command == 'filter':
        generate_filter(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                        index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                        keep=args.keep, container_property=args.property, value=args.value, T=args.T, ID=args.ID, N=args.N)

    elif args.command == 'dataset':
        generate_dataset(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                         index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
                         operation=args.operation, )

    elif args.command == 'solvent':
        generate_solvent(path=args.path,     source=args.source,     forces_tag=args.forces_tag,     energy_tag=args.energy_tag,      subfolders=args.subfolders, 
                         index=args.index,   verbose=args.verbose,   output_path=args.output_path,   output_source=args.output_source, 
    
                        density=args.density, solvent=args.solvent, slab=args.slab, 
                        shape=args.shape, size=args.size, vacuum_tolerance=args.vacuum_tolerance, 
                        colition_tolerance=args.colition_tolerance, translation=args.translation, wrap=args.wrap, 
                        seed=args.seed, 
                        )




if __name__ == '__main__':
    main()