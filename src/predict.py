import sys 
import os
import pandas as pd
from LoggingModule.exception import CustomException
from LoggingModule.logger import logging
import pickle

def load_object(file_path):
    try:
        with open(file_path, "rb") as obj :
            return pickle.load(obj)
    except Exception as e:
        logging.info("exception occured in loading object!")
        raise CustomException(e, sys)
    
    
class PredictPipeline:
    def __init__(self) -> None:
        pass

    def predictpipeline(self,model_name,features):
        try:
            model_file_path = os.path.join("models", "model.pkl")
            preprocessor_file_path = os.path.join("models", "preprocessor.pkl")
            model = load_object(model_file_path)
            preprocessor = load_object(preprocessor_file_path)

            data_scaled = preprocessor.transform(features)
            pred = model[model_name].predict(data_scaled)
            return pred
            
        except Exception as e:
            logging.info("ecception occured in prediction")
            raise CustomException(e,sys)

class custom_data:
    def __init__(self, state:float,
                 month : float,
                 co : float,
                 no2 : str,
                 pm10 : float,
                 pm25 : str,
                 so2 : str,) -> None:
        self.state = state
        self.month = month
        self.co = co
        self.no2 = no2
        self.pm10 = pm10
        self.pm25 = pm25
        self.so2 = so2

    def get_data_as_dataframe(self):
        try:
            data = {'State' : [self.state],
                    'Month':[self.month], 
                    'co µg/m³':[self.co],
                    'no2 µg/m³' : [self.no2], 
                    'pm10 µg/m³' :[self.pm10], 
                    'pm25 µg/m³':[self.pm25], 
                    'so2 µg/m³':[self.so2]}
            df = pd.DataFrame(data )
            logging.info("dataframe Gathered")
            return df
        except Exception as e:
            logging.info("Exception occured in prediction pipline")
            raise CustomException(e,sys)