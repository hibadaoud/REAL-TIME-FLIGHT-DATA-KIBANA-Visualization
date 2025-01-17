const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');
require('dotenv').config()
const User = require('./models/User');
const cors = require('cors')

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
    res.json({ token });
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

// Start Server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
