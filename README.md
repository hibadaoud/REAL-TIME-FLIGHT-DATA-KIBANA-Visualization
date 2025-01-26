#  **Real-Time Flight Data Visualization Dashboard** 

## 📖 **Table of Contents**
- [📌 Project Overview](#-project-overview)
- [🔑 Key Objectives](#-key-objectives)
- [🛠️ Technologies Used](#-technologies-used)
- [🏛️ Architecture](#-architecture)
- [📜 Data](#-data)
- [🧠 Model](#-model)
   - [🗂️ Data Annotation: Transformation to COCO Format](#️-data-annotation-transformation-to-coco-format)
   - [🧠 Model Architecture](#-model-architecture)
- [🔗 Model Integration](#-model-integration) 
- [🛠️ Node.js Express Backend](#️-nodejs-express-backend)
- [📱 Flutter Application](#️-flutter_application)
- [🐳 Dockerization](#-dockerization)  
- [☁️ Deployment Using Terraform](#-deployment-using-terraform)
- [📱 Results: Application interfaces](#-results-application-interfaces)
- [🔧 Setup and usage](#-setup-and-usage)
- [🔮 Future Considerations](#-future-considerations)
- [👨‍💻 Project By](#-project-by)


## 📌 Project Overview  

This project, developed by Hiba Daoud and Saad Raza as part of their academic journey at the University of Trento, delivers a **Real-Time Flight Data Visualization Dashboard** offering an interactive platform to monitor live flight data, airport details, and aircraft statistics.

### **Project Requirements**

- **Layered Architecture Implementation**:
    - Data Layer    
    - Adapter Layer  
    - Business Logic Layer   
    - Process-Centric Layer
    - Visualization Layer
    - Authentication System

- **General Design Principles:**
    - **Modular** and **Scalable** services designed for reusability and easy scaling across different environments.  
    -  Services interact exclusively through **REST APIs** for standardized communication.  
    - **Internal and External Integration**: Incorporates external flight data API and internal data processing and visualization components.  

- **Defined Data Structures**:
   - Inputs and outputs for services are JSON-based, with clear schema definitions provided for external and internal data exchanges.

- **Use of a Database Management System**

- **Deployment**
    - Entire system is containerized using **Docker** for consistency, scalability, and portability.
    - Deployment ensures real-time data processing and visualization with seamless user interaction.


## 🗝️ Key Features

### ✈️ Real-Time Flight Data Processing
- **Kafka Integration:** A Kafka producer-consumer system is used for streaming real-time flight data from an **external API: Airlabs Data API** 
- **PySpark Consumer:** Consumes flight data from Kafka in real-time, processes and transforms the data for meaningful insights.
- **Elasticsearch Integration:** Stores processed data in Elasticsearch for fast querying and retrieval of flight data.

### 📊 Interactive Data Visualization
- **Kibana Dashboard:** Displays real-time flight data, airports details, and aircafts statistics.

### 🌐 Interactive Web Application 
- **User Authentication:** Secure login and registration system with **token authorization**. User-related data are stored in **MongoDB**
- **Dynamic Dashboard:** Embedded Kibana dashboard using an iframe for real-time data visualization.

### 🏗️ Microservices Architecture 
- **Process-Centric API:** Coordinates user-triggered actions, such as data fetching.
- **RESTful APIs:** Enables interaction between services through clearly defined endpoints.
- **Reusable and Scalable:** Each service is modular and can be extended for other use cases.

### 🐳 Containerized Deployment
- **Dockerized Services:** All services are containerized for portability and scalability.
- **Container Orchestration:** Docker Compose manages service dependencies and networking.

## 🛠️ **Technologies Used**

| **Technology**        | **Purpose**                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Kafka                 | Acts as a message broker for real-time data streaming.                     |
| PySpark               | Processes, transforms, and enriches real-time flight data.                 |
| Elasticsearch         | Indexes processed data for visualization in Kibana.                        |
| Kibana                | Provides real-time data visualization on a Dashboard.              |
| Node.js (Express)     | Handles user authentication and user-triggered actions.           |
| MongoDB               | Stores user credentials.                               |
| HTML, CSS, JS         | Builds the web interface.                                                   |
| Docker                | Manages services in isolated and consistent environments.                  |

## 🏛️ Architecture

The web application incorporates **JWT-based authentication** for secure user authorization, with user credentials securely stored in **MongoDB**. Upon successful login, a **Kibana dashboard** is displayed, presenting **real-time flight data** retrieved from the **Airlabs API**, which offers extensive information on air traffic and airport density.

The data flow begins with a **Kafka producer**, which transmits the flight data to a topic named `flight`. For data processing, **Apache Spark** subscribes to the `flight` topic, retrieves the data, processes it, and sends the results to **Elasticsearch**, where it is stored in the `esflight` index. 

The **Kibana dashboard** is used to visualize the processed data in real time with precision. This dashboard is seamlessly embedded within the web application, providing users with a unified and interactive experience.

#### **1. Data Layer**  
Manages and stores persistent data:
- **MongoDB**: Handles user authentication data (email, password, tokens).  
- **Elasticsearch**: Stores and queries processed real-time flight data visualized in Kibana.

#### **2. Adapter Layer**  
Connects external API with internal systems:
- **Kafka**: Ingests and distributes real-time flight data.  
- **Python Requests**: Fetches data from **Airlabs Data APIs** and sends it to Kafka for processing.

#### **3. Business Logic Layer**  
Manages core functionality and processing:
- **Pyspark**: Processes real-time flight data from Kafka, transforms it and indexes it into Elasticsearch.  
- **Node.js (Express)**: Implements backend logic, including user authentication.

#### **4. Process-Centric Layer**  
Coordinates user actions and system workflows:
- **Node.js (Express)**: Provides REST APIs for login, registration, fetching real-time data, and triggering producer actions.