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

This project, developed by Hiba Daoud & Saad Raza as part of their academic work at the University of Trento, implements a **Real-Time Flight Data Visualization Dashboard** that provides an interactive interface to monitor live flight data, airport informations and aircraft informations. 

### **Project Requirements**

- **Layered Architecture Implementation**:
    1. Data Layer    
    2. Adapter Layer  
    3. Business Logic Layer   
    4. Process-Centric Layer
    5. Visualization Layer
    6. Authentication System

- **General Design Principles:**
    - **Modular and Scalable Services**: designed for reusability and easy scaling across different environments.  
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

---

## 🛠️ **Technologies Used**

| **Technology**        | **Purpose**                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Kafka                 | Acts as a message broker for real-time data streaming.                     |
| PySpark               | Processes, transforms, and enriches real-time flight data.                 |
| Elasticsearch         | Indexes processed data for visualization in Kibana.                        |
| Kibana                | Provides real-time data visualization on a Dashboard.              |
| Node.js (Express)     | Handles user authentication and user-triggered actions and coordinates API interactions.           |
| MongoDB               | Stores user credentials.                               |
| HTML, CSS, JS         | Builds the web interface.                                                   |
| Docker                | Manages services in isolated and consistent environments.                  |
