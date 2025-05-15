# PM4Sand2D_drivers_auto
## Scripts that produce multiple PM4Sand2D drivers for different loading paths, batch files for running them in FLAC 2D/9.00, and post-processing codes for plotting

### May 2025 updates:
- Added OS-based reading and writing of files in order to avoid path issues in IDEs
- improvements in path handling for IDEs

### April 2024 updates:
- Added extra flag for activating /deactivating FirstCall after static bias in undrained cyclic driver
- fixes in plotting files

### Structure

- Three folder structure (for now)
- building on katerinaziot/PM4Sand_drivers_auto for FLAC2D this time. Working with *.csv files now.
- PM4Sand2D* folders contain drivers and processing* folder contains post-processing and plotting files
- Each PM4Sand* folder provides the ability to create multiple FLAC *.f2fis drivers that cover various parameters and are named accordingly. A batch*.fis file is also produced that can be directly called in FLAC2D that will run them all and produce csv files with results in the same folder.
- Each plotting*.py file in the "processing_plotting" folder will process different drivers and produce Figures. Decode python file contains useful functions for all and ucdavis.mplstyle is used for figure styling.

### Driver details
#### PM4Sand2D_Cyclic_DSS_drained_batch
Produces strain controlled drained Direct Simple Shear drivers. Each driver features five elements, each at a different overburden. User can select relative densities. Options for exercising at a range of strains for a certain number of cycles at each one (will produce Modulus Reduction and Damping curves) or applying uniform cycles at the same shear strains for multiple cycles (will produce volumetric response). This can be controlled by the "volumetric" parameter.

#### PM4Sand2D_Cyclic_DSS_undrained_batch
Produces stress controlled undrained Direct Simple Shear drivers. Each driver features five elements, each at a different CSR. Middle element is exercised under the CRR of the relative density (set internally in DSS_cyclic_undrained.fis). User can select relative densities, overburdens, static shear stress bias values, and Ko values.

#### PENDING PM4Sand_Monotonic_batch
Produces drained and undrained monotonic Direct Simple Shear (DSS).

#### PENDING PM4Sand_Reconsolidation_batch
Produces stress controlled undrained Direct Simple Shear drivers.

### Original versions of processing and plotting files created by M-P Kippen in the framework of the PM4Sand3D development
---

Please send your comments, bugs, issues and features to add to [Katerina Ziotopoulou] at katerinaziot@gmail.com.
