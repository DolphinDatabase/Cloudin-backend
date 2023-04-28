FROM python:3.11-bullseye
COPY ../requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY .. /app
RUN flask run --host=0.0.0.0 --port=5000
ENTRYPOINT [ "python" ]
CMD [ "-m","pytest","test/unit-test/test_google.py"]
