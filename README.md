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

## 🐳 Dockerized Environment
To ensure seamless operation and management, our project is built upon a Dockerized environment, encapsulating each component of the system within its own container. This approach not only fosters a modular architecture, making it easier to update and maintain individual parts without affecting the whole system, but also enhances scalability and fault tolerance. 

Each service, from Kafka for real-time data ingestion to Kibana for insightful visualizations, operates in an isolated yet interconnected manner through a custom Docker network.

## Services
### Kakfa Integration: 
- Kafka is used as a message broker, enabling real-time data streaming. It fetches data from Airlabs API using `api_key` and distributes it for processing and visualization.
- **Services in `docker-compose.yml`**
    - **Zookeeper**: `docker.io/bitnami/zookeeper:3.8`
        - Coordinates and manages Kafka brokers.
        - Required for Kafka to function properly.
    - **Kafka**: `docker.io/bitnami/kafka:3.3`
        - Streams real-time data using topics.
        - Acts as the backbone for data ingestion and distribution.
- **Producer:** Publishes flight data fetched from the Airlabs API into a Kafka topic (flights).
    - `Producer({'bootstrap.servers': 'kafka:9093'})`: Connects the producer to Kafka inside the Docker network to publish messages to a topic. Used in `producer_app.py` because the producer is launched from the backend service, triggered by a user action. This communicates with Kafka internally within the Docker network.
    - `Producer({'bootstrap.servers': 'localhost:9092'})`: Connects the producer to Kafka outside Docker via the host's port to publish messages. Used in `producer.py` to manually test and launch the producer independently. This setup allows testing Kafka locally and running the consumer locally to observe the output of the Kafka service independently.
- **Consumer:** Subscribes to the flights topic, retrieves data, and stores it in `fetched_data.json`
    ```
        consumer = Consumer({
        'bootstrap.servers': 'localhost:9093' ,
        'group.id': 'my-group',                
        'auto.offset.reset': 'earliest'      
        })
    ```
- **Steps to Launch Kafka and retrieves data Locally**
    - Start `docker-compose.yml`:
        ```
        docker-compose up -d
        ```
    - Install Python Dependencies: In the Kafka directory, install the required Python packages:

        ```
        pip install requests confluent_kafka python-dotenv
        ```
    - In the Kafka directory, create a `.env` file with the following content:
        ```
        api_url="https://airlabs.co/api/v9/flights?api_key=<your-key>"
        ```
    - Start the Producer
        ```
        python kafka/producer.py
        ```
    - **In another terminal**, start the Consumer
        ```
        python kafka/consumer.py
        ```
        This will generate a `fetched_data.json` file containing the retrieved and processed data.

### Spark Integration: 
The Spark service processes real-time flight data retrieved from the Kafka topic, enriches it with additional information (e.g., airport names, flight types), and stores it in Elasticsearch for visualization in Kibana.

- **Services in `docker-compose.yml`**
    - **spark-master** : `hiba25/flight-dash:spark-master`
        - Custom image built from `spark/Dockerfile` to install Python dependencies, Scala, and configure Spark with specific scripts.
        - Acts as the master node of the Spark cluster.  
    - **spark-worker-1** : `hiba25/flight-dash:spark-worker-1`
        - Custom image built from `spark/Dockerfile`. Shares the same build as Spark Master for consistency.
        - Acts as a worker node to assist the master node in processing tasks.  
        - Connects to the Spark master at `spark://spark-master:7077`.

- **Steps Performed in `spark_stream.py`**
    - **Reading from Kafka:**
        - Subscribes to the Kafka topic `flights` using the broker `kafka:9092`.  
        - Consumes incoming messages in real-time.

    - **Data Enrichment:**
        - Enriches data with attributes like `type` which specify if the flight is domestic or international.  
        - Maps IATA codes (`dep_iata`, `arr_iata`) to airport details such as names and positions using `airports_external.csv` creating new fields: `Arrival`, `Departure`, `dep_pos`, `arr_pos`
        - Cleans and filters rows with missing data fields.

    - **Writing to Elasticsearch:**
        - Stores the enriched data in the Elasticsearch index `esflight`.  
        - Ensures unique records using `reg_number` as the identifier.

- **Steps to Launch Spark Locally**
    - Replace `SPARK_PUBLIC_DNS` with **your local ip** in `spark-env.sh`.
    - To see the Spark processing results independently in the console, comment out the Elasticsearch writing code and uncomment the `writeStream` section configured for console output.
    - Start `docker-compose.yml`:
        ```bash
        docker-compose up -d
        ```
    - The processed data will be printed in a table in the logs of the `spark-master` container.
        ```bash
        docker logs -f spark-master
        ```

### Elasticsearch Integration:   
Elasticsearch is responsible for storing and indexing the processed flight data to enable efficient querying and real-time visualization in Kibana. It depends on the Kafka service to retrieve processed data streams from the flights topic for indexing. This ensures persistent data storage, allowing historical data to remain accessible even when services are stopped or no new data is being ingested.
- **Docker image**: Custom image `hiba25/flight-dash:elasticsearch` built with the necessary Elasticsearch setup from `elasticsearch/Dockerfile'
-`custom_startup.sh`: Automates Elasticsearch initialization, waits for readiness, and creates the `esflight `index using `create_index_elastic.py`
-`create_index_elastic.py`: Defines and creates the esflight index with necessary mappings in Elasticsearch.
- **Steps to Launch Elasticsearch**
    - Start `docker-compose.yml`:
        ```bash
        docker-compose up -d
        ```
    - Use Elasticsearch HTTP API `localhost:9200` to query data directly or ensure data is flowing into the esflight index after Spark processing:
        ```bash
        curl -X GET "localhost:9200/esflight/_search?pretty"
        ```
    - To know how much data is stored in elasticsearch browse `http://localhost:9200/esflight/_count`
    



