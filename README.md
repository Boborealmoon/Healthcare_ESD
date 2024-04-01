
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

## Frontend Application

To view the frontend application, go to [http://127.0.0.1:5173](http://127.0.0.1:5173).

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

- [Stripe](https://stripe.com/docs/api)
- [NotificationAPI](https://docs.notificationapi.com/)

## User Scenarios (Diagrams)

### Scenario 1 - Visitor Participates in Challenges

<img src="https://user-images.githubusercontent.com/73370403/230126026-079c6d4d-2bdf-4a3a-a55a-1a338ea99f99.jpg" alt="User Scenario 1 Diagram-Scenario 1A"  width="75%">

Description: When the visitor comes to the theme park, they can view active missions and participate in a challenge to earn loyalty points.

<img src="https://user-images.githubusercontent.com/73370403/230126006-527edcea-9e7d-495d-9849-c308b558ae73.jpg" alt="User Scenario 1 Diagram-Scenario 1B"  width="75%">

Description: When the visitor completes a challenge, they will then be rewarded with and notifed of additional loyalty points.

<img src="https://user-images.githubusercontent.com/73370403/230125997-472d6cda-b3ba-45f0-aa80-80c8101574da.jpg" alt="User Scenario 1 Diagram-Scenario 1C"  width="75%">

Description: If the visitor decides to redeem their loyalty points, they will be able to view possible rewards available and redeem a reward or redeem it through the purchase of a jump queue ticket.

<hr>

### Scenario 2 - Visitor wants to create a group and search for more Theme-park goers to join his group

<img src="https://user-images.githubusercontent.com/93701568/230126466-2f36ce8b-c263-49da-992e-1590630c8085.jpg" alt="User Scenario 2 Interaction Diagram-Scenario 2A"  width="75%">

Description: This Scenario shows the Visitor creating a group and thereafter creates a Broadcast Message that everyone is able to view.

<img src="https://user-images.githubusercontent.com/93701568/230126777-c92f0c74-2588-4d78-9557-d650d2018f99.jpg" alt="User Scenario 2 Interaction Diagram-Scenario 2B"  width="75%">

Description: This Scenario shows the Visitor creating a group and then joins an already Broadcasted Message.

<hr>

### Scenario 3 - Visitor wants to Purchase a Jump Queue Ticket

<img src="https://user-images.githubusercontent.com/90820000/230129315-15035d12-63dd-4fb1-b299-de90687c9887.jpg" alt="User Scenario 3 Diagram-Scenario 3A"  width="75%">

Description: If the visitor does not want to wait in line for too long, they can opt to purchase a jump queue ticket through three payment methods. Once both loyalty and promo redemption is successful, the user will be notified of it through SMS.

<img src="https://user-images.githubusercontent.com/90820000/230129379-d469fe57-bcb3-4f81-b64f-69c01bb2ab45.png" alt="User Scenario 3 Diagram-Scenario 3B"  width="75%">

Description: Once payment is successful, a new jump queue ticket will be generated and notified to the visitor through SMS and on the UI.

<img src="https://user-images.githubusercontent.com/90820000/230129444-3a10fe92-a775-41f1-b98a-c80673051127.png" alt="User Scenario 3 Diagram-Scenario 3C"  width="75%">

Description: At the point in time before the user enters the ride through queue jumping, the user will redeem their ticket and be notified that the queue ticket is redeemed through SMS and on the UI.

<hr>

## Troubleshooting

### Docker-compose build fails

1. Delete all containers, images and volumes on Docker or Purge/Delete data on Docker
2. Enter the following into your terminal:

```sh
docker-compose build
docker-compose up
```
