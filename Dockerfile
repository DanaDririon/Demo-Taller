FROM python:3.9

COPY . .

RUN pip freeze > requeriments.txt

RUN pip install --no-cache-dir -r requeriments.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]