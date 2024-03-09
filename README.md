# Healthcare_ESD

This application will focus on 3 scenarios: 
1) Refill Prescription
2) Book an Appointment
3) Submit Claims

Whenever you wanna run the microservice: 
type this into command line to set DB URL:
1) [For Mac]
    export dbURL=mysql+mysqlconnector://root:root@localhost:yourMAMPSQLPort/Path

2) [For Windows]
    set dbURL=mysql://root:root@localhost/path 

<!-- to check list of dependencies -->
python -m pip freeze

<!-- Docker Build Image -->
docker build -t <your_dockerid>/filename:version ./
<!-- example -->
docker build -t <dockerid>/book:1.0 ./


<!-- View Images on Docker -->
docker images

<!-- Remove Images -->
docker rmi <image id>


To run the service, type in cmd line: 
python service_name.py