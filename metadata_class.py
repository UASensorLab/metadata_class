class Study:
    def __init__(self, investigator_id: int, 
                 study_id: int, 
                 PI: str=None, 
                 title: str=None, 
                 description: str=None, 
                 location_ids: list=None, 
                 sensor_ids: list=None, 
                 start_date: str=None):
        
        self.investigator_id = investigator_id
        self.PI = PI
        self.study_id = study_id
        self.title = title
        self.description = description
        self.location_ids = {}
        self.sensor_ids = {}
        self.start_date = start_date

        if location_ids is not None:
            for location_id in location_ids:
                self.createLocation(location_id)

        if sensor_ids is not None:
            for sensor_id in sensor_ids:
                self.createSensor(sensor_id)

    class Location:
        def __init__(self, location_id: str, 
                     description: str=None):
            
            self.location_id = location_id
            self.description = description

    def createLocation(self, location_id: str,
                      description: str=None):
        
        if location_id in self.location_ids.keys():
            return
        else:
            self.location_ids[location_id] = self.Location(location_id, description)
            return self.location_ids[location_id]

    class Sensor:
        def __init__(self, sensor_id: str, 
                     unit: dict=None, 
                     description: dict=None, 
                     sampling: str=None):
            
            self.sensor_id = sensor_id
            self.unit = unit
            self.description = description
            self.sampling = sampling

    def createSensor(self, sensor_id: str,
                     unit: dict=None,
                     description: dict=None, 
                     sampling: str=None):
        
        if sensor_id in self.sensor_ids.keys():
            return
        else:
            self.sensor_ids[sensor_id] = self.Sensor(sensor_id, unit, 
                                                   description, sampling)
            return self.sensor_ids[sensor_id]

def main():

    mystudy = Study(100, 101, PI="John", title="title", description="description", sensor_ids=["sensor"], start_date="11.12.23", location_ids=["location1", "location2"])
    print(mystudy.sensor_ids["sensor"].location_id)

if __name__ == "__main__":
    main()
