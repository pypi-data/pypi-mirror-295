try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del sys

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

class Filter_builder(PartitionManager):
    """
    A class for building filters related to simulations or theoretical calculations.

    This class extends PartitionManager and provides methods to filter containers
    based on various criteria.

    Inherits:
    All attributes and methods from PartitionManager.
    """
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """
        Initialize the Filter_builder with file location and name.

        Parameters:
        - file_location (str): Location of the file.
        - name (str): Name of the configuration.
        - **kwargs: Additional keyword arguments for the parent class.
        """
        super().__init__(name=name, file_location=file_location)
        


    def filter_conteiners(self, filter_function:str, container_property:str=None, 
                value:float=None, temperature:str=None, selection_number:int=None, ID:str=None,
                traj:bool=False, verbose:bool=False) -> bool:
        """

        """
        # Generate a mask based on the specified filter criteria
        mask = self.get_mask(filter_function=filter_function, container_property=container_property, 
             value=value, temperature=temperature, selection_number=selection_number,
             traj=traj, verbose=verbose)

        # Apply the generated mask to filter containers
        if verbose: print( f'Filter :: {container_property} {filter_function} {value} with temperature {temperature} : shape target {selection_number} : {len(self.containers)} >> {np.sum(mask)}')
        self.apply_filter_mask(mask)

        return True 

    def get_mask(self, filter_function:str, container_property:str=None, 
                value:float=None, temperature:int=None, selection_number:int=None, ID:str=None,
                traj:bool=False, verbose:bool=False) -> list:
        """

        """
        # Initialize a default mask to avoid errors
        mask = np.ones_like(self.containers) # to avoid errors 

        weights = self.get_weights(filter_function, container_property, value, temperature, ID, verbose)

        selected_indices = np.random.choice(mask.shape[0], p=weights/np.sum(weights), size=int(selection_number), replace=False)

        # Create a selection mask with True for selected indices
        mask = [i in selected_indices for i in range(mask.shape[0])]

        return np.array(mask, dtype=np.int64)

    def get_weights(self, filter_function, container_property, value, temperature, ID=None, verbose:bool=False):
        """
        Calculate the weights for selection based on the filter function.

        Parameters:
        - filter_function (str): The function to apply for filtering ('over', 'below', 'close', 'far').
        - container_property (str): The property to use for filtering.
        - value (float): The reference value for the filter.
        - temperature (float): Temperature parameter used in the weighting functions.
        - ID (str, optional): Atom ID for specific property retrieval.

        Returns:
        - np.ndarray: An array of weights.
        """
        values = self.get_property(container_property, ID)

        temperature = 1 if np.abs(temperature) < -.01 else temperature

        if filter_function.lower() == 'over':
            # Apply sigmoidal function: 1 / (1 + exp(-(values - value) / temperature))
            weights = 1 / (1 + np.exp(-(values - value) / temperature))
        elif filter_function.lower() == 'below':
            # Apply negative sigmoidal function: 1 / (1 + exp((values - value) / temperature))
            weights = 1 / (1 + np.exp((values - value) / temperature))
        elif filter_function.lower() == 'close':
            # Apply Gaussian function: exp(-((values - value) ** 2) / (2 * temperature ** 2))
            weights = np.exp(-((values - value) ** 2) / (2 * temperature ** 2))
        elif filter_function.lower() == 'far':
            # Apply negative Gaussian function: 1 - exp(-((values - value) ** 2) / (2 * temperature ** 2))
            weights = 1 - np.exp(-((values - value) ** 2) / (2 * temperature ** 2))
        else:
            raise ValueError(f"Unknown filter_function: {filter_function}")

        if np.sum(weights) < 10**-5:
            if verbose: print(' >> FILTER : renormalizing weights (+10**-4)')
            weights += 10**-4

        return weights

    def get_property(self, container_property:str=None, ID:str=None):

        # Create the filter mask
        if container_property.upper() == 'FORCES':
            # Calculate the magnitude of the total force for each container
            values = [np.linalg.norm(c.AtomPositionManager.total_force) for c in self.containers]

        elif container_property.upper() == 'E':
            # Calculate the magnitude of the total force for each container
            values = [ c.AtomPositionManager.E for c in self.containers ]

        elif container_property.upper() == 'E/N':
            # Calculate the magnitude of the total force for each container
            values = [ c.AtomPositionManager.E/c.AtomPositionManager.atomCount for c in self.containers ]

        elif container_property.upper() == 'ID':
            # 
            values = [ c.AtomPositionManager.atom_ID_amount(ID) for c in self.containers ]

        return np.array(values)

