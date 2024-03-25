<!-- markdownlint-disable MD022 MDO31 MD032 MD033 MD034 -->
<p align="center">
      <img src="images/logo.png">
</p>

## Members
| Team Members         | Student ID | Email                            |
| :------------------: | :--------: | :------------------------------: |
| Kevan Teo Tze Yong   |  01423044  | kevan.teo.2022@scis.smu.edu.sg   |
| Leong Yew Kit        |  01420494  | ykleong.2022@scis.smu.edu.sg     |
| Hong Yan Jie         |  01457716  | yanjie.hong.2022@scis.smu.edu.sg |
| Yu Jun Jie           |  01414236  | junjie.yu.2022@scis.smu.edu.sg   |
| Yin Qiuhao           |  01470941  | qiuhao.yin.2022@scis.smu.edu.sg  |

## Project Overview
Our project is dedicated to creating an extensive medical services website that bridges the gap between underserved communities and healthcare professionals. The main functionalities of our platform is the provision of online consultations with therapists and doctors, allowing for remote diagnosis and medical advice. Additionally, we will seamlessly integrate the Google Maps API to recommend the nearest clinics where users can obtain recommended medications or replacements. By harnessing the power of technology, our mission is to democratize healthcare, ensuring that individuals in underserved regions have cheap and easy access to essential medical guidance and support. Our goal is to empower these communities with convenient and affordable healthcare options, thereby improving their overall well-being and quality of life.


### 💉Functionalities of GetDiagnoised ⚕
1. 🤖<b>AI Symptom Checker</b>: Integrate an AI-based symptom checker to provide initial guidance before consultations. Integrating an AI-based symptom checker into healthcare systems offers the invaluable benefit of providing patients with prompt and round-the-clock access to initial healthcare guidance. This accessibility not only aids patients in assessing their symptoms but also helps alleviate the burden on healthcare facilities by streamlining the triage process. Patients can quickly determine the severity of their condition, allowing healthcare professionals to focus their attention on more critical cases.
2. 🗺<b>Clinic locator</b>: Locator function harnesses the precision of the Google Maps API, utilizing geolocation to accurately pinpoint a user's location. To maintain accuracy and relevance, it continuously updates data in real-time. This ensures that users receive current information regarding nearby clinics, pharmacies, and medication availability. Additionally, the function seamlessly integrates navigation capabilities, allowing users to obtain step-by-step directions to their selected healthcare facility or pharmacy, making the process of finding medical services and medications efficient and hassle-free.
3. 🎥<b>Remote Consultation</b>: Remote consultation through designated video call lanes" creates secure and privacy-focused spaces equipped with user-friendly technology, such as high-quality cameras and microphones. These dedicated areas facilitate remote consultations between patients and healthcare providers. The inclusion of professional support personnel ensures even technologically challenged individuals can easily connect with their providers. This innovative approach combines the convenience of telemedicine with the in-person assistance needed for a seamless remote consultation experience.

## Tech Stack
### Frontend
<a href="https://vuejs.org/" target="_blank" rel="noreferrer"> <img src="images/vue.png" alt="vuejs" width="40" height="40"/> </a>
<a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img src="images/bootstrap.png" alt="bootstrap" width="40" height="40"/></a> 
<a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="images/css.png" alt="css3" width="40" height="45"/> </a>
<a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="images/html.png" alt="html5" width="40" height="45"/> </a>
<a href="https://www.javascript.com/" target="_blank" rel="noreferrer"> <img src="images/js.png" alt="javascript" width="40" height="45"/> </a>
<a href="https://swiperjs.com/" target="_blank" rel="noreferrer"> <img src="images/swiperjs.png" alt="swiper" width="40" height="45"/> </a>


### Backend
<a href="https://firebase.google.com/" target="_blank" rel="noreferrer"> <img src="images/firebase.png" alt="firebase" width="40" height="45"/> </a>

<!-- ### Deployment -->
<!-- https://deployment.d3rfeip13ibxct.amplifyapp.com/ (We will be deploying it again as we have to deploy a separate Flask app as well) -->
<!-- It will be up soon... -->

### GitHub Repository
https://github.com/BeeeeenY/GetDiagnosed

## Setup and Guide
1. Users visit the site at https://beeeeeny.github.io/GetDiagnosed/index.html.
2. If users need quick remedies or symptom checking, they can click on the robot icon at the bottom right-hand corner to start a chat with the chatbot.
3. Users enter a prompt to initiate a conversation with the chatbot.
4. If users want to see a doctor via video, they will be prompted to log in via the login page.
5. Once logged in, the user can fill in the consultation page using the following credentials: <br>
Username: hyunbinhandsome <br>
Password: Kyongispretty@2
6. They will be directed to a list of doctors who are available and can click on the doctor they would like to see.
7. Users will be informed to be ready, as the next page will link the doctor to the patient directly.
8. After the call has ended, users will have a list of prescriptions ready for them. They can scroll down and click on "Locate Clinics" to find the closest clinic.
