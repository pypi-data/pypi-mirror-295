# class_hydrophobicity.py


Computation is based on next formula:

$$
\phi_{\text{hydr}} = - \displaystyle\sum_{r=1}^R K_r \displaystyle\sum_{a=1}^{A_r} \exp \left[ - \dfrac{\left( \mu_{\text{hydr}} - r_a \right)^2}{2 \sigma_{\text{hydr}}^2} \right]
$$

With \(\phi_{\text{hydr}}\) the field in a 3D space, \(R\) the total number of selected residues, \(K_r\) the residue hydrophobicity score (from Kyte Doolittle Scale), \(A_r\) the selected atoms from the residue \(r\), \(\mu_{\text{hydr}} (= 3.7~\text{Å})\) the mean (distance residue / receptor), \(r_a\) the atom position, \(\sigma_{\text{hydr}}^2 (= 2.0~\text{Å}^2)\) the variance (distance residue / receptor).

::: src.smiffer.grid.property_strategy.class_hydrophobicity
