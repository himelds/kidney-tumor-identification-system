import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from evidently import ColumnMapping
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report

from src.utils.logger import logger


@dataclass
class DriftReport:
    drift_detected: bool
    drift_score: float
    drifted_features: list
    timestamp: str
    report_path: str


class DriftDetector:
    """
    Detects data drift between reference (training) data
    and current (production) data using Evidently AI.

    For CT scan images, we compare extracted features:
    - Mean pixel intensity
    - Standard deviation
    - Contrast (CLAHE response)
    - Brightness histogram stats
    """

    def __init__(
        self,
        reference_data_path: str,
        current_data_path: str,
        drift_threshold: float = 0.15,
        report_output_dir: str = "reports/drift",
    ):
        self.reference_data_path = Path(reference_data_path)
        self.current_data_path = Path(current_data_path)
        self.drift_threshold = drift_threshold
        self.report_output_dir = Path(report_output_dir)
        self.report_output_dir.mkdir(parents=True, exist_ok=True)

    def _load_feature_stats(self, path: Path) -> pd.DataFrame:
        """
        Load pre-extracted image feature statistics.
        These are extracted during prediction and saved as CSV.
        Columns: mean_intensity, std_intensity, contrast, brightness_p25, brightness_p75
        """
        if not path.exists():
            raise FileNotFoundError(f"Feature stats file not found: {path}")
        return pd.read_csv(path)

    def run(self) -> DriftReport:
        """Run drift detection and return a structured report."""
        logger.info("Starting drift detection...")

        reference_df = self._load_feature_stats(self.reference_data_path)
        current_df = self._load_feature_stats(self.current_data_path)

        logger.info(
            f"Reference samples: {len(reference_df)} | " f"Current samples: {len(current_df)}"
        )

        # Define which columns to monitor for drift
        column_mapping = ColumnMapping(
            numerical_features=[
                "mean_intensity",
                "std_intensity",
                "contrast",
                "brightness_p25",
                "brightness_p75",
            ]
        )

        # Run Evidently drift report
        report = Report(metrics=[DataDriftPreset()])
        report.run(
            reference_data=reference_df,
            current_data=current_df,
            column_mapping=column_mapping,
        )

        # Save HTML report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_path = self.report_output_dir / f"drift_report_{timestamp}.html"
        report.save_html(str(html_path))
        logger.info(f"Drift HTML report saved: {html_path}")

        # Extract results as dict
        result = report.as_dict()

        # Parse drift score and drifted features
        drift_score, drifted_features = self._parse_results(result)
        drift_detected = drift_score > self.drift_threshold

        logger.info(f"Drift score: {drift_score:.4f} | Threshold: {self.drift_threshold}")
        logger.info(f"Drift detected: {drift_detected}")
        if drifted_features:
            logger.warning(f"Drifted features: {drifted_features}")

        # Save JSON summary — this is what GitHub Actions will read
        json_summary = {
            "drift_detected": drift_detected,
            "drift_score": round(drift_score, 4),
            "drift_threshold": self.drift_threshold,
            "drifted_features": drifted_features,
            "reference_samples": len(reference_df),
            "current_samples": len(current_df),
            "timestamp": timestamp,
            "html_report": str(html_path),
        }

        json_path = self.report_output_dir / "drift_summary.json"
        with open(json_path, "w") as f:
            json.dump(json_summary, f, indent=2)

        logger.info(f"Drift summary JSON saved: {json_path}")

        return DriftReport(
            drift_detected=drift_detected,
            drift_score=drift_score,
            drifted_features=drifted_features,
            timestamp=timestamp,
            report_path=str(html_path),
        )

    def _parse_results(self, result: dict) -> tuple[float, list]:
        """Extract drift score and list of drifted features from Evidently result dict."""
        drifted_features = []
        drift_scores = []

        try:
            metrics = result.get("metrics", [])
            for metric in metrics:
                result_data = metric.get("result", {})

                # Dataset-level drift share
                if "dataset_drift" in result_data:
                    dataset_drift_share = result_data.get("share_of_drifted_columns", 0.0)
                    drift_scores.append(dataset_drift_share)

                # Per-feature drift
                drift_by_columns = result_data.get("drift_by_columns", {})
                for feature_name, feature_data in drift_by_columns.items():
                    if feature_data.get("drift_detected", False):
                        drifted_features.append(feature_name)

        except Exception as e:
            logger.error(f"Error parsing Evidently results: {e}")

        overall_drift_score = float(np.mean(drift_scores)) if drift_scores else 0.0
        return overall_drift_score, drifted_features
