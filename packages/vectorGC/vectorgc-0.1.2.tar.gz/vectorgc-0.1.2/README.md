# Vector-GC - Modeling Dipolar Molecules with PCP-SAFT

[![repository](https://img.shields.io/pypi/v/vectorGC)](https://pypi.org/project/vectorGC)

`Vector-GC` is a group-contribution method for PCP-SAFT yielding parameters for non-polar and dipolar substances based on their molecular structure, e.g. given as SMILES. The method considers the dipolar term on a physical basis, thus improving predictions for dipolar substances and distinguishing cis- and trans-isomers. 

The method and the corresponding regression framework is published as pypi package and can be installed via pip as `vectorGC`. The regression framework utilizes rapid phase calculations and automatic differentiation through [FeOs-Torch](https://github.com/feos-org/feos-torch). The framework can be used to regress additional substance classes for the `Vector-GC` method or to develop novel group-contribution methods for PCP-SAFT (by implementing new sum rules).

## Using the `Vector-GC` Method

```python
from vectorGC import vectorGC

# get PCP-SAFT parameters from a SMILES
m, sigma, epsilon, mu = vectorGC.from_smiles("CCCCBr")
```

Currently, the `Vector-GC` method is parametrized for alkanes, alkenes, oxygenated substances, and halogenated substances. The parametrized groups and bonds are presented in our [publication](https://doi.org/10.1021/acsomega.4c04867). 

## Using the Regression Framework

```python
import pandas as pd
import vectorGC.regression_framework.models as models
from vectorGC.regression_framework.solver import scipy_solver

# Use scipy solver without printing progress
solver = scipy_solver(show_progress=False)

# Load data required for the model fit
with open("path_to_group_info.json", "r") as f:
        group_info = json.load(f)
chem_id = pd.read_json("path_to_chemid.json").set_index("mol_id")
phys_data = pd.read_json("path_to_physdata.json").set_index("mol_id")

# Initialize vectorGC model to be fitted; use square root as normalization between properties
vecGC = models.vectorGC(chem_id, group_info, phys_data=phys_data, normalize="sqrt")

# Fit vectorGC model and generate results dictionaries
solver.fit(vecGC)
vecGC.get_fit_results()

# Perform leave-one-out cross-validation and generate results dictionaries (Attention: This can take up a lot of time & resources!)
solver.loocv(vecGC)
vecGC.get_loocv_results()

# Save the model in a pickle file
vecGC.save(path2outdir,filename)
```

### Required Inputs
The model classes for PCP-SAFT regression require information on the chemical structure (`chem_id`), the groups and bonds that should be parametrized (`group_info`), and physical property data for vapor pressures and liquid densities (`phys_data`). See also [example_preprocessing_halogenated_compounds.ipynb](./examples/example_preprocessing_halogenated_compounds.ipynb) and [example_preprocessing_oxygenated_compounds.ipynb](./examples/example_preprocessing_oxygenated_compounds.ipynb) for examples how to create inputs.

#### `chem_id` dataframe:
---
| `mol_id` | `isomeric_smiles` | `mw` | `exp_dipole_moment` | `iupac_name` (or other additional identifier)
| ------------- | ------------- | ------------- | ------------- | ------------- |
| *(Mandatory)* Unique identifier for each considered substance | *(Mandatory)* Isomeric Smiles of each considered substance | *(Mandatory)* Molar weight of each considered substance | *(Optional)* Known experimental dipole moment of each substance | *(Optional)* Additional identifier / information for each substance|
---

#### `group_info` dictionary:
---
```Python
{
  "smarts" : dict,            
  "bonds" : dict,            
  "initvals" : dict,        
  "known_groups" : dict,
  "scaling_factors" : dict
}
```
##### `smarts` dictionary: Used to define considered groups, known and to be fitted
| | |
| -- | -- |
| **Keys** | Considered group as String |
| **Values** | Corresponding [SMART](https://daylight.com/dayhtml/doc/theory/theory.smarts.html) as String |
Example:
```Python
"smarts" : {
  "-CH3" : "[CH3;!R;!$([CH3][CH3]);!$([CH3][OH]);!$([CH3][NH2])]",
  "-CH2-": "[$([CX4H2]);!R;!$([CH2]=O)]",
  "F": "[$(F[C])]",
  ...
}
```
##### `bonds` dictionary: Used to define considered bonds, known and to be fitted
| | |
| -- | -- |
| **Keys** | Considered bond as String |
| **Values** | Array defining the bond with ["Atom with higher electronegativitiy", "Atom with lower electronegativity", Identifier for bond type: 1.0 for SINGLE, 1.5 for AROMATIC, 2.0 for DOUBLE bond] |
Example:
```Python
"bonds" : {
  "C-H" : ["C","H",1.0],
  "F-C" : ["F","C",1.0],
  ...
}
```
##### `initvals` dictionary: Used to define to be fitted groups and bonds and their initial values
| | |
| -- | -- |
| **Keys** | Considered bond or group as String; must match with defined Strings from `smarts` and `bonds` dictionaries |
| **Values** | Initial value(s) for the considered bond or group; `Float` in case of bonds; `dict` in case of groups |
Example: 
```Python
"initvals" : {
  "F-C" : 1.5,
  "F" : {"m" : 0.3, "sigma" : 3.5, "epsilon" : 350.0},
  ...
}
```
##### `known_groups` dictionary: Used to define known groups or bonds that should not be fitted
| | |
| -- | -- |
| **Keys** | Known, considered bond or group as String; must match with defined Strings from `smarts` and `bonds` dictionaries |
| **Values** | Known value(s) for considered bond or group; `Float` in case of bonds; `dict` in case of groups |
Example: 
```Python
"known_groups" : {
  "C-H" : 0.0,,
  "-CH3": {'m': 0.6119800000000001, 'sigma': 3.7202, 'epsilon': 229.9},
  "-CH2-": {'m': 0.45606, 'sigma': 3.89, 'epsilon': 239.01},
  ...
}
```
##### `scaling_factors` dictionary: Used to scale fit variables (group contributions) to same order of magnitude for solver
| | |
| -- | -- |
| **Keys** | PCP-SAFT parameters as String |
| **Values** | Factor that is used to scale group variables to same order of magnitude for solver |
Example: 
```Python
"scaling_factors" : {
  "m" : 1.0,
  "sigma": 4.0,
  "epsilon": 400.0,
  "mu" : 3.0,
  ...
}
```
---

#### `phys_data` dataframe:
---
| `mol_id` | `property` | `phase` | `temperature` | `pressure` | `value` | 
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| *(Mandatory)* Unique identifier for each considered substance, must match to `chem_id` | *(Mandatory)* Property of data point: `pressure` for vapor pressures or `density` for densities | *(Mandatory)* Phase of data point: `Vapor`, `Vapor (VLE)`, `Liquid`, `Liquid (VLE)`, or `Critical Point` | *(Mandatory)* Temperature of the data point in $\mathrm{K}$ | *(If applicable)* Pressure of the data point in $\mathrm{Pa}$ - only required for Densities (`property`==`density`) in liquid state (`phase`=`Liquid`) | *(Mandatory)* Value of the property: Pressures in $\mathrm{Pa}$ and Densities in $\mathrm{kg}/\mathrm{m}^3$ |
---

### Implementing new sum rules
See [example_implement_Sauer2014_sumrules.ipynb](./examples/example_implement_Sauer2014_sumrules.ipynb) for an example how to use the `pcsaftGC` model class to define other sum rules. Here, we show implementing the sum rules for $\mu$, $\varepsilon^{A_iB_i}$, and $\kappa^{A_iB_i}$ defined by [Sauer *et al.*, 2014](https://pubs.acs.org/doi/full/10.1021/ie502203w). Re-implementing sum rules for $m$, $\sigma$, and $\varepsilon$ works equivalently by overloading the function `sum_rules_pcpsaft`, see [models source code](./vectorGC/regression_framework/models.py).

### Running regression & loading model
Examples for running the regression and loading models can be found in the examples folder. The script [run_model_regression.py](./run_model_regression.py) additionally yields an executable script that can be run as a background job.

## Publication data
The regressed group parameters from our [publication](https://doi.org/10.1021/acsomega.4c04867) are available as csv and json files in the raw data folder: [Hemprich2024](./resources/raw_data/Hemprich2024/).

## Cite us

If you find `Vector-GC` or the developed regression framework useful for your own research, consider citing our [publication](https://doi.org/10.1021/acsomega.4c04867) from which this repository resulted.

```
@article{hemprich2024,
  author = {Hemprich, Carl and Rehner, Philipp and Esper, Timm and Gross, Joachim and Roskosch, Dennis and Bardow, André},
  title = {Modeling Dipolar Molecules with PCP-SAFT: A Vector Group-Contribution Method}
  journal = {ACS Omega},
  volume = {XX},
  number = {XX},
  pages = {XX},
  year = {2024}
}
```