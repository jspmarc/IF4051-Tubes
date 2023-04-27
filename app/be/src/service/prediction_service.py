class PredictionService:
    def predict(
        self, avg_humidity: float, avg_temperature: float, avg_co2_ppm: float
    ) -> bool:
        if avg_humidity >= 80 or avg_temperature >= 41 or avg_co2_ppm >= 1200:
            return True

        if avg_co2_ppm >= 800:
            return False

        if avg_co2_ppm >= 400 and (avg_temperature >= 31 or avg_humidity >= 65):
            return True

        # ppm < 400
        if avg_temperature >= 29 or avg_humidity >= 50:
            return True

        # temperature < 29 and ppm < 400 and humidity < 50
        return False
