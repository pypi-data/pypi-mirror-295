# cv_timeseries

Description.\
The package cv_timeseries is used to:\
	- Calculate the variation coefficient (VC) of a time series;\
	- Plot the VC.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cv_timeseries

```bash
pip install cv_timeseries
```

## Usage

```python
from cv_timeseries.statistics.calculate_cv import VC
from cv_timeseries.plots.plot_cv import Plot


cv = VC(time_series).calculate_vc()
Plot(cv).plot_cv()
```

## Author
Ana Sofia

## License
[MIT](https://choosealicense.com/licenses/mit/)