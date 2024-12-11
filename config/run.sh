python -m venv venv
source venv/scripts/activate
pip install -r requirements.txt
fastapi dev main.py

# Production
uvicorn main:app --host 0.0.0.0 --port 8080