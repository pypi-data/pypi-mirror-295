"""Contains a class with strategy to fill a grid with H-bond properties."""

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


class StrategyHBond(StrategyProperty):
    """A class for defining strategies to fill a grid with H-bond
    properties.

    Inheritance
    -----------
    This class is the child of `StrategyProperty`. Check this one for other
    **attributes** and **methods** definitions.

    Attributes
    ----------
    self.__key : `str`
        The key to switch between acceptor or donnor mode.
    """

    def __init__(self, name: str, atom_constant: object, key: str):
        """Define the strategy for H-bond properties computation.

        Parameters
        ----------
        name : `str`
            Name of the property.

        atom_constant : `AtomConstant`
            An object containing constant linked to atoms.

        key : `str`
            Which analyze to use between acceptor and donor. Respectively,
            gives the key "h_b_acceptor" or "h_b_donor" to this parameter to
            specify the wanted method.

        Raises
        ------
        ValueError
            Throw an error when the given key is not "h_b_acceptor" or
            "h_b_donor".
        """
        super().__init__(name, atom_constant)

        if key not in ["h_b_acceptor", "h_b_donor"]:
            raise ValueError(
                f'[Err##] Key "{key}" not accepted. List of '
                'accepted keys are "["h_b_acceptor", '
                '"h_b_donor"]".'
            )

        self.__key: str = key

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
            grid_object.yaml["function_h_bond_mu"]
            + grid_object.yaml["function_h_bond_sigma"]
            * grid_object.yaml["other_gaussian_kernel_scalar"]
        )

        h_bond_kernel: GaussianKernel = GaussianKernel(
            radius=radius,
            delta=grid_object.delta,
            v_mu=grid_object.yaml["function_h_bond_mu"],
            v_sigma=grid_object.yaml["function_h_bond_sigma"],
        )

        stamp: Stamp = Stamp(
            grid=grid,
            grid_origin=grid_object.coord[0],
            delta=grid_object.delta,
            kernel=h_bond_kernel,
        )

        for atom in grid_object.molecule:
            if atom.name not in self._atom_constant[self.__key][atom.resname]:
                continue

            stamp.stamp_kernel(center=atom.position)
