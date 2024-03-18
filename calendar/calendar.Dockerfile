FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./Clinic_calendar.py .
CMD [ "python", "./Clinic_calendar.py" ]
