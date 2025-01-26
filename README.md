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

---

## 📌 Project Overview  

### 📚 Background:
This project, developed by Hiba Daoud & Saad Raza as part of their academic work at the University of Trento, implements a **Real-Time Flight Data Visualization Dashboard** that provides an interactive interface to monitor live flight data. It integrates multiple services for data fetching, processing, storage, and visualization, ensuring scalability and modularity. The dashboard displays real-time data from **external APIs**, processed and stored using a robust pipeline involving **Kafka**, **Pyspark**, **MongoDB**, and **Elasticsearch**, and visualized in **Kibana**. Authentication is managed via a secure **Node.js** backend, and the system is deployed in Docker containers for easy orchestration and scalability.

---

## **Project Requirements**

### **Layered Architecture Implementation**:
The project must implement these layers: 
1. **Data Layer**:    
2. **Adapter Layer**:   
3. **Business Logic Layer**:   
4. **Process-Centric Layer**:
5. **Visualization Layer**
6. **Authetication Systm**

### **General Design Principles**
- **Modular and Scalable Services**: Designed for reusability and easy scaling across different environments.  
- **API-Based Communication**: Services interact exclusively through **REST APIs** for standardized communication.  
- **Internal and External Integration**: Incorporates external flight data APIs and internal data processing and visualization components.  

### **Defined Data Structures**
Inputs and outputs for services are JSON-based, with clear schema definitions provided for external and internal data exchanges.

### **Use of a Database  Management  System **

### **Deployment**
- Entire system is containerized using **Docker** for consistency, scalability, and portability.
- Deployment ensures real-time data processing and visualization with seamless user interaction.


## 🗝️ Key Features

This project incorporates multiple technologies and services to provide a robust and scalable solution for real-time flight tracking and data visualization. Below are the key features of the project:

### ✈️ Real-Time Flight Data Processing
- **Kafka Integration:** A Kafka producer-consumer system is used for streaming real-time flight data from an **external API**
- **PySpark:** Consumes flight data from Kafka in real-time, processes and transforms the data for meaningful insights.
- **Elasticsearch Integration:** Stores processed data in Elasticsearch for fast querying and retrieval of flight data.

### 📊 Interactive Data Visualization
- **Kibana Dashboard:** Displays real-time flight data, airports details, and aircafts statistics.

### 🌐 Interactive Web Application 
- **Dynamic Dashboard:** Embedded Kibana dashboard using an iframe for real-time data visualization.
- **User Authentication:** Secure login and registration system with token authorization. User-related data are stored in **MongoDB**

### 🏗️ Microservices Architecture 
- **Process-Centric API:** Coordinates user-triggered actions, such as data fetching.
- **RESTful APIs:** Enables interaction between services through clearly defined endpoints.
- **Reusable and Scalable:** Each service is modular and can be extended for other use cases.

### 🐳 Containerized Deployment
- **Dockerized Services:** All services are containerized for portability and scalability.
- **Container Orchestration:** Docker Compose manages service dependencies and networking.

---

## 🛠️ **Technologies Used**

| **Layer**                | **Technology**        | **Purpose**                                                                 |
|--------------------------|-----------------------|-----------------------------------------------------------------------------|
| **Data Layer**           | MongoDB              | Stores structured and processed flight data.                               |
|                          | Elasticsearch        | Indexes data for visualization in Kibana.                                 |
| **Adapter Layer**        | Kafka                | Acts as a message broker for real-time data streaming.                     |
| **Business Logic Layer** | PySpark              | Processes, transforms, and enriches real-time flight data.                 |
| **Process-Centric Layer**| Node.js (Express)    | Handles user-triggered actions and coordinates API interactions.           |
| **Frontend**             | HTML, CSS, JS        | Builds the web interface for user authentication and dashboard integration.|
| **Visualization**        | Kibana               | Provides real-time data visualization on flight information.               |
| **Containerization**     | Docker               | Manages services in isolated and consistent environments.                  |
