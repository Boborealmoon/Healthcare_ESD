
# UMS Clinic

An enterprise solution that utilises a wide range of functions through the application for clinics to utilise and engage with their patients and suppliers.

## Problem Statement

Enhancing patients' and suppliers' experiences by reducing the pains that they undergo in Clinics through providing a convenient and seamless solution.

## Team Members

- [Kevan Teo](https://www.linkedin.com/in/kevanteo/)
- [Foo See Jae](https://www.linkedin.com/in/seejaefoo/)
- [Ang Zhen Yue](https://www.linkedin.com/in/angzhenyue/)
- [Cheong Zhou Ming](https://www.linkedin.com/in/cheong-zhouming/)
- [Kenneth Lim](https://www.linkedin.com/in/kennethlimhg/)
- [Shawn Sin](https://www.linkedin.com/in/shawn-sin/)

## Requirements

- Docker Desktop v4.26.1

## Project Setup

The application has been dockerised to include MySQL, phpMyAdmin, RabbitMQ, Kong API Gateway, Frontend application and the Microservices to provide seamless set up with Docker Compose. Please ensure that your MAMP/WAMP or any MySQL database is turned **OFF**. Additionally, please ensure that port 8889 is unused.

To run the project in development environment, access the parent folder directory and run docker compose.

```sh
cd Healthcare_ESD
docker compose up
```

The application will take a few minutes to get everything set up. If the application is not working as expected, stop the terminal and run docker compose again.

```sh
docker-compose up
```

However, our microservices are still exposed publicly for ease of use in testing all the endpoints of the microservices.

## MySQL + phpMyAdmin

To view and access the database, go to [http://127.0.0.1:5013](http://127.0.0.1:5013) and enter the following credentials.

- Server Name: mysql-database
- Username: root
- Password: root

## RabbitMQ

To view and access RabbitMQ, go to [http://127.0.0.1:15672](http://127.0.0.1:15672) and enter the following credentials.

- Username: guest
- Password: guest

## Kong API Gateway

To view and access Kong API Gateway, go to [http://127.0.0.1:8002](http://127.0.0.1:8002) and enter the following credentials.

- Username: admin
- Password: adminadmin

## Front End Application

To view the front end, go to https://boborealmoon.github.io/Healthcare_ESD/templates/index.html.

## Microservices

The following are the addresses for the microservices. The respective API endpoints can be found here.

- Employees: [http://localhost:8000/api/v1/employees](http://localhost:8000/api/v1/employees)
- Inventory: [http://localhost:8000/api/v1/inventory](http://localhost:8000/api/v1/inventory)
- Patient: [http://localhost:8000/api/v1/patient](http://localhost:8000/api/v1/patient)
- Calendar: [http://localhost:8000/api/v1/calendar](localhost:8000/api/v1/calendar)
- Orders: [http://localhost:8000/api/v1/orders](http://localhost:8000/api/v1/orders)
- Appointments: [http://localhost:8000/api/v1/appointments](http://localhost:8000/api/v1/appointments)
- Emails: [http://localhost:8000/api/v1/emailservice](http://localhost:8000/api/v1/emailservice)
- Notification: [http://localhost:8000/api/v1/notification](http://localhost:8000/api/v1/notification)
- Claims: [http://localhost:8000/api/v1/claims](http://localhost:8000/api/v1/claims)

## External Microservices

- [Twilio](https://www.twilio.com/docs)
- [Kong](https://docs.konghq.com/)

## Troubleshooting

### Docker-compose build fails

1. Delete all containers, images and volumes on Docker or Purge/Delete data on Docker
2. Enter the following into your terminal:

```sh
docker-compose build
docker-compose up
```
