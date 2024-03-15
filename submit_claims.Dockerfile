FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./submit_claims.py ./invokes.py ./amqp_connection.py ./
CMD [ "python", "./submit_claims.py" ]
