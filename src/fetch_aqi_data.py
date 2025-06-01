import pandas as pd
import requests as req
import sys, os
import json
import time
from LoggingModule.logger import logging
from LoggingModule.exception import CustomException
from dotenv import load_dotenv
load_dotenv()
 
 
class Get_locations:
    def __init__(self):
        self.base_url = "https://api.openaq.org/v3/locations?limit=1000&page="
        self.header = {"X-API-Key" : os.getenv("API_KEY")}
        self.cities = ['Delhi', 'Mumbai', 'Kolkata', 'Bengaluru', 'Indore', 'Hyderabad', 'Kanpur', 'Lucknow']
        
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
                        location['city'] = city
                        sub_location_raw.append(location)

            logging.info('Getting important location info in Datafram')
            location_df = []
            for location in sub_location_raw:
                id = location['id']
                try:
                    area = location['name'].split(' - ')[0].split(', ')[0]
                except:
                    area = location['name'].split(' - ')[0].split(': ')[0]
                    
                city = location['city']
                    
                latitude = location['coordinates']['latitude']
                longitude = location['coordinates']['longitude']
                location_df.append([id, area, city, latitude, longitude])
                
            location_df = pd.DataFrame(location_df, columns=['Location_id', 'Area','City', 'Latitude', 'Longitude'])
            logging.info('Location DataFrame succefully created')
            logging.info('Now getting sensors information for locations')
            sensor_df = []
            listed_params = [1, 2, 4, 5, 6, 7, 8, 9]
            for city in sub_location_raw:
                sensor =  city['sensors']
                for value in sensor:
                        if value['parameter']['id'] in listed_params :
                            location_id = city['id']
                            sensor_id = value['id']
                            name = value['parameter']['displayName']
                            sensor_df.append([location_id, sensor_id, name])
            
            logging.info('Got all the sensors present in the location')            
            sensor_df = pd.DataFrame(sensor_df, columns= ['Location_id', 'Sensor_id','Sensor_name'])
            location_sensors_data = location_df.merge(sensor_df, how = 'left', on = ['Location_id','Location_id'])
            
            location_sensors_data = location_sensors_data[['Location_id', 'Sensor_id', 'Area', 'City', 'Sensor_name',	'Latitude', 'Longitude']]
            
            logging.info('Dataframe successfully merged.')
            logging.info('saving file')
            location_sensors_data.to_csv(os.path.join('data','location_sensors_raw.csv'), index=False)
            logging.info('save complete')
        except Exception as e:
            logging.info('Error in Processing raw data')
            

class GetMeasurements:
    def __init__(self):
        self.header = {"X-API-Key" : os.getenv("API_KEY")}
        self.dataset = []
        self.dataset_df = pd.DataFrame(self.dataset, columns=['Sensor_id', 'Value', 'DateTimeFrom', 'DateTimeTo'])
        self.dataset_df.to_csv(os.path.join('data','measeurments.csv'),index=False)
        
        
    def get_sensors_inrange(self, location_sensor_data : pd.DataFrame) :
        df_inrange = pd.DataFrame(columns=[location_sensor_data.columns])
        df_inrange.to_csv(os.path.join('data','loaction_sensors.csv'),mode= 'w', index=False)
        logging.info('Getting the sensors that are in date range')
        page = 0
        sensors_in_range = []
        sensors_ids = location_sensor_data['Sensor_id']
        logging.info('Hitting the URL for sensors data this will take time')
        
        for sensor in sensors_ids:
            try:
                r = req.get(url= f'https://api.openaq.org/v3/sensors/{sensor}?limit=100&page=1',headers=self.header)
                if r.status_code == 200:
                    request = r.json()['results']
                    try:
                        year_start = int(request[0]['coverage']['datetimeFrom']['local'].split('-')[0])
                        year_end = int(request[0]['coverage']['datetimeTo']['local'].split('-')[0])
                        # print(year_start, year_end)
                        if year_start<=2020 and year_end>= 2021:
                            sensors_in_range.append(sensor)
                            df_inrange = location_sensor_data[location_sensor_data['Sensor_id'] == sensor]
                            df_inrange = df_inrange.reset_index(drop=True)
                            df_inrange.to_csv(os.path.join('data','loaction_sensors.csv'), index=False,header = False, mode = 'a')
                            logging.info(f'The {sensor} is in date range. Sensor saved')
                        else :
                            logging.info(f'The -({sensor})- not in date range')
                    except:
                        logging.info(f'Error on fetching data From : {sensor}')
                else :
                    logging.info(f"Sensor : {sensor} invalid error code : {r.status_code}")
                time.sleep(1)
            except Exception as e:
                print("error" , e)
        logging.info('Got all the usefull locations and sensors. Saved in location_sensor.csv')
        return sensors_in_range
    
    def get_measurements(self):
        logging.info('Getting location sensor data for measurments')
        location_sensor_data = pd.read_csv("data\\location_sensors_raw.csv")
        sensors_in_range = self.get_sensors_inrange(location_sensor_data)
        logging.info('Initiating measurements data collection from sensors')
        for sensor in sensors_in_range:
            self.dataset = []
            page = 1
            while True:
                try:
                    request = req.get(f'https://api.openaq.org/v3/sensors/{sensor}/measurements/daily?limit=1000&page={page}&datetimeFrom=2024-01-01&datetimeTo=2025-01-01', headers = self.header)
                    raw = request.json()
                    data = raw['results']

                    if type(raw['meta']['found']) == int :
                        try:
                            for param in data:
                                if '2020' in param['period']['datetimeFrom']['local']:
                                    self.dataset.append([sensor, param['value'], param['period']['datetimeFrom']['local'].split("T")[0], param['period']['datetimeTo']['local'].split('T')[0]])
                            logging.info(f'Data Collected from : {sensor}')
                            break
                        except:
                            continue
                    else:
                        for param in data:
                            try:
                                if '2020' in param['period']['datetimeFrom']['local']:
                                    self.dataset.append([sensor, param['value'], param['period']['datetimeFrom']['local'].split("T")[0], param['period']['datetimeTo']['local'].split('T')[0]])
                            except:
                                continue
                        page+=1
                            
                except Exception as e:
                    logging.info(f'error in fetching from sensor , {sensor}, Error : , {e}')
            self.sensor_df = pd.DataFrame(self.dataset, columns=['Sensor_id', 'Value', 'DateTimeFrom', 'DateTimeTo'])    
            self.sensor_df.to_csv(os.path.join('data','measurements.csv'), mode="a",index=False, header=False)
                
                
class Get_AQI_Data:
   def __init__(self):
       self.locator = Get_locations()
       self.measurement = GetMeasurements()
       self.locator.Get_locations_dataframe()
       self.measurement.get_measurements()                
               
                
