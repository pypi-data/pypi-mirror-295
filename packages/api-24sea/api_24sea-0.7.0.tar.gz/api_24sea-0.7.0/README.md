# API 24Sea

**api_24sea** is a project designed to provide aid for the interaction with data from the [24SEA API](https://api.24sea.eu/).

## Installation

```shell
pip install api_24sea
```

## DataSignals Usage


The following example shows the classical usage of the datasignals module.

* The first step is to import the package and the necessary libraries.
* Then, the environment variables are loaded from a `.env` file.
* After that, the package is initialized and the user is authenticated with the API.
* Finally, the user can get data from the API.

### Importing the package
```python
# %%
# **Package Imports**
# - From the Python Standard Library
import logging
import os

# - From third party libraries
import dotenv
import pandas as pd

# - Local imports
from api_24sea.version import __version__, parse_version
import api_24sea
```

### Setting up the environment variables

This step assumes that you have a file structure similar to the following one:

```shell
.
├── env/
│   └── .env
├── notebooks/
│   └── example.ipynb
└── requirements.txt
```

The `.env` file should look like this:

```shell
API_USERNAME=your_username
API_PASSWORD=your_password
```


With this in mind, the following code snippet shows how to load the environment
variables from the `.env` file:

```python
# %%
_ = dotenv.load_dotenv("../env/.env")
if _:
    print("Environment Variables Loaded Successfully")
    print(os.getenv("API_USERNAME"))
else:
    raise Exception("Environment Variables Not Loaded")
```

### Initializing an empty dataframe

Initializing an empty dataframe is necessary to use the API, as here is
where the data will be stored.

```python
# %%
df = pd.DataFrame()

# %%
try:
    df.datasignals.get_metrics()
except Exception as e:
    print("API not available")
    print(e)
```

### Authenticating with the API

The authentication step allows the user to access the API and check the
available metrics.

```python
# %%
df.datasignals.authenticate(
    os.getenv("API_USERNAME"), os.getenv("API_PASSWORD")
)
# After authentication, the user can access the API
```

### Checking the available metrics after authentication
```python
# %%
df.datasignals.metrics_overview
# It will show all the available metrics with the corresponding units
# and the time window for which the user is allowed to get data
```

### Getting sample data from the API

After loading the environment variables and authenticating with the API,
the user can get data from [24SEA API endpoints](https://api.24sea.eu/redoc/v1/).


```python
# %%
sites = ["windfarm"]
locations = ["a01", "a02"]
metrics = ["mean WinDSpEed", "Std-windspeed", "mean_pitch", "mean power"]

start_timestamp = "2020-03-01T00:00:00Z"
end_timestamp = "2020-06-01T00:00:00Z"

df.datasignals.get_data(sites, locations, metrics,
                        start_timestamp, end_timestamp,
                        outer_join_on_timestamp=True)
```


### Checking the metrics selected
```python
# %%
df.datasignals.selected_metrics
```

### Checking the data
```python
# %%
df
```

## Project Structure

```shell
.
├── .azure/
├── api_24sea/
│   ├── __init__.py
│   ├── datasignals/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── utils.py
│   └── version.py
├── tests/
├── docs/
├── notebooks/
├── pyproject.toml
├── LICENSE
├── VERSION
└── README.md
```

## License

The package is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
