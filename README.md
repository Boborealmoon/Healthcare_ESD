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
<!-- Need to build 1 image for each microservice -->

<!-- View Images on Docker -->
docker images

<!-- Remove Images -->
docker rmi <image id>


[Docker Network]
<!-- Create a Internal Docker Network called my-net (For communication inside the network) -->
docker network create my-net

<!-- View available networks -->
docker network ls

<!-- Running the service on the network (port routing + running) -->
docker run --name book --network my-net -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/book <dockerid>/book:1.0
<!-- compare with docker run -p 5000:5000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/book <dockerid>/book:1.0 . Difference is that We no longer publish the container’s port to the host by removing the -p option. If you attempt to access the book service via http://localhost:5000/book, it will no longer work. -->
<!-- Type http://book:5000/book for the Book service URL and press Enter -to access the items inside -->

[Docker Compose]
1) Create compose.yaml file 
<!-- version: "3.8"

services:

  #################################
  # Book: The Book microservice
  #################################
  book:
    image: <dockerid>/book:1.0
    restart: always
    environment:
      dbURL: mysql+mysqlconnector://is213@host.docker.internal:3306/book


  ###############################################
  # callbook: The test_invoke_http.py program
  ###############################################
  callbook:
    image: <dockerid>/callbook:1.0
    depends_on:
      - book
    environment:
      bookURL: http://book:5000/book -->


2) Running application with Compose 
docker compose up 
<!-- By default, docker compose looks for the compose file named compose.yaml in the current folder. Use -f, --file FILE to specify an alternate compose file
 -->
 <!-- A container named docker-book-1 is created. It joins the docker_default network under the name book. 
The postfix 1 indicates the instance of the container. 
 -->

3) docker compose ps -a 
<!-- You will see the state of the 2 containers. In this case, book is still running while callbook has stopped.
 -->

4) Stopping the services 
docker compose down



To run the service, type in cmd line: 
python service_name.py