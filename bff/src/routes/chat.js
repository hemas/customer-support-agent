const express = require('express');

// Create a mini Express app just for this file
// Think of it as: "I want to create routes in this file"
const router = express.Router();

const axios = require('axios');

//Python agent url - loaded from .env file
const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';
 
/** 
 *  POST /api/chat/process
 * Receives message from Vue front end
 * Validates the request
 * Forwards to PYthon AI agent
 * Return AI response back to Vue
*/

router.post('/process' , async (req, res) => {
    //Extract fields from Vue's request body
    const { message, customer_name, customer_email, provider } = req.body;

    //Validates required fields
    if (!message || !customer_email) {
        return res.status(400).json({ error: 'Message and email are required' });
    }

    try {
        // Forward request to Python agent
        const response = await axios.post(`${PYTHON_SERVICE_URL}/process`, {
        query: message,
        customer_name: customer_name,
        customer_email: customer_email
    });

    //send python's response back to Vue
    res.json(response.data);
} catch (error) {
    //If Python is down or OpenAI fails
    res.status(500).json({ error: 'Agent service unavailable '});
}
});

//Export router so index.js can use it

module.exports = router;

