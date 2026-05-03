import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

PROJECT_NAME = "src"

files = [
    # Source — config
    f"{PROJECT_NAME}/__init__.py",
    f"{PROJECT_NAME}/config/__init__.py",
    f"{PROJECT_NAME}/config/configuration.py",
    # Source — entity
    f"{PROJECT_NAME}/entity/__init__.py",
    f"{PROJECT_NAME}/entity/config_entity.py",
    # Source — constants
    f"{PROJECT_NAME}/constants/__init__.py",
    # Source — utils
    f"{PROJECT_NAME}/utils/__init__.py",
    f"{PROJECT_NAME}/utils/common.py",
    f"{PROJECT_NAME}/utils/logger.py",
    f"{PROJECT_NAME}/utils/exception.py",
    f"{PROJECT_NAME}/utils/github_issue.py",
    # Source — components
    f"{PROJECT_NAME}/components/__init__.py",
    f"{PROJECT_NAME}/components/data_ingestion.py",
    f"{PROJECT_NAME}/components/data_validation.py",
    f"{PROJECT_NAME}/components/data_transformation.py",
    f"{PROJECT_NAME}/components/prepare_base_model.py",
    f"{PROJECT_NAME}/components/model_trainer.py",
    f"{PROJECT_NAME}/components/model_evaluation.py",
    f"{PROJECT_NAME}/components/gradcam.py",
    f"{PROJECT_NAME}/components/uncertainty.py",
    f"{PROJECT_NAME}/components/report_generator.py",
    f"{PROJECT_NAME}/components/drift_detector.py",
    # Source — pipeline stages
    f"{PROJECT_NAME}/pipeline/__init__.py",
    f"{PROJECT_NAME}/pipeline/stage_01_data_ingestion.py",
    f"{PROJECT_NAME}/pipeline/stage_02_data_validation.py",
    f"{PROJECT_NAME}/pipeline/stage_03_data_transformation.py",
    f"{PROJECT_NAME}/pipeline/stage_04_prepare_base_model.py",
    f"{PROJECT_NAME}/pipeline/stage_05_model_training.py",
    f"{PROJECT_NAME}/pipeline/stage_06_model_evaluation.py",
    f"{PROJECT_NAME}/pipeline/prediction_pipeline.py",
    # Config files
    "config/config.yaml",
    "params.yaml",
    "dvc.yaml",
    ".env.example",
    # FastAPI backend
    "api/__init__.py",
    "api/main.py",
    "api/Dockerfile",
    "api/routes/__init__.py",
    "api/routes/predict.py",
    "api/routes/history.py",
    "api/routes/feedback.py",
    "api/routes/health.py",
    "api/schemas/__init__.py",
    "api/schemas/prediction.py",
    "api/services/__init__.py",
    "api/services/model_service.py",
    "api/services/celery_tasks.py",
    # Streamlit frontend
    "app/__init__.py",
    "app/streamlit_app.py",
    "app/Dockerfile",
    "app/components/__init__.py",
    "app/components/upload.py",
    "app/components/heatmap_viewer.py",
    "app/components/result_card.py",
    "app/components/history_table.py",
    # Docker
    "docker/docker-compose.yml",
    "docker/docker-compose.dev.yml",
    # GitHub Actions
    ".github/workflows/ci.yml",
    ".github/workflows/cd.yml",
    ".github/workflows/retrain.yml",
    ".github/workflows/model_eval_gate.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/pull_request_template.md",
    # Tests
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_data_ingestion.py",
    "tests/test_data_validation.py",
    "tests/test_preprocessing.py",
    "tests/test_model_loading.py",
    "tests/test_prediction_pipeline.py",
    "tests/test_gradcam.py",
    "tests/test_api_endpoints.py",
    # Research notebooks
    "research/01_data_exploration.ipynb",
    "research/02_model_experiments.ipynb",
    "research/03_gradcam_analysis.ipynb",
    "research/04_error_analysis.ipynb",
    # Docs
    "docs/self_hosting.md",
    "docs/api_reference.md",
    "docs/retraining_guide.md",
    "docs/model_card.md",
    # Root level files
    "requirements.txt",
    "requirements-dev.txt",
    "setup.py",
    "Makefile",
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
    ".pre-commit-config.yaml",
    ".gitignore",
    ".dockerignore",
    "main.py",
]


def create_project_structure():
    for filepath in files:
        path = Path(filepath)

        if path.parent != Path("."):
            path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists() or path.stat().st_size == 0:
            path.touch()
            logging.info(f"Created: {path}")
        else:
            logging.info(f"Skipped (exists): {path}")


if __name__ == "__main__":
    create_project_structure()
    print("\n✅ Project structure created successfully!")
    print("📁 Next: fill in config/config.yaml and params.yaml")
