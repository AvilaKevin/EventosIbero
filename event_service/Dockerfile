FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

# Cuando construya el docker ejecuta los requerimientos q se agregaron
RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", " -- host", "0.0.0.e", " -- port", "8001"]