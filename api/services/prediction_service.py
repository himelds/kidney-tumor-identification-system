import base64
import time
from pathlib import Path

from api.config import Settings
from api.schemas.prediction import ClassProbability, PredictionResponse
from src.config.configuration import ConfigurationManager
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.utils.logger import api_logger as logger


class PredictionService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.config_manager = ConfigurationManager()
        self.pipeline = PredictionPipeline(self.config_manager)
        logger.info("PredictionService initialized")

    def predict(self, image_path: Path) -> PredictionResponse:
        start_time = time.perf_counter()
        result = self.pipeline.predict(image_path, generate_report=False)
        inference_time_ms = (time.perf_counter() - start_time) * 1000

        gradcam_base64 = self._encode_gradcam(Path(result.overlay_path))
        probabilities = self._build_probabilities(result.probabilities)

        return PredictionResponse(
            prediction_id=result.case_id,
            predicted_class=result.predicted_class,
            confidence=result.mc_dropout_confidence,
            probabilities=probabilities,
            uncertainty_score=result.uncertainty_score,
            is_uncertain=result.is_uncertain,
            gradcam_base64=gradcam_base64,
            inference_time_ms=inference_time_ms,
            model_version=self.settings.app_version,
        )

    def _encode_gradcam(self, overlay_path: Path) -> str:
        contents = overlay_path.read_bytes()
        encoded = base64.b64encode(contents).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    def _build_probabilities(self, probs_dict: dict) -> list[ClassProbability]:
        probabilities = [
            ClassProbability(class_name=class_name, probability=float(probability))
            for class_name, probability in probs_dict.items()
        ]
        return sorted(probabilities, key=lambda item: item.probability, reverse=True)
