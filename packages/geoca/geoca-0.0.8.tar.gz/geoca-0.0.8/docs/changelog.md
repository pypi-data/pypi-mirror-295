# Changelog

## v0.0.3 - 2024.2.24

**Improvement**:

- Remove all code used for initial project testing.

**New Features**:

- Read raster data from a file, convert the data into a Python list.
- Create a raster template based on the input raster, and replace the data from list into the new raster.
- Running CA models based on raster data to analyze population and other resource migration.

## v0.0.4 - 2024.3.18

**Improvement**:

- Modify the original code and comments.
- Add new Features.

**New Features**:

- Reads multiple raster data (.tif) from a folder and stores it in a dictionary.
- Reorganizes data from a list dictionary representing multiple raster data.

## v0.0.5 - 2024.3.29

**Improvement**:

- Fix some codes for exporting raster data.

## v0.0.6 - 2024.9.6

**Improvement**:

- Modify the names of some functions.

**New Features**:

- Running a cellular automata using an initial population size raster.

## v0.0.7 - 2024.9.11

**Improvement**:

- Modify the names of some functions.
- The direction of migration was reduced from eight to four (only east, west, south and north were retained).

**New Features**:

- The population can be dispersed and migrated to various neighboring areas based on the size of the raster pixel values.
- A proportion of the population can be focused and migrated to the most suitable areas.

## v0.0.8 - 2024.9.12

**Improvement**:

- Number of migration directions can be set (4 or 8).
