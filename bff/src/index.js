const express = require('express'); //Web Framework for Node.js - like flask for Python

const cors = require('cors'); //Allows Vue (port 5173) to talk to this server (port 3000)

const morgan = require('morgan'); //Logs every request to terminal - helps with debugging 

require('dotenv').config();

//Import Routes
const chatRoutes = require('./routes/chat');
const ticketRoutes = require('./routes/tickets')

const app = express();

const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({ origin: 'http://localhost:5173' }))
app.use(express.json());
app.use(morgan('dev'));

//Routes
app.use('/api/chat', chatRoutes);
app.use('/api/tickets', ticketRoutes);

// HEalth Check
app.get('/health', (req,res) => {
    res.json({status: 'ok' })
});

app.listen(PORT, () => {
    console.log(`BFF running on http://localhost:${PORT}`);
})

module.exports = app;
