import pickle

from os.path import join as join_path
from collections import Counter
from util.constants import Constants


class PredictionService:
    def __init__(
        self,
        co2_filename: str="ts_kmeans_co2.pkl",
        temperature_filename: str="ts_kmeans_temperature.pkl",
        humidity_filename: str="ts_kmeans_humidity.pkl"
    ) -> None:
        """
        Load machine learning models
        """
        self.tskm_co2_model = None
        self.tskm_temperature_model = None
        self.tskm_humidity_model = None

        with open(join_path(Constants.ML_MODELS_DIR, co2_filename), 'rb') as f:
            self.tskm_co2_model = pickle.load(f)
        with open(join_path(Constants.ML_MODELS_DIR, temperature_filename), 'rb') as f:
            self.tskm_temperature_model = pickle.load(f)
        with open(join_path(Constants.ML_MODELS_DIR, humidity_filename), 'rb') as f:
            self.tskm_humidity_model = pickle.load(f)
    
    def __new__(cls) -> "PredictionService":
        """
        Singleton class, only one instance is allowed
        """
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance
    

    def predict(
        self, avg_humidity: float, avg_temperature: float, avg_co2_ppm: float
    ) -> bool:
        """
        Returns True if window and door should be opened, else False
        """
        classes = []
        if self.tskm_co2_model is not None:
            classes.append(self.tskm_co2_model.predict(avg_co2_ppm))
        if self.tskm_temperature_model is not None:
            classes.append(self.tskm_temperature_model.predict(avg_temperature))
        if self.tskm_humidity_model is not None:
            classes.append(self.tskm_humidity_model.predict(avg_humidity))
        
        print(f"{len(classes)} classes: {classes}")

        if len(classes) == 0:
            return False

        # most_common results in list[(key, value)]; get the first key
        majority_class = Counter(classes).most_common()[0][0] 
        return majority_class

        if avg_humidity >= 80 or avg_temperature >= 41 or avg_co2_ppm >= 800:
            return True

        if avg_co2_ppm >= 400 and (avg_temperature >= 31 or avg_humidity >= 65):
            return True

        # ppm < 400
        if avg_temperature >= 29 or avg_humidity >= 50:
            return True

        # temperature < 29 and ppm < 400 and humidity < 50
        return False
