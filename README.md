![let_him_cook_mascotte](https://github.com/user-attachments/assets/ee802db1-0f28-4b99-911d-e3bc602049d7)

You can see the full assignment instructions in: [instructions.txt](./instructions.txt) 

# **Cooking Forum Authentication Service**

This project is a simple, secure, and containerized backend service for managing user registration and authentication for an online cooking forum. It is built with Python and the FastAPI framework.

## **Features**

* **User Registration**: New users can register with an email, password, and basic profile information
* **Stateless JWT Authentication**: Sessions are managed using JSON Web Tokens 
* **Two-Factor Authentication (2FA)**: Users can opt-in to 2FA during registration. If enabled, they will receive a One-Time Password (OTP) via email (simulated by logging to the console) to complete their login
* **API Documentation**: All endpoints are fully documented and accessible via Swagger UI and ReDoc
* **Containerized**: The service is ready to be deployed as a Docker container
* **Tested**: The project includes a suite of automated tests to ensure reliability

## **Tech Stack**

* **Backend**: Python 3.13+  
* **Framework**: FastAPI
* **ASGI**: Uvicorn
* **Testing**: pytest
* **Deployment**: Docker

## **How to Test the Service Locally**

### **Prerequisites**

* Python 3.13+  
* pip
* Docker (WSL2 has to be activated on Windows)

### **1. Clone the Repository**

`git clone https://github.com/0xLamzari/let_him_cook.git`

`cd let_him_cook`

### **2. Set Up a Virtual Environment**

#### Create the virtual environment  
`python -m venv venv`

#### Activate it  
##### On macOS/Linux:  
`source venv/bin/activate`
##### On Windows:  
`.\venv\Scripts\activate`

### **3. Install Dependencies**

Install all the required Python packages from the requirements.txt file

`pip install -r requirements.txt`

### **4. Run the Application**

You can now run the service using uvicorn (an ASGI server)

`uvicorn app.main:app`

The service will be running at http://127.0.0.1:8000

### **5. Access API Documentation**

Once the server is running, you can access the interactive API documentation (Swagger UI) at:

**http://127.0.0.1:8000/docs**

You can also find alternative documentation (ReDoc) at:

**http://127.0.0.1:8000/redoc**

## **How to Run with Docker**

The service is configured to run inside a Docker container

### **1. Build the Docker Image**

From the root directory of the project, run the following command:

`docker build -t let-him-cook . `

### **2. Run the Docker Container**

Once the image is built, you can run it as a container:

`docker run -p 8000:8000 --name let-him-cook let-him-cook`

The service will now be accessible from your host machine at `http://localhost:8000`

## **How to Run the Automated Tests**

The project uses pytest for automated testing. To run the tests, execute the following command in your terminal from the project's root directory:

`pytest -v`


### Flow without 2FA:
![giphy](https://github.com/user-attachments/assets/f7f38bca-41a7-4c5a-b882-8c57e7f31489)

### Flow with 2FA:
![giphy](https://github.com/user-attachments/assets/0a63feec-43e8-4e48-8054-bd065056f732)
