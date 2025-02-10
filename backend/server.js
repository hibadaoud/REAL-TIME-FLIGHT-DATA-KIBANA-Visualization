const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
require('dotenv').config()
const User = require('./models/User');
const cors = require('cors')
const { spawn } = require('child_process');
const path = require('path');


// Initialize Express
const app = express();
app.use(bodyParser.json());
app.use(cors())

// MongoDB Connection
const MONGO_URI = process.env.MONGO_URI ;
mongoose.connect(
    MONGO_URI, 
    { 
        user: process.env.MONGO_USER,
        pass: process.env.MONGO_PASSWORD,
    }
)
.then(() => console.log('Connected to MongoDB'))
.catch(err => console.error('MongoDB connection error:', err));

// JWT Secret Key
const SECRET_KEY = process.env.SECRET_KEY;

// Validate Password Function
const validatePassword = (password) => {
    const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$/;
    return regex.test(password);
};

// Routes

// 1. Registration Endpoint
app.post('/register', async (req, res) => {
    const { email, password } = req.body;

    // Check if the user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
        return res.status(400).json({ error: 'Email already exists' });
    }

     // Validate the password
    if (!validatePassword(password)) {
        return res.status(400).json({
            error:
                'Password must be at least 8 characters long and include uppercase letters, lowercase letters, numbers, and special characters.',
        });
    }

    // Hash the password and save the user
    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = new User({ email, password: hashedPassword });

    try {
        await newUser.save();
        res.status(201).json({ message: 'User registered successfully' });
    } catch (err) {
        res.status(500).json({ error: 'Error registering user' });
    }
});

// 2. Login Endpoint
app.post('/login', async (req, res) => {
    const { email, password } = req.body;

    // Find the user
    const user = await User.findOne({ email });
    if (!user) {
        return res.status(401).json({ error: 'Invalid email' });
    }

    // Compare the password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
        return res.status(401).json({ error: 'Wrong password' });
    }

    // Generate JWT
    const token = jwt.sign({ email: user.email }, SECRET_KEY);

    // Trigger the producer
    const scriptPath = path.join(__dirname, 'producer_app.py');
    const producer = spawn('python3', [scriptPath]);
    let firstDataSent = false;
    producer.stdout.on('data', (data) => {
        console.log(`Producer stdout: ${data.toString()}`);

        // Send response after first data is produced
        if (!firstDataSent) {
            firstDataSent = true;
            res.json({ token, message: 'Login successful and producer started!' });
        }
    });

    producer.stderr.on('data', (data) => {
        console.error(`Producer stderr: ${data.toString()}`);
    });

    producer.on('close', (code) => {
        if (code === 0) {
            console.log('Producer completed successfully.');
        } else {
            console.error(`Producer exited with code ${code}`);
        }
    });

});

// 3. Middleware for Authentication
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Extract token after "Bearer "

    if (!token) return res.status(403).json({ error: 'Token is required' });

    jwt.verify(token, SECRET_KEY, (err, user) => {
        if (err) return res.status(403).json({ error: 'Invalid or expired token' });

        req.user = user; // Attach user info to the request
        next();
    });
};

// 4. Protected Endpoint
app.get('/dashboard', authenticateToken, (req, res) => {
    res.json({ message: 'Welcome to the dashboard!', user: req.user });
});

// Route to trigger Kafka producer
app.post('/start-producer', (req, res) => {
    const scriptPath = path.join(__dirname, 'producer_app.py');

    // Start the producer script
    const producer = spawn('python3', [scriptPath]);

    let firstDataSent = false;

    producer.stdout.on('data', (data) => {
        console.log(`Producer stdout: ${data.toString()}`);

        // Check for the first data success signal
        if (!firstDataSent) {
            firstDataSent = true; // Ensure this block runs only once
            res.status(200).json({ message: 'Producer started successfully!' });
        }
    });

    producer.stderr.on('data', (data) => {
        console.error(`Producer stderr: ${data.toString()}`);
    });

    producer.on('close', (code) => {
        if (code !== 0) {
            console.error(`Producer exited with code ${code}`);
            if (!firstDataSent) {
                return res.status(500).json({ message: `Producer failed with code ${code}` });
            }
        }
        console.log('Producer process completed.');
    });
});

// Start Server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});