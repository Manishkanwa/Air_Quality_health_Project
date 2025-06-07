import pandas as pd
import requests as req
import sys, os
import json
import time
from LoggingModule.logger import logging
from LoggingModule.exception import CustomException

# path to all the Data
sensors_path = os.path.join('data', 'location_sensors.csv')
measurement_path= os.path.join('data', 'measurements.csv')
cases_path = os.path.join('data', 'Disease_case.xlsx')
population_path = os.path.join('data', 'States_population.xlsx')

class Data_Cleaning:
    def __init__(self):
        self.sensors = pd.read_csv(sensors_path)
        self.measurement = pd.read_csv(measurement_path)
        self.cases = pd.read_excel(cases_path)
        self.population = pd.read_excel(population_path)
        
    def __get_aqi_category(self, pollutant, value):
        '''
        Describes the category of the pollutant level from Good To Severe.
        '''
        if pd.isnull(value) or pd.isnull(pollutant):
            return 'Unknown'
        try:
            if pollutant == 'pm25 µg/m³':
                if value <= 30: return 'Good'
                elif value <= 60: return 'Satisfactory'
                elif value <= 90: return 'Moderate'
                elif value <= 120: return 'Poor'
                elif value <= 250: return 'Very Poor'
                else: return 'Severe'
                
            elif pollutant == 'pm10 µg/m³':
                if value <= 50: return 'Good'
                elif value <= 100: return 'Satisfactory'
                elif value <= 250: return 'Moderate'
                elif value <= 350: return 'Poor'
                elif value <= 430: return 'Very Poor'
                else: return 'Severe'
                
            elif pollutant == 'no2 µg/m³':
                if value <= 40: return 'Good'
                elif value <= 80: return 'Satisfactory'
                elif value <= 180: return 'Moderate'
                elif value <= 280: return 'Poor'
                elif value <= 400: return 'Very Poor'
                else: return 'Severe'
                
            elif pollutant == 'so2 µg/m³':
                if value <= 40: return 'Good'
                elif value <= 80: return 'Satisfactory'
                elif value <= 380: return 'Moderate'
                elif value <= 800: return 'Poor'
                elif value <= 1600: return 'Very Poor'
                else: return 'Severe'
                
            elif pollutant == 'co µg/m³':
                if value <= 1: return 'Good'
                elif value <= 2: return 'Satisfactory'
                elif value <= 10: return 'Moderate'
                elif value <= 17: return 'Poor'
                elif value <= 34: return 'Very Poor'
                else: return 'Severe'
        except:        
            return 'Unknown'

    
    def __clean_data(self):
        '''Changes the data type and names  of the attributes.'''
        # Change popullation from str to float and from millions to lakhs
        try :
            self.population['Population_lakhs'] = (self.population['Population_millions'].str.split(' ').str[0]).astype(float)*10
            self.population = self.population.drop('Population_millions', axis=1)
                    
            # Change the Date time to Datetime type
            self.measurement['DateTimeFrom'] = pd.to_datetime(self.measurement['DateTimeFrom'])
            self.measurement['DateTimeTo'] = pd.to_datetime(self.measurement['DateTimeTo'])
            
            #creating a month column
            self.measurement['Month'] = self.measurement['DateTimeFrom'].dt.month_name() 
            
            # rename the vale to pulltant_value       
            self.measurement['Pollutant_value'] = self.measurement['Value']
            self.measurement = self.measurement.drop("Value", axis=1)
            
            #changing the Data types of number of cases to int
            numeric = self.cases.select_dtypes(['int64', 'float64']).columns
            self.cases[numeric] = self.cases[numeric].round().astype('int64')
        except Exception as e :
            logging.info()
            raise CustomException(e, sys)
            
        
        
        
    def merge_data(self):
        '''This function merges all the data into one tables and create a pivot table.'''   
        try:
            logging.info('Started Cleaning Process----') 
            self._Data_Cleaning__clean_data()
            
            logging.info('Cleaning Process Complete ----') 
            logging.info("Mearging Data---")
            Data = self.sensors.merge(self.population, on= 'State', how= 'left')
            Data = Data.merge(self.cases, on= 'State')
            Data = Data.merge(self.measurement, on= ['Sensor_id', 'Month'], how='left')
            Data = Data.dropna(axis=0)
            Data.loc[Data['Pollutant_value'] < 0, ['Pollutant_value']] = 0
            
            # Different pollutants have different density range so its better have the Category. 
            logging.info('Creating AQI category---')
            Data['AQI_category'] =  Data.apply(lambda X: self._Data_Cleaning__get_aqi_category(X['Sensor_name'], X['Pollutant_value']),axis= 1)
            logging.info(Data.head())
            logging.info('Creating a pivot table')
            Data_pivot = Data.pivot_table(index=['State', 'Month'],
                    columns='Sensor_name',
                    values='Pollutant_value',
                    aggfunc='mean').reset_index()
            
            Data_pivot = Data_pivot[Data_pivot['so2 µg/m³'] < 150].sort_values(by='so2 µg/m³')
            Data_pivot = Data_pivot.round(2)
            
            
            case_per_lakh = self.cases.copy()
            case_per_lakh['Asthama_Cases'] = Data['Asthama_Cases']/(Data['Population_lakhs'])
            case_per_lakh['Bronchitis_Cases'] = Data['Bronchitis_Cases']/(Data['Population_lakhs'])
            case_per_lakh['COPD_Cases'] = Data['COPD_Cases']/(Data['Population_lakhs'])
            case_per_lakh['Heart_attacks'] = Data['Heart_attacks']/(Data['Population_lakhs'])
            case_per_lakh['Neumonia_Cases'] = Data['Neumonia_Cases']/(Data['Population_lakhs'])
            Data_pivot = Data_pivot.merge(case_per_lakh, on= ["State", 'Month'], how="left")
            logging.info('Added Diseases Cases per Lakh to pivot table')
            
            Data_pivot['Pollution_index'] = Data_pivot[['co µg/m³', 'no2 µg/m³', 'pm10 µg/m³', 'pm25 µg/m³', 'so2 µg/m³']].mean(axis=1)
            Data_pivot['Disease_index'] = Data_pivot[['Asthama_Cases', 'Bronchitis_Cases', 'Heart_attacks', 'COPD_Cases', 'Neumonia_Cases']].mean(axis=1)
            logging.info('Pullution and disease index added to the pivot table')
            
            # Define correct calendar order
            month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']

            # Convert 'Month' column to categorical with the correct order
            Data_pivot['Month'] = pd.Categorical(Data_pivot['Month'], categories=month_order, ordered=True)
            
            
            logging.info('Saving Both Tables --- ')
            Data.to_excel(os.path.join('data', 'clean_data' , 'AQI_Cases_data.xlsx'), index=False)
            Data_pivot.to_excel(os.path.join('data', 'clean_data' , 'Data_pivot.xlsx'), index=False)
            logging.info('Tables Saved')
        
        except Exception as e:
            raise CustomException(e,sys)
            

