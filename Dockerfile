FROM python:3.11-bullseye
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "flask" ]
CMD [ "run","--host=0.0.0.0","--port=5000"]