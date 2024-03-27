FROM python:3-slim
# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# Set the working directory in the container
WORKDIR /usr/src/app/
# Copy the dependencies file to the working directory
COPY ./http.reqs.txt ./
# Install any dependencies
RUN python -m pip install --no-cache-dir  -r http.reqs.txt
# Copy the content of the local src directory to the working directory
# Copy the content of the local directory to the working directory
COPY ./webpage.py ./
COPY ./templates ./templates
# COPY ./templates .

# # Expose the port that Flask runs on
EXPOSE 5555
# Define the command to run your Flask application
CMD ["python", "./webpage.py"]


# FROM python:3-slim
# WORKDIR /usr/src/app
# COPY http.reqs.txt ./
# RUN python -m pip install --no-cache-dir -r http.reqs.txt
# COPY ./app.py .
# # Make port 5555 available to the world outside this container
# EXPOSE 5555
# # Define environment variables
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=5555

# CMD [ "python", "./app.py" ]

# # Run the Flask application on container startup
# CMD [ "flask", "run" ]
