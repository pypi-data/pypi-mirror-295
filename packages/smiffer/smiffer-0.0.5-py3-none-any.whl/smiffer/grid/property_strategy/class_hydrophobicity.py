"""Contains a class with strategy to fill a grid with hydrophobic properties."""

# pylint: disable=duplicate-code
# THERE IS NO DUPLICATE CODE, THESE ARE IMPORT PYLINT!!!

__authors__ = ["Diego BARQUERO MORERA", "Lucas ROUAUD"]
__contact__ = [
    "diego.barqueromorera@studenti.unitn.it",
    "lucas.rouaud@gmail.com",
]
__copyright__ = "MIT License"

# [N]
import numpy as np

# [C]
from .class_property import StrategyProperty

# [G]
from ..class_stamp import Stamp

# [K]
from ..kernel import GaussianKernel

# pylint: enable=duplicate-code


class StrategyHydrophobic(StrategyProperty):
    """A class for defining strategies to fill a grid with hydrophobic
    properties.

    Inheritance
    -----------
    This class is the child of `StrategyProperty`. Check this one for other
    **attributes** and **methods** definitions.
    """

    def populate_grid(self, grid: np.ndarray, grid_object) -> None:
        """Populate a grid following H-bond properties.

        Parameters
        ----------
        grid : `np.ndarray`
            The grid to fill.

        grid_object : `Grid`
            The grid object to access all attributes.
        """
        radius: float = (
            grid_object.yaml["function_hydrophobic_mu"]
            + grid_object.yaml["function_hydrophobic_sigma"]
            * grid_object.yaml["other_gaussian_kernel_scalar"]
        )

        hydrophobicity_kernel: GaussianKernel = GaussianKernel(
            radius=radius,
            delta=grid_object.delta,
            v_mu=grid_object.yaml["function_hydrophobic_mu"],
            v_sigma=grid_object.yaml["function_hydrophobic_sigma"],
        )

        stamp: Stamp = Stamp(
            grid=grid,
            grid_origin=grid_object.coord[0],
            delta=grid_object.delta,
            kernel=hydrophobicity_kernel,
        )

        for atom in grid_object.molecule:
            stamp.stamp_kernel(
                center=atom.position,
                factor=self._atom_constant["kd_scale"][atom.resname],
            )
