import uuid
import os
import csv
import geohash
from shapely.geometry import Polygon as ShapelyPolygon, box
from queue import Queue
from shapely import intersects
from datetime import date, timedelta, datetime
from typing import List, Dict, Any, Tuple

class Base:
    """
    Base class for all query types.

    This class contains common functionality for date validation,
    filter validation, and basic query composition.

    :param before: The end date for the query range (inclusive), defaults to today.
    :param after: The start date for the query range (inclusive), defaults to 2 years ago.
    :param filters: A dictionary of additional filters to apply to the query.
    """

    def __init__(
            self, 
            before: str = str(date.today().strftime('%Y-%m-%d')),
            after: str = str((date.today() - timedelta(days=730)).strftime('%Y-%m-%d')),
            filters: Dict[str, Any] = {}
        ):
        self.before = before
        self.after = after
        self.filters = filters
        self.statement = ""

    def validate(self) -> bool:
        """
        Validate the input parameters for the query.

        :return: True if all parameters are valid, False otherwise.
        """
        if not self._validate_dates():
            print("Date validation failed.")
            return False

        if not self._validate_filters():
            print("Filters validation failed.")
            return False

        return True

    def _validate_dates(self) -> bool:
        """
        Validate the 'before' and 'after' date parameters.

        :return: True if dates are valid, False otherwise.
        """
        try:
            before_date = datetime.strptime(self.before, '%Y-%m-%d').date()
            after_date = datetime.strptime(self.after, '%Y-%m-%d').date()
        except ValueError:
            print("Date format error.")
            return False

        today = date.today()
        two_years_prior = today - timedelta(days=730)

        if not (two_years_prior <= before_date <= today):
            print(f"Before date {before_date} not in the valid range.")
            return False

        if not (two_years_prior <= after_date <= today):
            print(f"After date {after_date} not in the valid range.")
            return False

        if after_date > before_date:
            print("After date is not before the before date.")
            return False

        return True

    def _validate_filters(self) -> bool:
        """
        Validate the filters dictionary.

        :return: True if filters are valid, False otherwise.
        """
        valid_filter_keys = [
            'device_make', 'device_model', 'device_os', 'device_os_version',
            'derived_country', 'ip_address', 'horizontal_accuracy', 'operator_name', 
            'user_locale', 'geohash'
        ]
        
        if not isinstance(self.filters, dict):
            print("Filters is not a dictionary.")
            return False

        for key, value in self.filters.items():
            if key not in valid_filter_keys:
                print(f"Invalid filter key: {key}")
                return False
            
            if isinstance(value, (list, tuple)):
                if not all(isinstance(item, (str, int, float)) for item in value):
                    print(f"Filter {key} has invalid values: {value}")
                    return False
            elif not isinstance(value, (str, int, float)):
                print(f"Filter {key} is not a valid type: {type(value)}")
                return False

        return True

    def build_date_filter(self) -> str:
        """
        Build the SQL filter for the date range.

        :return: A string containing the SQL filter for the date range.
        """
        return f"to_date(timestamp) between '{self.after}' and '{self.before}'"

    def build_custom_filters(self) -> str:
        """
        Build custom SQL filters based on the filters dictionary.

        :return: A string containing the custom SQL filters.
        """
        filters = []
        for filter_name, filter_value in self.filters.items():
            if isinstance(filter_value, (list, tuple)):
                formatted_values = [f"lower('{v}')" if isinstance(v, str) else str(v) for v in filter_value]
                if filter_name in ['device_make', 'device_model', 'device_os', 'device_os_version', 'derived_country', 'ip_address', 'operator_name', 'user_locale']:
                    filters.append(f"lower({filter_name}) in ({', '.join(formatted_values)})")
                elif filter_name in ['horizontal_accuracy']:
                    if len(formatted_values) == 2:
                        filters.append(f"{filter_name} between {min(formatted_values)} and {max(formatted_values)}")
                    else:
                        filters.append(f"{filter_name} in ({', '.join(formatted_values)})")
                elif filter_name == 'geohash':
                    geohash_conditions = [f"{filter_name} like '{v}%'" for v in filter_value]
                    filters.append(f"({' or '.join(geohash_conditions)})")
            elif isinstance(filter_value, str):
                filters.append(f"lower({filter_name}) = lower('{filter_value}')")
            else:
                filters.append(f"{filter_name} = {filter_value}")
        
        return " and ".join(filters)

    def compose(self) -> None:
        """
        Compose the final SQL query statement.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement compose method")


class Ids(Base):
    """
    A class to handle ID-based queries.

    :param ids: A list of ID strings to query.
    :param device_history: A boolean indicating whether to return full device history.

    Example:
        >>> from a6py.snowflake import SnowflakeConnection
        >>> from a6py.query import Query
        >>> from a6py.blocks import Ids
        >>> 
        >>> ids_query = Query(blocks=[
        ...     Ids(
        ...         ids=['123e4567-e89b-12d3-a456-426614174000', '987e6543-e21b-12d3-a456-426614174000'],
        ...         before='2023-09-30',
        ...         after='2023-09-01',
        ...         filters={'device_make': 'Apple', 'horizontal_accuracy': [0, 100]},
        ...         device_history=True
        ...     )
        ... ])
        >>> 
        >>> sf_obj = SnowflakeConnection()
        >>> sf_obj.run(ids_query)
        >>> print(ids_query.results[:5])
    """

    def __init__(
            self, 
            ids: List[str], 
            before: str = str(date.today().strftime('%Y-%m-%d')),
            after: str = str((date.today() - timedelta(days=730)).strftime('%Y-%m-%d')),
            filters: Dict[str, Any] = {},
            device_history: bool = False
        ):
        super().__init__(before, after, filters)
        self.ids = ids
        self.device_history = device_history

    def validate(self) -> bool:
        """
        Validate the input parameters for the query.

        :return: True if all parameters are valid, False otherwise.
        """
        if not isinstance(self.ids, list) or not all(isinstance(id, str) and self._is_valid_uuid(id) for id in self.ids):
            print("IDs are not a list of valid UUIDs.")
            return False

        return super().validate()

    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """
        Check if a string is a valid UUID.

        :param uuid_string: The string to check.
        :return: True if the string is a valid UUID, False otherwise.
        """
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False

    def build_id_filter(self) -> str:
        """
        Build the SQL filter for IDs.

        :return: A string containing the SQL filter for IDs.
        """
        return " or ".join([f"lower(idfa) = lower('{id}')" for id in set(self.ids)])

    def build_prefix_filter(self) -> str:
        """
        Build the SQL filter for ID prefixes.

        :return: A string containing the SQL filter for ID prefixes.
        """
        return " or ".join([f"idfa like '{id[:3].upper()}%'" for id in set(self.ids)])

    def compose(self) -> None:
        """
        Compose the final SQL query statement.

        This method combines all the filters and constructs the complete SQL query.
        The result is stored in the `statement` attribute.
        """
        filters = [
            self.build_id_filter(),
            self.build_prefix_filter(),
            self.build_date_filter(),
            self.build_custom_filters()
        ]
        
        formatted_filters = "where\n\t" + " and\n\t".join([f"({f})" for f in filters if f])

        headers = "select\n\t*" if self.device_history else "select\n\tdistinct lower(idfa)"

        self.statement = f"{headers}\nfrom\n\t{os.getenv('SNOWFLAKE_DATABASE')}.public.h4_maid_clustered\n{formatted_filters}"

class Polygon(Base):
    """
    A class to handle polygon-based queries.

    :param coordinates: A list of coordinate tuples defining the polygon.

    Example:
        >>> from a6py.snowflake import SnowflakeConnection
        >>> from a6py.query import Query
        >>> from a6py.blocks import Polygon
        >>> 
        >>> polygon_query = Query(blocks=[
        ...     Polygon(
        ...         coordinates=[
        ...             (40.7128, -74.0060),  # New York City
        ...             (34.0522, -118.2437),  # Los Angeles
        ...             (41.8781, -87.6298),  # Chicago
        ...             (40.7128, -74.0060)   # Back to New York to close the polygon
        ...         ],
        ...         before='2023-09-30',
        ...         after='2023-09-01',
        ...         filters={'device_os': 'iOS', 'horizontal_accuracy': [0, 50]}
        ...     )
        ... ])
        >>> 
        >>> sf_obj = SnowflakeConnection()
        >>> sf_obj.run(polygon_query)
        >>> print(polygon_query.results[:5])
    """

    def __init__(
            self, 
            coordinates: List[Tuple[float, float]], 
            before: str = str(date.today().strftime('%Y-%m-%d')),
            after: str = str((date.today() - timedelta(days=730)).strftime('%Y-%m-%d')),
            filters: Dict[str, Any] = {}
        ):
        super().__init__(before, after, filters)
        self.coordinates = coordinates

    def validate(self) -> bool:
        """
        Validate the input parameters for the query.

        :return: True if all parameters are valid, False otherwise.
        """
        if not isinstance(self.coordinates, list):
            print("Coordinates are not a list.")
            return False

        if not all(isinstance(coord, tuple) and len(coord) == 2 and all(isinstance(val, (int, float)) for val in coord) for coord in self.coordinates):
            print("Coordinates are not a list of tuples with two float/int elements.")
            return False

        if not all(-90 <= lat <= 90 and -180 <= lon <= 180 for lat, lon in self.coordinates):
            print("Latitude or longitude out of bounds.")
            return False

        return super().validate()

    def build_polygon_filter(self) -> str:
        """
        Build the SQL filter for the polygon.

        :return: A string containing the SQL filter for the polygon.
        """
        polygon_points = ", ".join([f"{lon} {lat}" for lat, lon in self.coordinates])
        return f"st_contains(st_polygon(to_geography('linestring({polygon_points})')), to_geography(st_point(longitude, latitude)))"

    def build_geohash_filter(self) -> str:
        """
        Build the SQL filter for geohashes that intersect with the polygon.

        :return: A string containing the SQL filter for geohashes.
        """
        # Convert the custom Polygon to a Shapely Polygon
        shapely_polygon = ShapelyPolygon(self.coordinates)
        
        # Find initial geohashes from polygon vertices
        initial_geohashes = set(geohash.encode(lat, lon, precision=3) for lat, lon in self.coordinates)
        
        # Initialize result set with initial geohashes
        result = set(initial_geohashes)
        
        # Set up for BFS
        to_check = Queue()
        for gh in initial_geohashes:
            to_check.put(gh)
        
        checked = set()
        
        while not to_check.empty():
            current = to_check.get()
            if current in checked:
                continue
            
            checked.add(current)
            
            # Check if the geohash intersects or is contained by the polygon
            bbox = geohash.bbox(current)
            gh_polygon = box(bbox['w'], bbox['s'], bbox['e'], bbox['n'])
            
            if intersects(shapely_polygon, gh_polygon):
                if current not in result:
                    result.add(current)
                
                # Add neighbors to the queue
                neighbors = geohash.neighbors(current)
                for neighbor in neighbors:
                    if neighbor not in checked:
                        to_check.put(neighbor)
        return " or ".join([f"geohash like '{gh}%'" for gh in result])

    def compose(self) -> None:
        """
        Compose the final SQL query statement.

        This method combines all the filters and constructs the complete SQL query.
        The result is stored in the `statement` attribute.
        """
        filters = [
            self.build_polygon_filter(),
            self.build_date_filter(),
            self.build_geohash_filter(),
            self.build_custom_filters()
        ]
        
        formatted_filters = "where\n\t" + " and\n\t".join([f"({f})" for f in filters if f])

        self.statement = f"select\n\tdistinct lower(idfa)\nfrom\n\t{os.getenv('SNOWFLAKE_DATABASE')}.public.h4_geo_clustered\n{formatted_filters}"


class BoundaryBox(Base):
    """
    A class to handle boundary box-based queries.

    :param lower_left_lat: Latitude of the lower left corner of the boundary box.
    :param lower_left_lon: Longitude of the lower left corner of the boundary box.
    :param upper_right_lat: Latitude of the upper right corner of the boundary box.
    :param upper_right_lon: Longitude of the upper right corner of the boundary box.

    Example:
        >>> from a6py.snowflake import SnowflakeConnection
        >>> from a6py.query import Query
        >>> from a6py.blocks import BoundaryBox
        >>> 
        >>> boundarybox_query = Query(blocks=[
        ...     BoundaryBox(
        ...         lower_left_lat=40.7128,
        ...         lower_left_lon=-74.0060,
        ...         upper_right_lat=40.7828,
        ...         upper_right_lon=-73.9360,
        ...         before='2023-09-30',
        ...         after='2023-09-01',
        ...         filters={'device_model': ['iPhone12,1', 'iPhone13,2'], 'operator_name': 'Verizon'}
        ...     )
        ... ])
        >>> 
        >>> sf_obj = SnowflakeConnection()
        >>> sf_obj.run(boundarybox_query)
        >>> print(boundarybox_query.results[:5])
    """

    def __init__(
            self, 
            lower_left_lat: float,
            lower_left_lon: float,
            upper_right_lat: float,
            upper_right_lon: float,
            before: str = str(date.today().strftime('%Y-%m-%d')), 
            after: str = str((date.today() - timedelta(days=730)).strftime('%Y-%m-%d')),
            filters: Dict[str, Any] = {}
        ):
        super().__init__(before, after, filters)
        self.lower_left_lat = lower_left_lat
        self.lower_left_lon = lower_left_lon
        self.upper_right_lat = upper_right_lat
        self.upper_right_lon = upper_right_lon

    def validate(self) -> bool:
        """
        Validate the input parameters for the query.

        :return: True if all parameters are valid, False otherwise.
        """
        if not all(isinstance(coord, (int, float)) for coord in [self.lower_left_lat, self.lower_left_lon, self.upper_right_lat, self.upper_right_lon]):
            print("Coordinates are not valid numbers.")
            return False

        if not (-90 <= self.lower_left_lat < self.upper_right_lat <= 90 and
                -180 <= self.lower_left_lon < self.upper_right_lon <= 180):
            print("Coordinates are out of valid range.")
            return False

        return super().validate()

    def build_boundary_box_filter(self) -> str:
        """
        Build the SQL filter for the boundary box.

        :return: A string containing the SQL filter for the boundary box.
        """
        return f"latitude between {self.lower_left_lat} and {self.upper_right_lat} and longitude between {self.lower_left_lon} and {self.upper_right_lon}"

    def build_geohash_filter(self) -> str:
        """
        Build the SQL filter for geohashes that intersect with the boundary box.

        :return: A string containing the SQL filter for geohashes.
        """
        # Convert the BoundaryBox to a Shapely Polygon
        shapely_polygon = box(self.lower_left_lon, self.lower_left_lat, self.upper_right_lon, self.upper_right_lat)
        
        # Find initial geohashes from polygon vertices
        initial_geohashes = set([
            geohash.encode(self.lower_left_lat, self.lower_left_lon, precision=3),
            geohash.encode(self.lower_left_lat, self.upper_right_lon, precision=3),
            geohash.encode(self.upper_right_lat, self.lower_left_lon, precision=3),
            geohash.encode(self.upper_right_lat, self.upper_right_lon, precision=3)
        ])
        
        # Initialize result set with initial geohashes
        result = set(initial_geohashes)
        
        # Set up for BFS
        to_check = Queue()
        for gh in initial_geohashes:
            to_check.put(gh)
        
        checked = set()
        
        while not to_check.empty():
            current = to_check.get()
            if current in checked:
                continue
            
            checked.add(current)
            
            # Check if the geohash intersects or is contained by the polygon
            bbox = geohash.bbox(current)
            gh_polygon = box(bbox['w'], bbox['s'], bbox['e'], bbox['n'])
            
            if shapely_polygon.intersects(gh_polygon):
                if current not in result:
                    result.add(current)
                
                # Add neighbors to the queue
                neighbors = geohash.neighbors(current)
                for neighbor in neighbors:
                    if neighbor not in checked:
                        to_check.put(neighbor)
        
        return " or ".join([f"geohash like '{gh}%'" for gh in result])

    def compose(self) -> None:
        """
        Compose the final SQL query statement.

        This method combines all the filters and constructs the complete SQL query.
        The result is stored in the `statement` attribute.
        """
        filters = [
            self.build_boundary_box_filter(),
            self.build_date_filter(),
            self.build_geohash_filter(),
            self.build_custom_filters()
        ]
        
        formatted_filters = "where\n\t" + " and\n\t".join([f"({f})" for f in filters if f])

        self.statement = f"select\n\tdistinct lower(idfa)\nfrom\n\t{os.getenv('SNOWFLAKE_DATABASE')}.public.h4_geo_clustered\n{formatted_filters}"

class Country(Base):
    """
    A class to handle country-based queries.

    :param country: A 3-character ISO country code.

    Example:
        >>> from a6py.snowflake import SnowflakeConnection
        >>> from a6py.query import Query
        >>> from a6py.blocks import Country
        >>> 
        >>> country_query = Query(blocks=[
        ...     Country(
        ...         country='USA',
        ...         before='2023-09-30',
        ...         after='2023-09-01',
        ...         filters={'user_locale': 'en_US', 'device_os_version': ['14.0', '14.1', '14.2']}
        ...     )
        ... ])
        >>> 
        >>> sf_obj = SnowflakeConnection()
        >>> sf_obj.run(country_query)
        >>> print(country_query.results[:5])
    """


    def __init__(
            self, 
            country: str,
            before: str = str(date.today().strftime('%Y-%m-%d')), 
            after: str = str((date.today() - timedelta(days=730)).strftime('%Y-%m-%d')),
            filters: Dict[str, Any] = {}
        ):
        super().__init__(before, after, filters)
        self.country = country.lower()

    def validate(self) -> bool:
        """
        Validate the input parameters for the query.

        :return: True if all parameters are valid, False otherwise.
        """
        if not isinstance(self.country, str) or len(self.country) != 3:
            print("Country code must be a 3-character string.")
            return False

        with open("data/country_geos.csv", 'r') as f:
            reader = csv.DictReader(f)
            if not any(row['iso3'].lower() == self.country.lower() for row in reader):
                print(f"Country code {self.country} not found in the list of valid countries.")
                return False

        return super().validate()

    def build_country_filter(self) -> str:
        """
        Build the SQL filter for the country.

        :return: A string containing the SQL filter for the country.
        """
        return f"derived_country = '{self.country}'"

    def build_geohash_filter(self) -> str:
        """
        Build the SQL filter for geohashes associated with the country.

        :return: A string containing the SQL filter for geohashes.
        """
        with open("data/country_geos.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['iso3'].lower() == self.country.lower():
                    geohashes = row['geohashes']
                    return " or ".join([f"geohash like '{gh}%'" for gh in geohashes.split(',')])
        return ""

    def compose(self) -> None:
        """
        Compose the final SQL query statement.

        This method combines all the filters and constructs the complete SQL query.
        The result is stored in the `statement` attribute.
        """
        filters = [
            self.build_country_filter(),
            self.build_geohash_filter(),
            self.build_date_filter(),
            self.build_custom_filters()
        ]
        
        formatted_filters = "where\n\t" + " and\n\t".join([f"({f})" for f in filters if f])

        self.statement = f"select\n\tdistinct lower(idfa)\nfrom\n\t{os.getenv('SNOWFLAKE_DATABASE')}.public.h4_geo_clustered\n{formatted_filters}"


class Geohashes(Base):
    """
    A class to handle geohash-based queries.

    :param geohashes: A list of geohash strings to query.

    Example:
        >>> from a6py.snowflake import SnowflakeConnection
        >>> from a6py.query import Query
        >>> from a6py.blocks import Geohashes
        >>> 
        >>> geohashes_query = Query(blocks=[
        ...     Geohashes(
        ...         geohashes=['dr5ru', 'dr5rv', 'dr5rt'],
        ...         before='2023-09-30',
        ...         after='2023-09-01',
        ...         filters={'derived_country': 'USA', 'ip_address': ['192.168.1.1', '10.0.0.1']}
        ...     )
        ... ])
        >>> 
        >>> sf_obj = SnowflakeConnection()
        >>> sf_obj.run(geohashes_query)
        >>> print(geohashes_query.results[:5])
    """

    def __init__(
            self, 
            geohashes: List[str], 
            before: str = str(date.today().strftime('%Y-%m-%d')), 
            after: str = str((date.today() - timedelta(days=730)).strftime('%Y-%m-%d')),
            filters: Dict[str, Any] = {}
        ):
        super().__init__(before, after, filters)
        self.geohashes = list(set(geohashes))  # Ensure distinct geohashes

    def validate(self) -> bool:
        """
        Validate the input parameters for the query.

        :return: True if all parameters are valid, False otherwise.
        """
        if not isinstance(self.geohashes, list) or not all(isinstance(gh, str) for gh in self.geohashes):
            print("Geohashes must be a list of strings.")
            return False

        if not all(self._is_valid_geohash(gh) for gh in self.geohashes):
            print("Invalid geohash format or value.")
            return False

        return super().validate()

    def _is_valid_geohash(self, geohash: str) -> bool:
        """
        Check if a string is a valid geohash.

        :param geohash: The string to check.
        :return: True if the string is a valid geohash, False otherwise.
        """
        import re
        # Check if the geohash is a string of length 1 to 12
        if not isinstance(geohash, str) or len(geohash) < 1 or len(geohash) > 12:
            return False
        
        # Check if the geohash only contains valid characters
        return bool(re.match(r'^[0123456789bcdefghjkmnpqrstuvwxyz]+$', geohash.lower()))

    def build_full_geohash_filter(self) -> str:
        """
        Build the SQL filter for the full geohashes.

        :return: A string containing the SQL filter for the full geohashes.
        """
        return " or ".join([f"geohash like '{gh}%'" for gh in self.geohashes])

    def build_geohash_filter(self) -> str:
        """
        Build the SQL filter for the first 3 characters of the geohashes.

        :return: A string containing the SQL filter for the geohash prefixes.
        """
        geos = list(set([x[:3] for x in self.geohashes]))
        return " or ".join([f"geohash like '{gh}%'" for gh in geos])

    def compose(self) -> None:
        """
        Compose the final SQL query statement.

        This method combines all the filters and constructs the complete SQL query.
        The result is stored in the `statement` attribute.
        """
        filters = [
            self.build_geohash_filter(),
            self.build_full_geohash_filter(),
            self.build_date_filter(),
            self.build_custom_filters()
        ]
        
        formatted_filters = "where\n\t" + " and\n\t".join([f"({f})" for f in filters if f])

        self.statement = f"select\n\tdistinct lower(idfa)\nfrom\n\t{os.getenv('SNOWFLAKE_DATABASE')}.public.h4_geo_clustered\n{formatted_filters}"
