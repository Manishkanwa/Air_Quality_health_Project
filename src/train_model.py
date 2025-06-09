import pandas as pd
import numpy as np 
import os, time , sys
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, FunctionTransformer, StandardScaler
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor, plot_importance
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error as MAE, r2_score as R2, mean_squared_error as MSE
from dataclasses import dataclass
import pickle as pkl

from LoggingModule.logger import logging
from LoggingModule.exception import CustomException



def save_object(file_path, obj):
    try: 
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path,"wb") as file_obj:
            pkl.dump(obj, file_obj)
            
        
    except Exception as e:
        raise CustomException(e, sys)
    
@dataclass
class Data_config:
    data_path = os.path.join('data', 'clean_data', 'Data_pivot.xlsx')
    preprocessor_path = os.path.join('models', 'preprocessor.pkl')
    model_path = os.path.join('models', 'model.pkl')
    
    

    
class CyclicEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, max_value=12, prefix='month'):
        self.max_value = max_value
        self.prefix = prefix

    def fit(self, X, y=None):
        return self

    def transform(self, X):
         # Convert to numeric numpy array (even if it's string month names like "January")
        if isinstance(X, pd.DataFrame):
            X_array = X.iloc[:, 0].astype(float).to_numpy()
        elif isinstance(X, pd.Series):
            X_array = X.astype(float).to_numpy()
        else:
            X_array = np.array(X, dtype=float).ravel()
        radians = 2 * np.pi * X_array / self.max_value
        return np.c_[np.sin(radians), np.cos(radians)]

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            input_features = [self.prefix]
        return [f"{input_features[0]}_sin", f"{input_features[0]}_cos"]
    
    
class Data_Transformation:
    def __init__(self):
        self.data_config = Data_config()
        self.Data_pivot = pd.read_excel(self.data_config.data_path)
        self.preprocessor_path = self.data_config.preprocessor_path
        
        
    def get_transformation_object(self):
        try:
            # Column groups
            logging.info("organixing Feature")
            categorical_features = ['State']
            month_feature = ['Month']
            numerical_features = [ 'co µg/m³', 'no2 µg/m³', 'pm10 µg/m³', 'pm25 µg/m³','so2 µg/m³']
            logging.info("Establising column transformer")
            preprocessor = ColumnTransformer(
                transformers=[
                    ('state', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                    ('month', CyclicEncoder(), month_feature),
                    ('numeric',StandardScaler() ,numerical_features)
                ],
                sparse_threshold=0,
                remainder='passthrough'
            )
            
            return preprocessor
            
        except Exception as e:
            logging.info('Error in creating preprocessor')
            raise CustomException(e,sys)
        
        
    def initiate_transformation(self):
        logging.info("Initiating Data Transformation")
        
        X = self.Data_pivot.drop(columns=['Asthama_Cases', 'Bronchitis_Cases', 'Heart_attacks', 'COPD_Cases', 'Neumonia_Cases', 'Pollution_index', 'Disease_index', 'Pollution_category'])
        Asthama_Cases = self.Data_pivot[['Asthama_Cases']]
        Bronchitis_Cases = self.Data_pivot[['Bronchitis_Cases']]
        Heart_attacks = self.Data_pivot[['Heart_attacks']]
        COPD_Cases = self.Data_pivot[['COPD_Cases']]
        Neumonia_Cases = self.Data_pivot[['Neumonia_Cases']] 
        
        X_train, X_test, Asthama_train, Asthama_test, Bronchitis_train, Bronchitis_test, Heart_attacks_train, Heart_attacks_test, COPD_train, COPD_test, Neumonia_train, Neumonia_test  = train_test_split(
            X,
            Asthama_Cases, Bronchitis_Cases, Heart_attacks, COPD_Cases, Neumonia_Cases,
            test_size=0.2,
            random_state=42
            )
        
        logging.info("Getting the PreProcessor")
        
        preprocessor = self.get_transformation_object()
        logging.info("Fitting the data")
        X_train = preprocessor.fit_transform(X_train)
        X_test = preprocessor.transform(X_test)

        logging.info(f'{preprocessor}')
        logging.info("Saving the object")
        with open(self.preprocessor_path,"wb") as file_obj:
            pkl.dump(preprocessor, file_obj)
        # save_object(self.preprocessor_path, preprocessor)
        return X_train, X_test, Asthama_train, Asthama_test, Bronchitis_train, Bronchitis_test, Heart_attacks_train, Heart_attacks_test, COPD_train, COPD_test, Neumonia_train, Neumonia_test, preprocessor
        
        
        
class Model_train:
    def __init__(self):
        self.transform = Data_Transformation()
        self.config = Data_config()
        self.model_path = self.config.model_path

    
    def evaluate_model(name, model, X_test, y_test):
        y_pred = model.predict(X_test)

        rmse = np.sqrt(MSE(y_test, y_pred))
        mae = MAE(y_test, y_pred)
        r2 =  R2(y_test, y_pred)
        
        return {
            'Model': name,
            'RMSE': rmse,
            'MAE': mae,
            'R²': r2
        }
        
    
    def initiate_model_training(self):
        
        X_train, X_test, Asthama_train, Asthama_test, Bronchitis_train, Bronchitis_test, Heart_attacks_train, Heart_attacks_test, COPD_train, COPD_test, Neumonia_train, Neumonia_test, preprocessor =  self.transform.initiate_transformation()
        
        param_grid = {
            'n_estimators': [50, 100, 150],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.05, 0.1],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0]
        }

        xgb = XGBRegressor(random_state=42)
        grid_search = GridSearchCV(estimator=xgb,
                                param_grid=param_grid,
                                scoring='r2',
                                cv=5,
                                verbose=1,
                                n_jobs=-1)
        tests = [
            (Asthama_train, Asthama_test, 'Asthama_Model'),
            (Bronchitis_train, Bronchitis_test, 'Bronchitis_Model'),
            (Heart_attacks_train, Heart_attacks_test, 'Heart_Model'),
            (COPD_train, COPD_test, 'COPD_Model'),
            (Neumonia_train, Neumonia_test, 'Neumonia_Model')
        ]
        best_estimator = {}
        for y_train, y_test, name in tests:
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
            best_model.get_booster().feature_names = list(preprocessor.get_feature_names_out())
            best_score = self.evaluate_model(best_model, X_test, y_test)
            logging.info(f"Model Score : {best_score}")
            best_estimator[name] = best_model
        save_object(self.model_path, best_estimator)
