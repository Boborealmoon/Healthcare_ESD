FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./app.py .
# Make port 5555 available to the world outside this container
EXPOSE 5555
# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5555

# CMD [ "python", "./app.py" ]

# Run the Flask application on container startup
CMD [ "flask", "run" ]