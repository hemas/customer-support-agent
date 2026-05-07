
const express = require('express'); //Web framework for Node.js

const router = express.Router(); // Adds the routes in this file to the express app

const axios = require('axios'); //THis calls the python url

//Python Agent URL - loaded from .env file
const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';

/**
 * GET /api/tickets
 * Fetch all support tickets from Python
 */
router.get('/', async(req, res) => {
    try{
        const response = await axios.get(`${PYTHON_SERVICE_URL}/tickets`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Could not fetch tickets'});
    }
});

/**
 * POST /api/tickets
 * Create a new support ticket
 */
router.post('/', async(req, res) => {
 const { message, customer_name, customer_email, provider } = req.body;
   
        if (!message || !customer_email) {
            return res.status(400).json({ error: 'Message and email are required '});
        }        
    try {
        const response = await axios.post(`${PYTHON_SERVICE_URL}/tickets`, {
        message: message,
        customer_name: customer_name,
        customer_email: customer_email,
        provider: provider
    });
    res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Could not create ticket' });
    }   
           
});

/**
 * PUT /api/tickets/:id
 * Update ticket status (open, resolved, closed)
 */
router.put('/:id', async(req, res) => {
    const { id } = req.params;
    const {status } = req.body;
    try {
        const response = await axios.put(`${PYTHON_SERVICE_URL}/tickets/${id}`, {
        status: status
    });
    res.json(response.data);
 } catch (error) {
        res.status(500).json({ error: 'could not update the ticket'});
    }
});

module.exports = router;