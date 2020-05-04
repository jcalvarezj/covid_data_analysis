import json

class BedsRecord:
    """
    This class represents a record from the beds capacity dataset
    """
    def __init__(self, code=None, lat=None, lng=None, beds_average=None,
                 population=None, estimated_beds_average=None, source=None,
                 source_url=None):
        self._code = code
        self._lat = lat
        self._lng = lng
        self._beds_average = beds_average
        self._population = population
        self._estimated_beds_average = estimated_beds_average
        self._source = source
        self._source_url = source_url
        self._bed_type = []


    def __str__(self):
        structure = {
            'code': self._code,
            'lat': self._lat,
            'lng': self._lng,
            'bedsAverage': self._beds_average,
            'population': self._population,
            'estimatedBedsAverage': self._estimated_beds_average,
            'source': self._source,
            'sourceUrl': self._source_url,
            'bedType': self._bed_type
        }        
        return json.dumps(structure, indent=4)

    
    def add_bed_types(self, bed_types):
        """
        Adds all the bed_types objects to the instance's bed_type list
        """
        for bt in bed_types:
            self._bed_type.append(bt)