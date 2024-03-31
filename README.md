ESDeezknee
An immersive enterprise solution that offers a wide range of functions through the application for theme parks to utilise and engage with their visitors.

Problem Statement
Enhancing visitors' experiences by reducing the pains that visitors undergo in theme parks through providing a convenient and seamless solution.

Team Members
Ng Kang Ting
Teo Wei Lun
Keith Law
Joel Tan
Zachary Lian
Vanessa Lee
Application Preview
Application


Requirements
Docker v4.17.0
Project Setup
The application has been dockerised to include MySQL, phpMyAdmin, RabbitMQ, Kong API Gateway, Frontend application and the Microservices to provide seamless set up with Docker Compose. Please ensure that your MAMP/WAMP or any MySQL database is turned OFF. Additionally, please ensure that port 3306 is unused.

To run the project in development environment, access the parent folder directory and run docker compose.

cd ESDeezknee
docker-compose up
The application will take a few minutes to get everything set up. If the application is not working as expected, stop the terminal and run docker compose again.

docker-compose up
However, our microservices are still exposed publicly for ease of use in testing all the endpoints of the microservices.

MySQL + phpMyAdmin
To view and access the database, go to http://127.0.0.1:5013 and enter the following credentials.

Server Name: mysql-database
Username: root
Password: root
RabbitMQ
To view and access RabbitMQ, go to http://127.0.0.1:15672 and enter the following credentials.

Username: guest
Password: guest
Kong API Gateway
To view and access Kong API Gateway, go to http://127.0.0.1:1337 and enter the following credentials.

Username: admin
Password: adminadmin
Frontend Application
To view the frontend application, go to http://127.0.0.1:5173.

Microservices
The following are the addresses for the microservices. The respective API endpoints can be found in the Postman Collection.

Verification: http://127.0.0.1:6001
Notification: http://127.0.0.1:6002
Account: http://127.0.0.1:6003
Icebreaker: http://127.0.0.1:6101
Broadcast: http://127.0.0.1:6102
Group: http://127.0.0.1:6103
HandleGroup: http://127.0.0.1:6104
Order: http://127.0.0.1:6201
QueueTicket: http://127.0.0.1:6202
Payment: http://127.0.0.1:6203
Promo: http://127.0.0.1:6204
Mission: http://127.0.0.1:6300
Loyalty: http://127.0.0.1:6301
Challenge: http://127.0.0.1:6302
Reward: http://127.0.0.1:6303
Redemption: http://127.0.0.1:6304
External Microservices
Stripe
NotificationAPI
Postman Environment + Collections
To test the API endpoints of the microservices, import the following to Postman.

ESDeezknee Environment
ESDeezknee Collection
ESDeezknee API Gateway Collection
User Scenarios (Diagrams)
Scenario 1 - Visitor Participates in Challenges
User Scenario 1 Diagram-Scenario 1A

Description: When the visitor comes to the theme park, they can view active missions and participate in a challenge to earn loyalty points.

User Scenario 1 Diagram-Scenario 1B

Description: When the visitor completes a challenge, they will then be rewarded with and notifed of additional loyalty points.

User Scenario 1 Diagram-Scenario 1C

Description: If the visitor decides to redeem their loyalty points, they will be able to view possible rewards available and redeem a reward or redeem it through the purchase of a jump queue ticket.

Scenario 2 - Visitor wants to create a group and search for more Theme-park goers to join his group
User Scenario 2 Interaction Diagram-Scenario 2A

Description: This Scenario shows the Visitor creating a group and thereafter creates a Broadcast Message that everyone is able to view.

User Scenario 2 Interaction Diagram-Scenario 2B

Description: This Scenario shows the Visitor creating a group and then joins an already Broadcasted Message.

Scenario 3 - Visitor wants to Purchase a Jump Queue Ticket
User Scenario 3 Diagram-Scenario 3A

Description: If the visitor does not want to wait in line for too long, they can opt to purchase a jump queue ticket through three payment methods. Once both loyalty and promo redemption is successful, the user will be notified of it through SMS.

User Scenario 3 Diagram-Scenario 3B

Description: Once payment is successful, a new jump queue ticket will be generated and notified to the visitor through SMS and on the UI.

User Scenario 3 Diagram-Scenario 3C

Description: At the point in time before the user enters the ride through queue jumping, the user will redeem their ticket and be notified that the queue ticket is redeemed through SMS and on the UI.

Troubleshooting
Docker-compose build fails
Delete all containers, images and volumes on Docker or Purge/Delete data on Docker
Enter the following into your terminal:
docker-compose build
docker-compose up
Login Error
Please use the following account to navigate through the system:

Email: kangting.ng.2021@scis.smu.edu.sg
Password: IS213ESDeezKnee
MySQL issue when using docker compose
On your MAMP/WAMP with your mySQL
Ensure that root account password is 'root'
Enter the following into your terminal:
docker-compose -f docker-compose.local.yml build
docker-compose -f docker-compose.local.yml up
