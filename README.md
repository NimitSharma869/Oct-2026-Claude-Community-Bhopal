# Oct-2026-Claude-Community-Bhopal
October 2026 Hackathon Claude Community Bhopal

# How to run

## Windows (Powershell)

cd backend 

py -m venv .venv

.venv\Scripts\Activate.ps1

python -m pip install -r requirements.text

python -m cvicorn jal_drishti.api::app --port 8000

## Mac/Linux

cd backend

python3 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.text

python -m cvicorn jal_drishti.api::app --port 8000
