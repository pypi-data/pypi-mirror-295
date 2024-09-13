# lqlpath

`lqlpath` is a Python package designed to search for paths in JSON files based on either keys or values. 
## Features

- **Search by Key**: Retrieve a list of field paths in the JSON where a specific key is found.
- **Search by Value**: Retrieve a list of field paths in the JSON where a specific value is found.

#EXAMPLE

from lqlpath import get_byKey,get_byValue
##
print(get_byKey('bq.json','reservation'))
##
print(get_byValue('bq.json',"us-central1"))


output:
['protoPayload.serviceData.jobInsertResponse.resource.jobStatistics.reservation']
['protoPayload.serviceData.jobInsertResponse.resource.jobName.location']