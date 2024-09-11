# tagmapper-sdk
Prototype python package to get IMS-tag mappings for data models for separators and wells.

Authentication is done using Azure credentials and bearer tokens.


## Use
See (examples/demo_separator.py)[demo]. Or try the following simple code.  
```
from tagmapper import Well


w = Well("NO 30/6-E-2")  
```


## Installing
Install from github using pip.  
``
pip install git+https://github.com/equinor/tagmapper-sdk.git
``


## Developing
Clone repo and run ``poetry install`` to install dependencies.


## Testing
Run tests and check coverage using pytest-cov
``poetry run pytest --cov=tagmapper test/ --cov-report html``
