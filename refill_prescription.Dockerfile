FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./refill_prescription.py ./invokes.py ./amqp_connection.py ./
CMD [ "python", "./refill_prescription.py" ]