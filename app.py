"""Standalone ML experiment reporting demo using Gemini on Vertex AI.

All experiment data in this repository is synthetic and was created
specifically for this public example.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from pydantic import BaseModel, Field


class ExperimentSummary(BaseModel):
    best_overall_candidate: str

    summary: str

    tradeoffs: list[str] = Field(
        description="Important performance, latency, or complexity tradeoffs."
    )

    recommendation: str

    next_experiments: list[str] = Field(
        description="Useful follow-up experiments justified by the supplied data."
    )


def require_env(name: str) -> str:
    """Return required environment configuration or fail clearly."""

    value = os.environ.get(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value


def load_experiments(path: Path) -> list[dict]:
    """Load synthetic experiment metrics."""

    if not path.exists():
        raise FileNotFoundError(
            f"Experiment file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_client() -> genai.Client:
    """Create a Vertex AI-backed Google Gen AI client."""

    project = require_env("GOOGLE_CLOUD_PROJECT")

    location = os.environ.get(
        "GOOGLE_CLOUD_LOCATION",
        "us-central1",
    )

    return genai.Client(
        vertexai=True,
        project=project,
        location=location,
        http_options=HttpOptions(
            api_version="v1",
        ),
    )


def generate_report(
    client: genai.Client,
    model: str,
    experiments: list[dict],
) -> ExperimentSummary:
    """Generate a structured comparison using only supplied metrics."""

    experiment_text = json.dumps(
        experiments,
        indent=2,
    )

    response = client.models.generate_content(
        model=model,
        contents=(
            "Analyze these synthetic machine-learning experiments.\n\n"
            f"{experiment_text}"
        ),
        config=GenerateContentConfig(
            system_instruction=(
                "You are an ML experiment reviewer. "
                "Base every conclusion only on the supplied metrics and notes. "
                "Do not invent benchmark results."
            ),
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=ExperimentSummary,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Vertex AI returned an empty response."
        )

    parsed = json.loads(response.text)

    return ExperimentSummary.model_validate(parsed)


def main() -> None:
    """Generate and print the experiment report."""

    model = require_env("VERTEX_MODEL")

    experiments = load_experiments(
        Path("experiments.json")
    )

    client = build_client()

    report = generate_report(
        client=client,
        model=model,
        experiments=experiments,
    )

    print(
        json.dumps(
            report.model_dump(),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()