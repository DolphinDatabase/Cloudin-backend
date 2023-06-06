FROM python:3.11-bullseye
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "flask" ]
CMD [ "run","--host=0.0.0.0","--port=5000"]

# docker logout

# docker build -t midall-backend-api5:1.1.3 .

# docker tag midall-backend-api5:1.1.3 dolphindatabase/midall-backend-api5:1.1.3

# docker login 

# docker push dolphindatabase/midall-backend-api5:1.1.3

# docker run -p 8080:8080 midall-backend-api5:1.1.3