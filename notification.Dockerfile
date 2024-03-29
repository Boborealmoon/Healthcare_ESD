FROM python:3-slim
WORKDIR /usr/src/app
COPY notif.reqs.txt ./
RUN python -m pip install --no-cache-dir -r notif.reqs.txt
RUN pip install twilio
COPY ./notification.py ./
CMD [ "python", "./notification.py" ]