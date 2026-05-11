from pathlib import Path

from api.config import Settings
from src.config.configuration import ConfigurationManager
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.utils.logger import api_logger as logger


class ReportService:
    """Generate PDF reports for completed prediction requests."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.config_manager = ConfigurationManager()
        self.pipeline = PredictionPipeline(self.config_manager)
        logger.info("ReportService initialized")

    def generate_report(self, image_path: str, prediction_id: str) -> str:
        """Generate a PDF report and return its file path."""
        image_file = Path(image_path)
        if not image_file.exists():
            raise FileNotFoundError(f"Image file not found: {image_file}")

        result = self.pipeline.predict(
            image_file,
            case_id=prediction_id,
            generate_report=True,
        )

        logger.info("PDF report generated for prediction %s", prediction_id)
        return str(result.report_path)
