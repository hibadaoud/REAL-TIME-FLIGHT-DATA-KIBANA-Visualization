#  **Real-Time Flight Data Visualization Dashboard** 

## 📖 **Table of Contents**
- [📌 Project Overview](#-project-overview)
- [🔑 Key Objectives](#-key-objectives)
- [🛠️ Technologies Used](#-technologies-used)
- [🏛️ Brief Description & Architecture](#-architecture)
- [🐳 Dockerized Environment](#-dockerized-environment)
- [🔧 Setup and usage](#-setup-and-usage)
- [⚙️ Services](#-services)
- [🖥️ Results](#-results)
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
- **Authentication & Authorization System**:
    - Implement JWT-based authentication, requiring a token to access specific API endpoints.
- **Use of a Database Management System**
- **Defined Data Structures**:
   - Inputs and outputs for services are JSON-based, with clear schema definitions provided for external and internal data exchanges.
- **General Design Principles:**
    - **Modular** and **Scalable** services designed for reusability and easy scaling across different environments.  
    -  Services interact exclusively through **REST APIs** for standardized communication.  
    - **Internal and External Integration**: Incorporates external flight data API and internal data processing and visualization components.  
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

## 🏛️ Brief Description & Architecture 

The web application features **JWT-based authentication** for secure user access, with credentials safely stored in **MongoDB**. After a successful login  and using **token authorization**, users are directed to a **Kibana dashboard** that displays **real-time flight data** from the **Airlabs API**, offering detailed information on air traffic and airport density.

The data flow starts with a **Kafka producer** that publishes flight data to the `flight` topic. **Apache Spark** subscribes to this topic, processes the data, and forwards the results to **Elasticsearch**, where they are stored in the `esflight` index.

The **Kibana dashboard**, embedded directly within the web application, visualizes the processed data in real time, providing users with a seamless, interactive experience.

![Application Architecture](./img/archi.png)


#### **1. Data Layer**  
Manages and stores persistent data:
- **MongoDB**: Handles user authentication data (email,password).  
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

#### **5. Vizualization Layer**  
Presents real-time processed data to the end user through a user-friendly interface
- **Kiabana**: Visualizes real-time flight data using an interactive dashboard.
- **HTML, CSS, JS**: Builds the web interface for user authentication and embedding Kibana for real-time visualization.
- **Nginx**: Serves the frontend and routes requests to the backend.

## 🐳 Dockerized Environment
To ensure seamless operation and management, our project is built upon a Dockerized environment, encapsulating each component of the system within its own container. This approach not only fosters a modular architecture, making it easier to update and maintain individual parts without affecting the whole system, but also enhances scalability and fault tolerance. 

Each service in the system, operates in an isolated yet interconnected manner through a custom Docker network.

![Docker compose Services](./img/docker.jpg)

## 🔧 Setup and Usage
In order to see the web application with Real Time visualization Dashboard you just need to:
- create a `.env` file, in the same directory as `docker-compose.yml`,  with the following content:
    ```
    MONGO_INITDB_ROOT_USERNAME=<mongo_username>
    MONGO_INITDB_ROOT_PASSWORD=<mongo_password>
    MONGO_INITDB_DATABASE=auth_db
    MONGO_URI=mongodb://mongo:27017/auth_db?authSource=admin
    API_URL = "https://airlabs.co/api/v9/flights?api_key=<your-key>"
    ```
- In the backend directory, create a `.env` file with the following content:
    ```
    SECRET_KEY=<your secret key>
    ```
    You can obtain it executing these commands in the terminal after installing `node` from the source web page
    ```
    node
    require('crypto').randomBytes(64).toString('hex')
    ```
- Start `docker-compose.yml`:
    ```bash
        docker-compose up -d
    ```
- Access the web application via `http://localhost:8080`.
- The landing page provides navigation options to login or register.
- Upon successful login, the Kibana dashboard is displayed with Real Time data
- The button Fetch Real Time Data is used for retrieving new data when needed.

> [!NOTE]
> Note that this is only for seeing results directly but we will detail every service and its usage in the next section.

## ⚙️ Services
### Kakfa service: 
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

### Spark Service: 
The Spark service processes real-time flight data retrieved from the Kafka topic, enriches it with additional information (e.g., airport names, flight types), and stores it in Elasticsearch for visualization in Kibana.
**The Spark service communicates with Kafka and Elasticsearch services using internal APIs as they are all in the same network.**

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

### Elasticsearch service:   
Elasticsearch is responsible for storing and indexing the processed flight data to enable efficient querying and real-time visualization in Kibana. It depends on the Kafka service to retrieve processed data streams from the flights topic for indexing. This ensures persistent data storage, allowing historical data to remain accessible even when services are stopped or no new data is being ingested.
**The Spark Elasticsearch communicates with Kafka and Kibana services using internal APIs as they are all in the same network.**

- **Elasticsearch image**: Custom image `hiba25/flight-dash:elasticsearch` built with the necessary Elasticsearch setup from `elasticsearch/Dockerfile'.
- `custom_startup.sh`: Automates Elasticsearch initialization, waits for readiness, and creates the `esflight` index using `create_index_elastic.py`
-   `create_index_elastic.py`: Defines and creates the esflight index with necessary mappings in Elasticsearch.
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
    
### **Kibana Service**

Kibana serves as the **real-time data visualization** layer in this project, connecting to Elasticsearch to fetch and display processed flight data. The data is displayed in custom dashboard with insightful graphs and maps. The dashboard is embedded into the web application using an `iframe`, providing users with an interactive and seamless visualization experience.
**The Kibana service communicates with Elasticsearch and Frontend services using internal APIs as they are all in the same network.**

- **Kibana image**: Custom image `hiba25/flight-dash:kibana` built with the necessary Kiabana setup from `kibana/Dockerfile'.
- `custom_cmd.sh`:
   - Executes essential setup scripts and ensures Kibana runs smoothly.
   - Calls `load_ndjson.sh` to import the preconfigured dashboard into Kibana.
- `load_ndjson.sh`:
   - Imports saved the Kibana dashboard using the Kibana API.
   - Ensures the dashboard is available immediately after starting the Kibana container.
- `export.ndjson`:
   - Contains the exported configuration for Kibana dashboard, visualization, and saved objects.
   - Loaded into Kibana on startup to provide prebuilt visualizations.
- **Steps to Launch Kibana**
    - Start `docker-compose.yml`:
        ```bash
        docker-compose up -d
        ```
    - Browse Kibana HTTP API `localhost:5601` to visualize and interacte with data stored in Elasticsearch.
    - Go to Management > StackManagement > Kibana > Saved Objects
    - You will see Airport Managment Dashboard, click on it and vizualize the data with custom graphs
    - If not import `export.ndjson` manually.

###  Backend Service 
The backend service is **the core API for user authentication, data handling, and Kafka producer triggering.** It connects with other services, such as MongoDB for storing user credentials and Kafka for data streaming, and provides RESTful endpoints for user interactions.
- **Services Used**
    - **MongoDB** : `mongo:latest`
        - **Purpose**: Stores user authentication data (email, password, tokens).  
        - **Integration**: MongoDB is accessed via Mongoose in the `server.js` file for operations like user registration and login.
    - **Kafka**  
        - **Purpose**: Acts as the message broker for streaming flight data.  
        - **Integration**: Upon successful user login, the backend triggers the Kafka producer (`producer_app.py`) to fetch and publish real-time flight data.
    - **Node.js (Express)** `hiba25/flight-dash:backend`  
        - **Purpose**: Implements RESTful APIs for user authentication (`/register`, `/login`) and producer management (`/start-producer`).  
        - **Docker Image**: Custom image built from `backend/Dockerfile` to install Python and nodejs dependencies.
- `server.js`: Contains the API logic and middleware for authentication. It handles user authentication, token validation, and producer control.
    - **Login API**: Triggers the Kafka producer and returns a **JWT token** upon successful login.
    - **Protected API**: `/dashboard` uses JWT to allow access only to authenticated users.
- **Steps to Launch the Backend**
    - In the same directory as `docker-compose.yml`, create a `.env` file with the following content:
        ```
        MONGO_INITDB_ROOT_USERNAME=<mongo_username>
        MONGO_INITDB_ROOT_PASSWORD=<mongo_password>
        MONGO_INITDB_DATABASE=auth_db
        MONGO_URI=mongodb://mongo:27017/auth_db?authSource=admin
        API_URL = "https://airlabs.co/api/v9/flights?api_key=<your-key>"
        ```
    - In the backend directory, create a `.env` file with the following content:
        ```
        SECRET_KEY=<your secret key>
        ```
        You can obtain it executing these commands in the terminal after installing `node` from the source web page
        ```
        node
        require('crypto').randomBytes(64).toString('hex')
        ``
     - Start `docker-compose.yml`:
        ```bash
        docker-compose up -d
        ```
    - Use backend HTTP API `localhost:3000` endpoints to locally try user authentication and authorization.
        ```bash
        curl -X POST http://localhost:3000/register \
        -H "Content-Type: application/json" \
        -d '{"email": "testuser@example.com", "password": "securepassword123"}'

        curl -X POST http://localhost:3000/login \
        -H "Content-Type: application/json" \
        -d '{"email": "testuser@example.com", "password": "securepassword123"}' -o response.json

        curl -X GET http://localhost:3000/dashboard \
        -H "Authorization: Bearer <your-jwt-token>"
        ```
       `<your-jwt-token>` is stored in `response.json`

### Frontend Service 
The frontend service provides an intuitive and user-friendly web interface for the Real-Time Flight Visualization Dashboard. It enables users to interact with the application for tasks such as login, Fro, and viewing real-time flight data via the embedded Kibana dashboard.
**The Frontend service communicates with Backend services using API_URL="http://localhost:3000"**

- **Steps to Launch the Backend**
    - Start `docker-compose.yml`:
        ```bash
        docker-compose up -d
        ```
    - Access the web application via `http://localhost:8080`.

## 🖥️ Results
**Welcome Page**
![index-page](img/index.jpg)
**Sign In / Sign Up**
![login-page](img/login.jpg)
![register-page](img/register.jpg)
**Dashboard**
![dashboard-page](img/dashboard.jpg)

Let us now focus on the graphs developed during the data visualization process. We have chosen to divide our dashboard into three sections: airport information, flight information, and aircraft information.
### Airport Information
For this section of the dashboard, we focused on information useful for airport administrators, notably the total number of flights related to that airport and the flow of departures and arrivals. The figure above shows an overview for all airports, but the available filters allow selecting a specific airport.

![Airport-information](img/Airport-Information.png)

### Flight Information
For this part of the dashboard, we visualize on the map the position of aircraft, their departure and arrival airports sorted by their speeds or altitudes as needed. Then the treemaps display the most frequent flights, grouped by aircraft type and country flag, highlighting key trends such as the dominance of aircraft models like B738 and countries like the US in air traffic operations.

![Flight-information](img/Flight-information.jpeg)

### Aircraft Information
Finally, for the section related to the aircraft itself, using the data available on the API, we can determine the average and maximum speeds of aircraft as well as their speeds relative to their altitudes to ultimately identify the fastest aircraft and rank them in descending order.
![Aircraft-information](img/Aircraft-information.png)

### Filters' addition
In addition to graphics, we have developed a variety of filters that make dashboars customizable and interactive. In particular, we use a filter for the flight code, the departure or arrival, the status of the flight or its type but also the airline and the aircraft code.
The filters can be found in the dashboard header as follows:

![Filters](img/cover-filters.png)

## 🔮 Future Considerations

1. **Streamlined Data Orchestration**  
Automate the end-to-end workflow for data ingestion, processing, and storage using **Apache Airflow**. This will enable better scheduling, error handling, and task dependencies, making the pipeline more efficient and less error-prone.

2. **Scalable Deployment Architecture**  
- Leverage **Kubernetes** for container orchestration to ensure service scalability and fault tolerance. 
- Implement **CI/CD pipelines** with tools like **Jenkins** to automate testing and deployment, reducing manual effort and improving reliability.

3. **Dynamic Load Balancing**  
Introduce load balancing mechanisms to distribute traffic across multiple instances of the services dynamically. This will improve system performance and ensure stability during peak usage.

## 👨‍💻 Project by  
<a href="https://github.com/hibadaoud/hibadaoud/REAL-TIME-FLIGHT-DATA-KIBANA-Visualization/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=hibadaoud/REAL-TIME-FLIGHT-DATA-KIBANA-Visualization"/>
</a>









