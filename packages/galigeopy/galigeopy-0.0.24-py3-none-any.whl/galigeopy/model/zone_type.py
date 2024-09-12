import pandas as pd
from sqlalchemy import text

from galigeopy.model.zone import Zone

class ZoneType:
    def __init__(
        self,
        zone_type_id:int,
        name:str,
        org: 'Org' # type: ignore
    ):
        # Infos
        self._zone_type_id = zone_type_id
        self._name = name
        # Engine
        self._org = org

    def __str__(self):
        return self.name + " (" + str(self.zone_type_id) + ")"
    
    # Getters and setters
    @property
    def zone_type_id(self): return self._zone_type_id
    @property
    def name(self): return self._name
    @property
    def org(self): return self._org
    
    # Public Methods
    def number_of_zones(self):
        query = text(f"SELECT COUNT(*) FROM ggo_zone WHERE zone_type_id = {self.zone_type_id}")
        with self._org.engine.connect() as conn:
            result = conn.execute(query)
            return result.scalar()
        
    def getZonesList(self):
        query = text(f"SELECT * FROM ggo_zone WHERE zone_type_id = {self.zone_type_id}")
        return pd.read_sql(query, self._org.engine)
    
    def getZoneById(self, zone_id:int):
        query = f"SELECT * FROM ggo_zone WHERE zone_id = {zone_id} AND zone_type_id = {self.zone_type_id}"
        df = pd.read_sql(query, self._org.engine)
        if len(df) > 0:
            data = df.iloc[0].to_dict()
            data.update({"org": self._org})
            return Zone(**data) 
        else:
            raise Warning(f"Zone {zone_id} not found in ZoneType {self.name}")
        
    def getAllZones(self):
        query = text(f"SELECT * FROM ggo_zone WHERE zone_type_id = {self.zone_type_id}")
        df = pd.read_sql(query, self._org.engine)
        zones = []
        for i in range(len(df)):
            data = df.iloc[i].to_dict()
            data.update({"org": self._org})
            zones.append(Zone(**data))
        return zones
        
    def add_to_model(self)-> int:
        # Add to database
        query = f"""
        INSERT INTO ggo_zone_type (
            name
        ) VALUES (
            '{self.name.replace("'", "''")}'
        ) RETURNING zone_type_id;
        """
        zone_type_id = self._org.query(query)[0][0]
        return zone_type_id

