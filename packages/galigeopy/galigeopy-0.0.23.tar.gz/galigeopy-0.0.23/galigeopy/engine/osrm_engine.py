import requests

class OsrmEngine:
    def __init__(
            self,
            osrm_url:str,
            verified_url:bool=True,
            profile:str="driving",
            version:str="v1"
        ):
        self._osrm_url = osrm_url
        self._verified_url = verified_url
        self._profile = profile
        self._version = version

    # Getters and setters
    @property
    def osrm_url(self): return self._osrm_url
    @property
    def verified_url(self): return self._verified_url
    @property
    def profile(self): return self._profile
    @property
    def version(self): return self._version

    def get_nearest(self, location:dict, number:int=1)->list:
        url = f"{self.osrm_url.removesuffix('/')}/nearest/{self.version}/{self.profile}/{location['lng']},{location['lat']}"
        url += f"?number={number}"
        response = requests.get(url, verify=self.verified_url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        data = response.json()
        if data["code"] != "Ok":
            raise Exception(f"Error {data['code']}: {data['message']}")
        return data["waypoints"]

    def get_route(self, start, end,
        alternatives:bool=False,
        steps:bool=False,
        annotations:bool=False,
        geometries:str="polyline",
        overview:str="simplified",
        continue_straight:str="default",

    )->list:
        url = f"{self.osrm_url.removesuffix('/')}/route/{self.version}/{self.profile}/{start['lng']},{start['lat']};{end['lng']},{end['lat']}"
        # Properties
        url += f"?alternatives={str(alternatives).lower()}"
        url += f"&steps={str(steps).lower()}"
        url += f"&annotations={str(annotations).lower()}"
        url += f"&geometries={geometries}"
        url += f"&overview={overview}"
        url += f"&continue_straight={continue_straight}"
        response = requests.get(url, verify=self.verified_url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        data = response.json()
        if data["code"] != "Ok":
            raise Exception(f"Error {data['code']}: {data['message']}")
        return data["routes"]
    
    def get_table(self, locations:list, sources:list=None, destinations:list=None)->list:
        url = f"{self.osrm_url.removesuffix('/')}/table/{self.version}/{self.profile}/"
        url += f";".join([f"{location['lng']},{location['lat']}" for location in locations])
        if sources or destinations:
            url += "?"
        if sources:
            url += f"sources={';'.join([str(source) for source in sources])}"
        if destinations:
            if sources:
                url += "&"
            url += f"destinations={';'.join([str(destination) for destination in destinations])}"
        print(url)
        response = requests.get(url, verify=self.verified_url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        data = response.json()
        if data["code"] != "Ok":
            raise Exception(f"Error {data['code']}: {data['message']}")
        del data["code"]
        return data
    
    def get_match(
        self,
        locations:list,
        steps:bool=False,
        geometries:str="polyline",
        annotations:bool=False,
        overview:str="simplified",
        timestamps:list=None,
        radiuses:list=None
    )->list:
        url = f"{self.osrm_url.removesuffix('/')}/match/{self.version}/{self.profile}/"
        url += f";".join([f"{location['lng']},{location['lat']}" for location in locations])
        # Properties
        url += f"?steps={str(steps).lower()}"
        url += f"&geometries={geometries}"
        url += f"&annotations={str(annotations).lower()}"
        url += f"&overview={overview}"
        if timestamps:
            url += f"&timestamps={';'.join([str(timestamp) for timestamp in timestamps])}"
        if radiuses:
            url += f"&radiuses={';'.join([str(radius) for radius in radiuses])}"
        response = requests.get(url, verify=self.verified_url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        data = response.json()
        if data["code"] != "Ok":
            raise Exception(f"Error {data['code']}: {data['message']}")
        del data["code"]
        return data
    
    def get_trip(
        self,
        locations:list,
        steps:bool=False,
        annotations:bool=False,
        geometries:str="polyline",
        overview:str="simplified",
    ):
        url = f"{self.osrm_url.removesuffix('/')}/trip/{self.version}/{self.profile}/"
        url += f";".join([f"{location['lng']},{location['lat']}" for location in locations])
        # Properties
        url += f"?steps={str(steps).lower()}"
        url += f"&annotations={str(annotations).lower()}"
        url += f"&geometries={geometries}"
        url += f"&overview={overview}"
        response = requests.get(url, verify=self.verified_url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        data = response.json()
        if data["code"] != "Ok":
            raise Exception(f"Error {data['code']}: {data['message']}")
        del data["code"]
        return data
    
    def get_tile(
        self,
        x:int,
        y:int,
        zoom:int
    )->bytes:
        url = f"{self.osrm_url.removesuffix('/')}/tile/{self.version}/{self.profile}/tile({x},{y},{zoom}).mvt"
        response = requests.get(url, verify=self.verified_url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        return response.content
    
    
