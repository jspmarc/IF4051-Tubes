from __future__ import annotations
import pickle
from os.path import join as join_path
from typing import Literal, Tuple
import numpy as np

from util.constants import Constants


class PredictionService:
    __instance: PredictionService | None = None

    def __init__(
        self,
        co2_filename: str = "ts_kmeans_co2.pkl",
        temperature_filename: str = "ts_kmeans_temperature.pkl",
        humidity_filename: str = "ts_kmeans_humidity.pkl",
    ) -> None:
        """
        Load machine learning models
        """
        self.tskm_co2_model = None
        self.tskm_temperature_model = None
        self.tskm_humidity_model = None

        with open(join_path(Constants.ML_MODELS_DIR, co2_filename), "rb") as f:
            self.tskm_co2_model = pickle.load(f)
        with open(join_path(Constants.ML_MODELS_DIR, temperature_filename), "rb") as f:
            self.tskm_temperature_model = pickle.load(f)
        with open(join_path(Constants.ML_MODELS_DIR, humidity_filename), "rb") as f:
            self.tskm_humidity_model = pickle.load(f)

    @classmethod
    def get_or_create_instance(cls) -> PredictionService:
        """
        Singleton class, only one instance is allowed
        """
        instance = cls.__instance

        if instance is None:
            instance = PredictionService()
            cls.__instance = instance

        return instance

    def predict(
        self, avg_humidity: float, avg_temperature: float, avg_co2_ppm: float
    ) -> Tuple[bool, Literal["temperature", "humidity", "co2"] | None]:
        """
        Returns True if window and door should be opened, else False
        """
        # gather information about the classes
        classes = dict()
        if self.tskm_co2_model is not None:
            classes["co2"] = self.tskm_co2_model.predict(
                np.asarray(avg_co2_ppm).reshape(-1, 1)
            )
        if self.tskm_temperature_model is not None:
            classes["temperature"] = self.tskm_temperature_model.predict(
                np.asarray(avg_temperature).reshape(-1, 1)
            )
        if self.tskm_humidity_model is not None:
            classes["humidity"] = self.tskm_humidity_model.predict(
                np.asarray(avg_humidity).reshape(-1, 1)
            )

        # it's verdict time
        # co2 is the most important factor, if outside air is bad, don't fucking open the window
        if classes.get("co2", 0) == 0:
            return False, "co2"

        # outside air is fine, but do we need to open?
        if classes.get("temperature", 0) == 0:
            return True, "temperature"
        if classes.get("humidity", 0) == 0:
            return True, "humidity"

        return False, None
