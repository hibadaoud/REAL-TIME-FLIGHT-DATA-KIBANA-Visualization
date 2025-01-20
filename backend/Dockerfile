# Use the official Node.js image as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY backend/package*.json ./

# Install dependencies
RUN npm install
RUN npm install -g nodemon

# Install Python and dependencies
# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-setuptools python3-dev libssl-dev libsasl2-dev && \
    python3 -m pip install --upgrade pip --break-system-packages && \
    python3 -m pip install requests confluent_kafka python-dotenv --break-system-packages

# Copy the rest of the application files
COPY backend .
COPY kafka/producer_app.py .

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["npm", "run", "dev"]
