FROM python:3-slim
#change directory
WORKDIR /usr/src/app

COPY requirements.txt ./
#download dependency
RUN python -m pip install --no-cache-dir -r requirements.txt
#copy book.py to the current directory
COPY ./book.py .
#run file
CMD [ "python", "./app.py" ]
