# LLC Science SDK

> A simple way to fetch scientific data from the Science Admin.
> Please visit {BASE_URL}/api/schema/swagger-ui/#/ for more information on the API.

## Installation

```sh
pip install llcsciencesdk
```

## Updating to a new version

```sh
pip install llcsciencesdk -U
```

## Usage

#### Specifying environment

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk() # connect to production
llc_api = ScienceSdk(environment="staging") # connect to staging
llc_api = ScienceSdk(environment="local") # connect to localhost
llc_api = ScienceSdk(environment="http://127.0.0.1:8009") # connect to custom url
```

#### Logging in

```python
from llcsciencesdk.llc_api import ScienceSdk

llc_api = ScienceSdk()
llc_api.login("username", "password")
```

#### Using the endpoints

```python
from llcsciencesdk.llc_api import ScienceSdk
llc_api = ScienceSdk()
llc_api.login("username", "password")
model_input = llc_api.get_ft_input(1)
planting_design_list = llc_api.get_planting_design_list()
planting_design_detail = llc_api.get_planting_design(10)
```



## Supported endpoints

See the swagger docs for a complete list. {BASE_URL}/api/schema/swagger-ui/#/

## For Developers

### Updating package

1. Make sure you have supported version of flit installed (see project.toml).

```
    python3 -m pip install flit
```

2. Set env variables for PiPy login:

```
    Get the token from the PiPy website and run the following commands:
```
3. Update the version of the API in the __init__.py file.
4. Run command to publish to PiPy:

```
    flit publish
```

