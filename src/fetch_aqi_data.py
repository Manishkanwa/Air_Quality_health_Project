import pandas as pd
import requests as req
import sys, os
import json
import time
from LoggingModule.logger import logging
from LoggingModule.exception import CustomException
 
class Get_locations:
    def __init__(self):
        self.base_url = "https://api.openaq.org/v3/locations?limit=1000&page="
        self.header = {"X-API-Key" : "42d38676e3881aa6c8105ddd703c301ec72faad3c6ca3fab3c93dd9fff7c3af1"}
        self.cities = ['Delhi', 'Mumbai', 'Kolkata', 'Bengaluru', 'Chennai', 'Indore']
        
    def fetch_locations_data(self):
        try:
            page = 1
            location_raw = []
            
            logging.info('fetching location data from api.')
        
            while True:
                logging.info(f'Hitting the api for {page} time')
                url = f'{self.base_url}{page}'
                response = req.get(url, headers=self.header)
                
                data = response.json()
                location_meta = data.get('meta', [])
                location_data_temp = data.get('results', [])
                
                if location_data_temp == []:
                    break
                else:
                    if response.status_code == 200:
                        for city in location_data_temp:
                            if city['country']['id'] == 9:
                                location_raw.append(city)
                                
                    else:
                        logging.info(f"Error:  response.status_code response.text")
                        
                page+=1
            logging.info('Raw data fetched successfully.')
            return location_raw   
            
        except Exception as e :
            logging.info("error during fetching location from the api")
            raise CustomException(e, sys)   
        
    def Get_locations_dataframe(self):
        location_raw = self.fetch_locations_data()
        try:
            logging.info('Processing Raw data')
            sub_location_raw = []
            logging.info('Get subset of cities chosen from raw data.')
            for location in location_raw:
                for city in self.cities:
                    if city in location['name']:
                        sub_location_raw.append(location)

            logging.info('Getting important location info in Datafram')
            location_df = []
            for location in sub_location_raw:
                id = location['id']
                try:
                    area = location['name'].split(' - ')[0].split(', ')[0]
                except:
                    area = location['name'].split(' - ')[0].split(': ')[0]
                    
                try:
                    city = location['name'].split(' - ')[0].split(', ')[1]
                except:
                    try:
                        city = location['name'].split(' - ')[0].split(': ')[1]
                    except:
                        city = 'Mumbai'
                    
                latitude = location['coordinates']['latitude']
                longitude = location['coordinates']['longitude']
                location_df.append([id, area, city, latitude, longitude])
                
            location_df = pd.DataFrame(location_df, columns=['Location_id', 'Area','City', 'Latitude', 'Longitude'])
            logging.info('Location DataFrame succefully created')
            logging.info('Now getting sensors information for locations')
            sensor_df = []
            listed_params = [1, 2, 3, 5, 6, 7, 8, 9]
            for city in sub_location_raw:
                sensor =  city['sensors']
                for value in sensor:
                        if value['parameter']['id'] in listed_params :
                            location_id = city['id']
                            sensor_id = value['id']
                            name = value['parameter']['displayName']
                            sensor_df.append([location_id, sensor_id, name])
                        
            sensor_df = pd.DataFrame(sensor_df, columns= ['Location_id', 'Sensor_id','Sensor_name'])
            location_sensors_data = location_df.merge(sensor_df, how = 'left', on = ['Location_id','Location_id'])
            
            location_sensors_data = location_sensors_data[['Location_id', 'Sensor_id', 'Area', 'City', 'Sensor_name',	'Latitude', 'Longitude']]
            
            logging.info('Dataframe successfully merged.')
            logging.info('saving file')
            location_sensors_data.to_csv(os.path.join('data','loaction_sensors.csv'))
            logging.info('save complete')
        except Exception as e:
            logging.info('Error in Processing raw data')
            
    