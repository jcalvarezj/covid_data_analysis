import json

class BedsRecord:
    """
    This class represents a record from the beds capacity dataset
    """
    def __init__(self, code=None, lat=None, lng=None, beds=None,
                 population=None, source=None, source_url=None, 
                 bed_type=None, estimated_beds=None):
        self._code = code
        self._lat = lat
        self._lng = lng
        self._beds = beds
        self._population = population
        self._estimated_beds = estimated_beds
        self._source = source
        self._source_url = source_url
        self._bed_type = bed_type


    def __str__(self):
        return json.dumps(self.__dict__, indent=4)