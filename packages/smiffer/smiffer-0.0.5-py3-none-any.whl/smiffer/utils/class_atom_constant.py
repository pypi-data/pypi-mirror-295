"""Contains a class in order to parse a `.yaml` parameter file."""

__authors__ = ["Diego BARQUERO MORERA", "Lucas ROUAUD"]
__contact__ = ["diegobarqueromorera@gmail.com", "lucas.rouaud@gmail.com"]
__copyright__ = "MIT License"


class AtomConstant:
    """Define atoms constants.

    Attributes
    ----------
    self.__AROMATIC : `dict`
        A dictionary mapping atom implied in cycle, for given residue.

    self.__KD_SCALE : `dict`
        A dictionary with the different residue KD values.

    self.__H_B_ACCEPTOR : `dict`
        A dictionary mapping atom implied in hydrogen bond acceptor, for given
        residue.

    self.__H_B_DONOR : `dict`
        A dictionary mapping atom implied in hydrogen bond donor, for given
        residue.

    self.__KEY : `list`
        A list of available keys.

    self.__VALUE : `list`
        A list containing all available dictionnaries.
    """

    # List of atoms implied in cycle, taking in consideration residues
    # and RNA bases.
    __AROMATIC: dict = {
        "HIS": "CD2 CE1 CG ND1 NE2",
        "PHE": "CD1 CD2 CE1 CE2 CG CZ",
        "TRP": "CD1 CD2 CE2 CE3 CG CH2 CZ2 CZ3 NE1",
        "TYR": "CD1 CD2 CE1 CE2 CG CZ",
        "U": "N1 C2 N3 C4 C5 C6",
        "C": "N1 C2 N3 C4 C5 C6",
        "A": "N1 C2 N3 C4 C5 C6 N7 C8 N9",
        "G": "N1 C2 N3 C4 C5 C6 N7 C8 N9",
    }

    # List of side chain hydrophobicity scores, from Kyte Doolittle Scale.
    # Warning: Unavailable for RNA bases.
    # Note:
    #   KD > 0: CYS ALA VAL ILE LEU MET PHE.
    #   KD < 0: ASP GLU SER THR ASN GLN PRO TYR TRP HIS LYS ARG GLY.
    __KD_SCALE: dict = {
        "ALA": 1.8,
        "ARG": -4.5,
        "ASN": -3.5,
        "ASP": -3.5,
        "CYS": 2.5,
        "GLN": -3.5,
        "GLU": -3.5,
        "GLY": -0.4,
        "HIS": -3.2,
        "ILE": 4.5,
        "LEU": 3.8,
        "LYS": -3.9,
        "MET": 1.9,
        "PHE": 2.8,
        "PRO": -1.6,
        "SER": -0.8,
        "THR": -0.7,
        "TRP": -0.9,
        "TYR": -1.3,
        "VAL": 4.2,
    }

    # List of atoms implied in hydrogen bond acceptor, taking in consideration
    # residues and RNA bases.
    __H_B_ACCEPTOR: dict = {
        "ASP": ("O", "OD1", "OD2"),
        "GLU": ("O", "OE1", "OE2"),
        "SER": ("O", "OG"),
        "THR": ("O", "OG1"),
        "ASN": ("O", "OD1", "ND2"),
        "GLN": ("O", "OE1", "NE2"),
        "CYS": ("O", "SG"),
        "PRO": ("O"),
        "GLY": ("O"),
        "ALA": ("O"),
        "VAL": ("O"),
        "ILE": ("O"),
        "LEU": ("O"),
        "MET": ("O"),
        "PHE": ("O"),
        "TYR": ("O", "OH"),
        "TRP": ("O", "NE1"),
        "HIS": ("O", "ND1", "NE2"),
        "LYS": ("O"),
        "ARG": ("O", "NE"),
        "U": ("OP1", "OP2", "O2'", "O3'", "O4'", "O5'", "O2", "N3", "O4"),
        "C": (
            "OP1",
            "OP2",
            "O2'",
            "O3'",
            "O4'",
            "O5'",
            "O2",
            "N3",
        ),
        "A": ("OP1", "OP2", "O2'", "O3'", "O4'", "O5'", "N3", "N7", "N1"),
        "G": ("OP1", "OP2", "O2'", "O3'", "O4'", "O5'", "N3", "N7", "O6"),
    }

    # List of atoms implied in hydrogen bond donor, taking in consideration
    # residues and RNA bases.
    __H_B_DONOR: dict = {
        "ASP": ("N"),
        "GLU": ("N"),
        "SER": ("N", "OG"),
        "THR": ("N", "OG1"),
        "ASN": ("N", "ND2", "ND2"),
        "GLN": ("N", "NE2", "NE2"),
        "CYS": ("N", "SG"),
        "PRO": (),
        "GLY": ("N"),
        "ALA": ("N"),
        "VAL": ("N"),
        "ILE": ("N"),
        "LEU": ("N"),
        "MET": ("N"),
        "PHE": ("N"),
        "TYR": ("N", "OH"),
        "TRP": ("N", "NE1"),
        "HIS": ("N", "ND1"),
        "LYS": ("N", "NZ", "NZ", "NZ"),
        "ARG": ("N", "NE", "NH1", "NH1", "NH2", "NH2"),
        "U": ("N3", "O2'"),
        "C": ("N4"),
        "A": ("N6"),
        "G": ("N1", "N2"),
    }

    __KEY: list = ["aromatic", "kd_scale", "h_b_acceptor", "h_b_donor"]
    __VALUE: list = [__AROMATIC, __KD_SCALE, __H_B_ACCEPTOR, __H_B_DONOR]

    def __setitem__(self, key: str, dictionary: dict):
        """Throws an exception if an setting is tried.

        Parameters
        ----------
        key : `str`
            The key to assign a parameter.

        dictionary : `dict`
            The dictionary to asign.

        Raises
        ------
        TypeError
            Throw when this method is called. Because it has to be not used.
        """
        raise TypeError(
            "[Err##] You cannot modify any attributes in this class!"
        )

    def __getitem__(self, key: str) -> dict:
        """Return a dictionary value corresponding to a given key.

        Parameters
        ----------
        key : `str`
            The key to fetch a dictionary.

        Returns
        -------
        `dict`
            The fetched dictionary.
        """
        if key not in self.__KEY:
            raise ValueError(
                f'[Err##] Key "{key}" not accepted. List of '
                f'accepted keys are "{self.__KEY}".'
            )

        return self.__VALUE[self.__KEY.index(key)]

    def keys(self) -> list:
        """Return keys linked to this object.

        Returns
        -------
        `list`
            The keys.
        """
        return self.__KEY

    def values(self) -> list:
        """Return dictionaries linked to this object.

        Returns
        -------
        `list`
            The values.
        """
        return self.__VALUE

    def items(self) -> zip:
        """Return keys, paired to their dictionaries, linked to this object.

        Returns
        -------
        `zip`
            The pairs key/value.
        """
        return zip(self.__KEY, self.__VALUE)

    def __str__(self) -> str:
        """Redefine the print() function for this object.

        Returns
        -------
        `str`
            The string representation of this object.
        """
        to_print: str = f"Available properties are: {self.__KEY}."

        return to_print


if __name__ == "__main__":
    atom_constant = AtomConstant()

    print(f"atom_constant[aromatic] return:\n {atom_constant['aromatic']}\n")
    print(atom_constant)
