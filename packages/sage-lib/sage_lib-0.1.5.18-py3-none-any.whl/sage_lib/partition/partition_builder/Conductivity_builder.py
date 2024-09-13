try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del syss

try:
    from sage_lib.IO.structure_handling_tools.AtomPosition import AtomPosition
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing AtomPosition: {str(e)}\n")
    del sys
    
try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    from scipy.optimize import leastsq
    from scipy.constants import Boltzmann, Avogadro, hbar, pi
    import pickle
    from typing import Dict, List, Tuple, Union
    import pickle

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.colors import LogNorm
    from scipy.stats import linregress
    from scipy.stats import gaussian_kde

except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing scipy.optimize.leastsq : {str(e)}\n")
    del sys

class Conductivity_builder(PartitionManager):

    @staticmethod
    def plot_violin(ax, data, positions, widths):
        """
        Create violin plots on a specified axis.
        
        Args:
        ax (matplotlib.axes.Axes): The axis to plot on.
        data (list of arrays): List of data arrays for each violin.
        positions (array): Array of positions for the violins.
        widths (float or array): Width of the violins.
        """
        for d, p in zip(data, positions):
            kde = gaussian_kde(d)
            x = np.linspace(min(d), max(d), 100)
            v = kde.evaluate(x)
            v = v / v.max() * widths  # Normalize the width
            ax.fill_betweenx(x, p - v, p + v, alpha=0.7)

    def get_msd_data(self, chemical_ID:list=None):

        V = self.containers[0].AtomPositionManager.get_volume()
        atoms_labels = self.containers[0].AtomPositionManager.get_atomic_labels()
        atoms_positions = np.zeros( (len(self.containers), self.containers[0].AtomPositionManager.atomPositions.shape[0], 3) )

        for c_i, c in enumerate(self.containers):
            atoms_positions[c_i,:,:] = c.AtomPositionManager.atomPositions

        # n_particles, n_time, n_dim ----> n_time, n_particles, n_dim
        atoms_positions = np.transpose(atoms_positions, (1, 0, 2))

        return atoms_positions, atoms_labels, V, 

    def plot_msd(self, conductivity_data, time_step, max_ions_to_plot=100):
        """
        Plots an enhanced version of the mean squared displacement (MSD) for each ion type in the conductivity_data.
        
        Args:
        conductivity_data (dict): Dictionary containing MSD data for ions.
        time_step (float): Time step between data points.
        max_ions_to_plot (int): Maximum number of individual ion trajectories to plot.
        
        Keys in conductivity_data:
            'msd' (dict): Dictionary with keys as ion IDs and values as arrays of MSD data.
        """
        def plot_violin(ax, data, positions, widths):
            """
            Create violin plots on a specified axis.
            
            Args:
            ax (matplotlib.axes.Axes): The axis to plot on.
            data (list of arrays): List of data arrays for each violin.
            positions (array): Array of positions for the violins.
            widths (float or array): Width of the violins.
            """
            for d, p in zip(data, positions):
                kde = gaussian_kde(d)
                x = np.linspace(min(d), max(d), 100)
                v = kde.evaluate(x)
                v = v / v.max() * widths  # Normalize the width
                ax.fill_betweenx(x, p - v, p + v, alpha=0.7)

        print("Available styles:", plt.style.available)
        
        plt.style.use('seaborn-whitegrid' if 'seaborn-whitegrid' in plt.style.available else 'default')

        plt.rcParams.update({
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'axes.edgecolor': 'gray',
            'axes.grid': True,
            'grid.alpha': 0.3,
            'grid.color': 'gray',
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10
        })
        
        for cID, msd_data in conductivity_data['msd'].items():
            fig = plt.figure(figsize=(20, 10))
            gs = GridSpec(1, 2, width_ratios=[2, 1])
            
            ax1 = fig.add_subplot(gs[0, 0])
            ax2 = fig.add_subplot(gs[0, 1])
            
            fig.suptitle(f'MSD Analysis for Ion Type {cID}', fontsize=16)

            time = np.arange(msd_data.shape[1]) * time_step

            colors = plt.cm.viridis(np.linspace(0, 1, max_ions_to_plot))
            for ion_index in range(min(msd_data.shape[0], max_ions_to_plot)):
                ax1.plot(time, msd_data[ion_index], alpha=0.7, linewidth=1, color=colors[ion_index])
            
            ax1.set_xlabel('Time', fontsize=12)
            ax1.set_ylabel('MSD', fontsize=12)
            ax1.set_title(f'Individual Ion Trajectories (showing {min(msd_data.shape[0], max_ions_to_plot)} out of {msd_data.shape[0]} ions)', fontsize=14)
            ax1.grid(True, which="both", ls="-", alpha=0.2)

            num_violins = 15
            times_to_plot = np.linspace(0, msd_data.shape[1] - 1, num_violins, dtype=int)
            data_to_plot = [msd_data[:, time_idx] for time_idx in times_to_plot]
            positions = [time_idx * time_step for time_idx in times_to_plot]
            plot_violin(ax2, data_to_plot, positions, widths=6.1)
            
            ax2.set_xlabel('Time', fontsize=12)
            ax2.set_ylabel('MSD', fontsize=12)
            ax2.set_title('Violin Plot of MSD at Different Times', fontsize=14)
            
            avg_msd = np.mean(msd_data, axis=0)
            ax1.plot(time, avg_msd, color='red', linewidth=2, label='Average MSD')

            D, best_interval, best_slope, best_intercept, best_r_squared = self.calculate_diffusion_coefficient(np.mean(msd_data, axis=0), time_step)

            # Plot the best fit line on the interval of linearity
            fit_time = time[best_interval[0]:best_interval[1]]
            fit_line = best_slope * fit_time + best_intercept
            ax1.plot(fit_time, fit_line, 'k--', label=f'Best Fit: R^2 = {best_r_squared:.2f}')
            ax1.axvspan(fit_time[0], fit_time[-1], color='gray', alpha=0.2, label='Linear Fit Interval')

            ax1.legend(fontsize=10)

            max_msd = np.max(msd_data)
            min_msd = np.min(msd_data)
            final_avg_msd = avg_msd[-1]
            
            stats_text = f'Max MSD: {max_msd:.2e}\nMin MSD: {min_msd:.2e}\nFinal Avg MSD: {final_avg_msd:.2e}\nDiffusion Coefficient: {D:.2e}'
            ax1.text(0.05, 0.95, stats_text, transform=ax1.transAxes, fontsize=10,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.show()

    def calculate_diffusion_coefficient(self, msd, time_step, dimensionality=3, weight_data: bool=True, verbose: bool=False):
        """
        Calculate the diffusion coefficient from the MSD data.
        
        Parameters:
        msd (np.ndarray): Mean Squared Displacement data.
        time_step (float): Time step between MSD data points.
        dimensionality (int): Dimensionality of the system (default is 3).
        weight_data (bool): If True, add weight to the number of data points included in the linear fit.
        verbose (bool): If True, print detailed information about the best fit.
        
        Returns:
        float: Estimated diffusion coefficient.
        """
        time = np.arange(len(msd)) * time_step
        best_slope = 0
        best_r_squared = 0
        best_interval = (0, len(msd))
        best_intercept = 0

        for start in range(len(msd) // 2):
            for end in range(start + len(msd) // 10, len(msd)):
                slope, intercept, r_value, _, _ = linregress(time[start:end], msd[start:end])
                r_squared = r_value ** 2
                
                # Apply weighting based on the number of data points
                if weight_data:
                    r_squared += (end - start) / len(msd) * 10**-20
                
                if r_squared > best_r_squared:
                    best_r_squared = r_squared
                    best_slope = slope
                    best_intercept = intercept
                    best_interval = (start, end)

        if verbose:
            print(f"Best interval for linear fit MSD = {best_slope:.2e} * t + {best_intercept:.2e}: {best_interval}")
            print(f"R-squared value: {best_r_squared:.2f}")
                
        diffusion_coefficient = best_slope / (2 * dimensionality)
        
        return diffusion_coefficient, best_interval, best_slope, best_intercept, best_r_squared

    @staticmethod
    def _calculate_ionic_conductivity(D, q, N, V, T):
        return np.sum(q*q * N * D)/ (V*np.Kb*T)

    def handle_conductivity_analysis(self, analysis_parameters:list ):
        """
        Handle molecular dynamics analysis based on specified analysis_parameters.

        Args:
            analysis_parameters (list): List of analysis types to perform.
        """
        conductivity_data = {}

        for v_key, v in analysis_parameters.items():

            if v_key.upper() == 'ANALYSIS':

                T = v['T']
                atoms_charge = v['q']
                chemical_ID = v['ID']
                dt = v['dt']

                conductivity_data['r'], conductivity_data['labels'], conductivity_data['V'] = self.get_msd_data(chemical_ID)
                
                conductivity_data['msd'], conductivity_data['t'], conductivity_data['D'] = {}, {}, {}
                conductivity_data['MSD'] = {}

                for cID in chemical_ID:
                    conductivity_data['t'][cID], conductivity_data['msd'][cID] = self.MSD(conductivity_data['r'][conductivity_data['labels']==cID], lag=True, fft=True)
                    conductivity_data['MSD'][cID] = np.mean(conductivity_data['msd'][cID], axis=0)
                    conductivity_data['D'][cID], best_interval, best_slope, best_intercept, best_r_squared = self.calculate_diffusion_coefficient(conductivity_data['MSD'][cID], dt, dimensionality=3)

                self.plot_msd(conductivity_data, time_step=dt)




'''
def generate_extract(path:str, source:str=None, subfolders:bool=False, forces_tag:str=None, energy_tag:str=None, output_path:str=None,
                g:str=None, f:list=None,  last:bool=None,
                verbose:bool=False, conteiner_index:int=None):


    import ast
    import numpy as np

    with open('data.txt', 'r') as file:
        content = file.read()
    data = ast.literal_eval(content)

    print(data)
    output_dict = {}
    for i, (key1,item1) in enumerate(data.items()):

        print(f'item {i}, label {key1}')
        path = item1['init']+'/OUTCAR'
        PT_init = Partition()
        PT_init.read_files(file_location=path, source='OUTCAR', energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose)
        PT_init.containers = [PT_init.containers[-1]]

        path = item1['end']+'/OUTCAR'
        PT_end = Partition()
        PT_end.read_files(file_location=path, source='OUTCAR', energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose)
        PT_end.containers = [PT_end.containers[-1]]

        path = item1['ts']+'/OUTCAR'
        PT_ts = Partition()
        PT_ts.read_files(file_location=path, source='OUTCAR', energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose)
        PT_ts.containers = [PT_ts.containers[-1]]

        path = item1['vib ']+'/OUTCAR'
        PT_vib = Partition()
        PT_vib.read_files(file_location=path, source='OUTCAR', energy_tag=energy_tag, forces_tag=forces_tag, subfolders=subfolders, verbose=verbose)
        PT_vib.containers = [PT_vib.containers[-1]]

        freq = PT_vib.containers[0].AtomPositionManager.dynamical_eigenvalues







       # Condición para labels
        condition_labels = (PT_ts.containers[0].AtomPositionManager.atomLabelsList == 'Fe') | (PT_ts.containers[0].AtomPositionManager.atomLabelsList == 'Ni')

        # Condición para la coordenada z
        condition_z = PT_ts.containers[0].AtomPositionManager.atomPositions[:, 2] > 25.5

        # Índices que cumplen ambas condiciones
        indices = np.where(condition_labels & condition_z)[0]

        values = {
                    'g'         :   ['H2O'],
                    'format'    :   f,
                    'last'      :   last,
                }

        indices = np.concatenate((indices, PT_end.generate_extract(values=values, verbose=verbose)))

        values = {
                    'g'         :   ['OOH'],
                    'format'    :   f,
                    'last'      :   last,
                }
        indices = np.concatenate((indices, PT_init.generate_extract(values=values, verbose=verbose)))

        indices = list(set(indices))
        output_dict[f'{i}'] = {
                'ts': {
                    'E':PT_ts.containers[0].AtomPositionManager.E,
                    'label':PT_ts.containers[0].AtomPositionManager.atomLabelsList[indices],
                    'charge':PT_ts.containers[0].AtomPositionManager.charge[indices][:,-1],
                    'magnetization':PT_ts.containers[0].AtomPositionManager.magnetization[indices][:,-1],
                    'dist': np.array([ [ PT_ts.containers[0].AtomPositionManager.distance( PT_ts.containers[0].AtomPositionManager.atomPositions[n1],
                                            PT_ts.containers[0].AtomPositionManager.atomPositions[n2])  for i2, n2 in enumerate(indices) ] for i1, n1 in enumerate(indices) ], dtype=np.float64 )
                        },
                'end': {
                    'E':PT_end.containers[0].AtomPositionManager.E,
                    'label':PT_end.containers[0].AtomPositionManager.atomLabelsList[indices],
                    'charge':PT_end.containers[0].AtomPositionManager.charge[indices][:,-1],
                    'magnetization':PT_end.containers[0].AtomPositionManager.magnetization[indices][:,-1],
                    'dist': np.array([ [ PT_end.containers[0].AtomPositionManager.distance( PT_end.containers[0].AtomPositionManager.atomPositions[n1],
                                    PT_end.containers[0].AtomPositionManager.atomPositions[n2])   for i2, n2 in enumerate(indices) ] for i1, n1 in enumerate(indices) ], dtype=np.float64 )
                        },
                'init': {
                    'E':PT_init.containers[0].AtomPositionManager.E,
                    'label':PT_init.containers[0].AtomPositionManager.atomLabelsList[indices],
                    'charge':PT_init.containers[0].AtomPositionManager.charge[indices][:,-1],
                    'magnetization':PT_init.containers[0].AtomPositionManager.magnetization[indices][:,-1],
                    'dist': np.array([ [ PT_init.containers[0].AtomPositionManager.distance( PT_init.containers[0].AtomPositionManager.atomPositions[n1],
                                    PT_init.containers[0].AtomPositionManager.atomPositions[n2])  for i2, n2 in enumerate(indices) ] for i1, n1 in enumerate(indices) ], dtype=np.float64 )
                        },
                'freq' : freq,
                'Ea1': PT_ts.containers[0].AtomPositionManager.E - PT_init.containers[0].AtomPositionManager.E ,
                'Ea2': PT_ts.containers[0].AtomPositionManager.E - PT_end.containers[0].AtomPositionManager.E  ,
                'Er' : PT_end.containers[0].AtomPositionManager.E - PT_init.containers[0].AtomPositionManager.E,
                    }

        print(indices)
        #print(output_dict)
        import pickle
        with open('data.pkl', 'wb') as f:
            pickle.dump(output_dict, f)

'''




















