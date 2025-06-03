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
        self.states = pd.read_json("data\\indian_location.json")
        
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
            with open (os.path.join('data','locations_raw.json') ,'w') as file:
                json.dump(location_raw, file, indent = 4) 
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
            for state in self.states:
                for city in state['districts']: 
                    for location in location_raw:
                        if city in location['name'] and location['id'] not in location_id:
                            # new_location = location.copy()
                            location['State'] = state['state']
                            sub_location_raw.append(location)
                            location_id.append(location['id'])

            logging.info('Getting important location info in Datafram')
            location_sensors_data = []
            listed_params = [1, 2, 4, 5, 6, 7, 8, 9]
            for location in sub_location_raw:
                sensors =  location['sensors']
                try:
                    area = location['name'].split(' - ')[0].split(', ')[0]
                except:
                    area = location['name'].split(' - ')[0].split(': ')[0]
                state = location['State']
                latitude = location['coordinates']['latitude']
                longitude = location['coordinates']['longitude']
                for sensor in sensors:
                    if sensor['parameter']['id'] in listed_params :
                        location_id = location['id']
                        sensor_id = sensor['id']
                        name = sensor['name']
                        location_sensors_data.append([location_id, sensor_id, state, area, name, latitude, longitude])
                        
            location_sensors_data = pd.DataFrame(location_sensors_data, columns= ['Location_id', 'Sensor_id', 'State', 'Area','Sensor_name', 'Latitude', 'Longitude'])(drop = True)
            logging.info('Location DataFrame succefully created')
            
            logging.info('Dataframe successfully merged.')
            logging.info('saving file')
            location_sensors_data.to_csv(os.path.join('data','location_sensors_raw.csv'), index=False)
            logging.info('save complete')
        except Exception as e:
            logging.info('Error in Processing raw data')
            

class GetMeasurements:
    def __init__(self):
        self.header = {"X-API-Key" : os.getenv("API_KEY")}
        self.location_sensor_data = pd.read_csv("data\\location_sensors_raw.csv")
        self.dataset = []
        self.dataset_df = pd.DataFrame(self.dataset, columns=['Sensor_id', 'Value', 'DateTimeFrom', 'DateTimeTo'])
        self.dataset_df.to_csv(os.path.join('data','measeurments.csv'),index=False)
         
    def get_sensors_inrange(self) :
        df_inrange = pd.DataFrame(columns=[self.location_sensor_data.columns])
        df_inrange.to_csv(os.path.join('data','location_sensors.csv'),mode= 'w', index=False)
        logging.info('Getting the sensors that are in date range')
        page = 0
        sensors_in_range = []
        sensors_ids = self.location_sensor_data['Sensor_id']
        logging.info('Hitting the URL for sensors data this will take time')
        start_time = time.time()
        index = 0
        track = 0
        end_time = time.time()
        sensors_in_range = []
        elapsed_time = end_time - start_time
        df_inrange = pd.DataFrame(columns=[self.location_sensor_daself.columns])
        df_inrange.to_csv('location_sensors.csv',mode= 'w', index=False)
        for sensor in sensors_ids:
            try:
                logging.info(f'{index} ', end = '')
                r = req.get(url= f'https://api.openaq.org/v3/sensors/{sensor}?limit=100&page=1',headers=self.header)
                if r.status_code == 200:
                    request = r.json()['results']
                    try:
                        year_start = int(request[0]['coverage']['datetimeFrom']['local'].split('-')[0])
                        year_end = int(request[0]['coverage']['datetimeTo']['local'].split('-')[0])
                        # print(year_start, year_end)
                        if year_start<=2020 and year_end>= 2021:
                                sensors_in_range.append(sensor)
                                df_inrange = self.location_sensor_data[self.location_sensor_data['Sensor_id'] == sensor]
                                df_inrange.to_csv(os.path.join('data','loaction_sensors.csv'), index=False,header = False, mode = 'a')
                    except:
                        logging.info('Data Not Found ')
                else :
                    logging.info(f"Sensor : {sensor} invalid error code : {r.status_code}")
            except Exception as e:
                logging.info(f"error {e}")        
            index+=1
            track += 1
            end_time = time.time()
            elapsed_time = end_time - start_time
            if track == 60 and elapsed_time < 60 :
                logging.info('Wait for :',61-elapsed_time)
                time.sleep(round(1))
                track = 0
                start_time = time.time()
        logging.info('Got all the usefull locations and sensors. Saved in location_sensor.csv')
        return sensors_in_range
    
    def get_measurements(self):
        logging.info('Getting location sensor data for measurments')
        sensors_in_range = self.get_sensors_inrange()
        logging.info('Initiating measurements data collection from sensors')
        for sensor in sensors_in_range:
            self.dataset = []
            page = 1
            while True:
                try:
                    request = req.get(f'https://api.openaq.org/v3/sensors/{sensor}/days/monthly?limit=1000&page={page}', headers = self.header)
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
               
                
