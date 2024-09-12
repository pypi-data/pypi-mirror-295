import pandas as pd
import geopandas as gpd

from sqlalchemy import text

class GeolevelDataType:
    # Constructor
    def __init__(
            self,
            custdata_type_id:int,
            name:str,
            properties:dict,
            geolevel_id:int,
            org:'Org' # type: ignore
    ):
        self.geolevel_data_type_id = custdata_type_id
        self.name = name
        self.properties = properties
        self.geolevel_id = geolevel_id
        self.org = org

    # Getters
    @property
    def geoleveldata_type_id(self): return self._geoleveldata_type_id
    @property
    def name(self): return self._name
    @property
    def properties(self): return self._properties
    @property
    def geolevel_id(self): return self._geolevel_id
    @property
    def org(self): return self._org
