# ML Experiment Reporter

A standalone Vertex AI demo that turns synthetic machine-learning
experiment metrics into a structured engineering summary.

This repository was designed and implemented specifically as a public
engineering example. It is not extracted from, adapted from, or intended
to reproduce any employer system.

## What it demonstrates

- Gemini on Vertex AI
- Google Gen AI SDK
- Application Default Credentials
- structured JSON generation
- Pydantic validation
- environment-based cloud configuration
- grounded analysis over supplied metrics
- explicit failure handling

## Flow

```text
synthetic experiment metrics
             ↓
      Gemini on Vertex AI
             ↓
     structured response
             ↓
 recommendation + tradeoffs
```

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Configure Google Application Default Credentials.

For local development, one option is:

```bash
gcloud auth application-default login
```

Then set:

```bash
export GOOGLE_CLOUD_PROJECT="YOUR-PROJECT-ID"
export GOOGLE_CLOUD_LOCATION="us-central1"
export VERTEX_MODEL="YOUR-MODEL-NAME"
```

Run:

```bash
python3 app.py
```

## Sample data

All model names, metrics, latency values, and notes included here are
synthetic and exist only for demonstration purposes.