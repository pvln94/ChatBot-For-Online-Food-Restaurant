# ChatBot-For-Online-Food-Restaurant


## Welcome to the Online Food Restaurant Chatbot repository! This chatbot is designed to assist users in navigating an online food ordering website by providing recommendations, answering FAQs, and facilitating the ordering process.

## Features

### 📌 Menu Browsing: Users can explore the restaurant's menu with detailed descriptions and prices.

### 🛒 Order Placement: The chatbot helps customers add items to their cart and guides them through the checkout process.

### ❓ FAQs Handling: Answers common questions related to delivery, payment options, and restaurant policies.

### 📍 Order Tracking: Provides real-time updates on order status.

### 🗣️ Conversational AI: Engages users in a natural conversation for an enhanced customer experience.


## Technologies Used

### Frontend: HTML, CSS, JavaScript

### Backend: Python (Flask/Django, FastAPI)

### Database: SQL

### Chatbot: Dialogflow

# Media:
## Dialogflow:
### Intent: 
![image](https://github.com/user-attachments/assets/daeac790-7011-4ece-8023-92340a014d29)

### Entity:
![image](https://github.com/user-attachments/assets/f199a246-9c10-441f-9f7c-2945a9d43aa1)

### Fullfillment:
![image](https://github.com/user-attachments/assets/d8fc8a4e-e413-4d07-ae0f-49e4c00f1f33)


## Webpage:
![image](https://github.com/user-attachments/assets/6b85338e-17db-41ee-9a97-c2bebfca1847)

![image](https://github.com/user-attachments/assets/7c1047b2-d157-4a61-b620-942fdb7b6f29)

![image](https://github.com/user-attachments/assets/edafee22-772a-406a-ac3b-fdfc54e73b38)

## Database:
![image](https://github.com/user-attachments/assets/55f043fe-339c-4b98-ae33-ac48d3adec5f)

![image](https://github.com/user-attachments/assets/9ff955af-82a0-4459-b356-95c20ac702ee)

![image](https://github.com/user-attachments/assets/264132d2-a15f-4c8e-b5f9-d3a2dc79f685)

## Coding
![image](https://github.com/user-attachments/assets/8f03d6c1-d2c6-442b-a342-f62c057c4a15)




## Usage

### Users can interact with the chatbot on the restaurant's website.

### The chatbot will guide them through menu selection, order placement, and FAQs.

### It will also provide real-time updates about their orders.





Directory structure
===================
backend: Contains Python FastAPI backend code
db: contains the dump of the database. you need to import this into your MySQL db by using MySQL workbench tool
dialogflow_assets: this has training phrases etc. for our intents
frontend: website code

Install these modules
======================

pip install mysql-connector
pip install "fastapi[all]"

OR just run pip install -r backend/requirements.txt to install both in one shot

To start fastapi backend server
================================
1. Go to backend directory in your command prompt
2. Run this command: uvicorn main:app --reload

ngrok for https tunneling
================================
1. To install ngrok, go to https://ngrok.com/download and install ngrok version that is suitable for your OS
2. Extract the zip file and place ngrok.exe in a folder.
3. Open windows command prompt, go to that folder and run this command: ngrok http 80000

NOTE: ngrok can timeout. you need to restart the session if you see session expired message.
