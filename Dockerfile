FROM python:3.11-bullseye
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "pytest" ]
CMD [ "test/unit-test/test_google.py"]
