FROM python:3.11-bullseye
RUN apt-get update && apt-get install -y zabbix-agent
RUN sed -i 's/Server=127.0.0.1/Server=ec2-52-87-238-138.compute-1.amazonaws.com/g' /etc/zabbix/zabbix_agentd.conf \
    && sed -i 's/Hostname=Zabbix server/Hostname=cloudin-backend/g' /etc/zabbix/zabbix_agentd.conf
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "flask" ]
CMD [ "run","--host=0.0.0.0","--port=5000"]
