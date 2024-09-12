# psdm2pp 


This is a work-in-progress tool for converting [PSDM](https://github.com/ie3-institute/PowerSystemDataModel) to [pandapower](https://github.com/e2nIEE/pandapower) grid models.


## Limitations 

- Currently only basic grid model conversion supported
- No switch conversion implemented yet


## Usage

```py
from pypsdm import RawGridContainer
from psdm2pp.grid import convert_grid

psdm_path = "/my/psdm_grid/path"
psdm_grid = RawGridContainer.from_csv(psdm_path)
pp_grid, uuid_idx_maps = convert_grid(psdm_grid)
```
