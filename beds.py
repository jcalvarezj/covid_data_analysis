import json

class BedsRecord:
    """
    This class represents a record from the beds capacity dataset
    """
    def __init__(self, code=None, lat=None, lng=None, beds_average=None,
                 beds_total=None, population_average=None, 
                 estimated_beds_total=None, estimated_beds_average=None):
        self._code = code
        self._lat = lat
        self._lng = lng
        self._beds_average = beds_average
        self._beds_total = beds_total
        self._population_average = population_average
        self._estimated_beds_total = estimated_beds_total
        self._estimated_beds_average = estimated_beds_average
        self._bed_type = []


    def __str__(self):
        structure = {
            'code': self._code,
            'lat': self._lat,
            'lng': self._lng,
            'bedsTotal': self._beds_total,
            'bedsAverage': self._beds_average,            
            'populationAverage': self._population_average,
            'estimatedBedsTotal': self._estimated_beds_total,
            'estimatedBedsAverage': self._estimated_beds_average,
            'bedType': self._bed_type
        }        
        return json.dumps(structure, indent=4)

    
    def add_bed_type(self, bed_type):
        """
        Adds a BedTypesData object to the instance's bed_type list
        """
        self._bed_type.append(bed_type)


class BedTypesData:
    """
    This class represents an object of bed types
    """
    def __init__(self, type_name=None, count=None, percentage=None,
                 population=None, estimated_for_population=None, source=None,
                 source_url=None):
        self._type_name = type_name
        self._count = count
        self._percentage = percentage
        self._population = population
        self._estimated_for_population = estimated_for_population
        self._source = source
        self._source_url = source_url


    def getStructure(self):
        structure = {
            self._type_name: self._count,
            'percentage': self._percentage,
            'population': self._population,
            'estimatedForPopulation': self._estimated_for_population,
            'source': self._source,
            'sourceUrl': self._source_url
        }
        return structure