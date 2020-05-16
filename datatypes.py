import json

class BedsRecord:
    """
    This class represents a record from the beds capacity dataset
    """
    def __init__(self, code = None, lat = None, lng = None,
                 beds_average = None, beds_total = None,
                 estimated_beds_total = None, estimated_beds_average = None,
                 population_average = None):
        self._code = code
        self._lat = lat
        self._lng = lng
        self._beds_average = beds_average
        self._beds_total = beds_total
        self._population_average = population_average
        self._estimated_beds_total = estimated_beds_total
        self._estimated_beds_average = estimated_beds_average


    def __str__(self):
        return json.dumps(self.to_json())


    def __repr__(self):
        return str(self)


    def to_json(self):
        """
        Returns the json representation of the BedsRecord instance
        """
        return {
            'code': self._code,
            'lat': self._lat,
            'lng': self._lng,
            'bedsTotal': self._beds_total,
            'bedsAverage': self._beds_average,
            'populationAverage': self._population_average,
            'estimatedBedsTotal': self._estimated_beds_total,
            'estimatedBedsAverage': self._estimated_beds_average
        }


class BedTypesData:
    """
    This class represents a bed type information object
    """
    def __init__(self, code = None, type_name = None, count = None,
                 percentage = None, population = None,
                 estimated_for_population = None, source = None,
                 source_url = None, year = None):
        self._code = code
        self._type_name = type_name
        self._count = count
        self._percentage = percentage
        self._population = population
        self._estimated_for_population = estimated_for_population
        self._source = source
        self._source_url = source_url
        self._year = year


    def __str__(self):
        return json.dumps(self.to_json())


    def __repr__(self):
        return str(self)


    def to_json(self):
        """
        Returns the json representation of the BedTypesData instance
        """
        return {
            'code': self._code,
            'type': self._type_name,
            'total': self._count,
            'percentage': self._percentage,
            'population': self._population,
            'estimatedForPopulation': self._estimated_for_population,
            'source': self._source,
            'sourceUrl': self._source_url,
            'year': self._year
        }


class BedsGeneralData:
    """
    This class represents the object that stores general beds statistics
    """
    def __init__(self, beds_count = None, beds_average = None, 
                 beds_stantard_deviation = None, sources_count = None):
        self._beds_count = beds_count
        self._beds_average = beds_average
        self._beds_stantard_deviation = beds_stantard_deviation
        self._sources_count = sources_count


    def __str__(self):
        return json.dumps(self.to_json())


    def __repr__(self):
        return str(self)


    def to_json(self):
        return {
            'bedCount': self._beds_count,
            "bedAverage": self._beds_average,
            "bedStandardDeviation": self._beds_stantard_deviation,
            "sourcesCount": self._sources_count
        }


class BedTypesGeneralData:
    """
    This class represents the object that stores general bed types statistics
    """
    def __init__(self, type_name = None, count = None, percentage = None,
                  average = None, standard_deviation = None):
        self._type_name = type_name
        self._count = count
        self._percentage = percentage
        self._average = average
        self._standard_deviation = standard_deviation


    def __str__(self):
        return json.dumps(self.to_json())


    def __repr__(self):
        return str(self)


    def to_json(self):
        return {
            "type": self._type_name,
            "count": self._count,
            "percentage": self._percentage,
            "average": self._average,
            "standardDeviation": self._standard_deviation
        }



class MeasuresData:
    """
    This class represents an object of measures and restrictions information
    """
    def __init__(self, code = None, date_start = None, date_end = None,
                 description = None, keywords = None, exceptions = None,
                 quantity = None, target_city = None, target_country = None,
                 target_region = None, target_state = None):
        self._code = code
        self._date_start = date_start
        self._date_end = date_end
        self._description = description
        self._keywords = keywords
        self._exceptions = exceptions
        self._quantity = quantity
        self._target_city = target_city
        self._target_country = target_country
        self._target_region = target_region
        self._target_state = target_state


    def __str__(self):
        return json.dumps(self.to_json())


    def __repr__(self):
        return str(self)


    def to_json(self):
        """
        Returns the json representation of the MeasuresData instance
        """
        return dict(self)