-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tickets table
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    query TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'open',
    sentiment VARCHAR(20),
    intent VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    ticket_id INT REFERENCES tickets(id),
    role VARCHAR(10) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge base table
CREATE TABLE IF NOT EXISTS knowledge_base (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample knowledge base data
INSERT INTO knowledge_base (category, question, answer) VALUES
('billing', 'How do I update my billing information?', 'You can update your billing information by going to Account Settings > Billing > Update Payment Method.'),
('billing', 'Why was I charged twice?', 'Double charges are usually resolved within 3-5 business days. Please contact support with your transaction ID for faster resolution.'),
('technical', 'How do I reset my password?', 'Click on Forgot Password on the login page and follow the instructions sent to your email.'),
('technical', 'The app is not loading. What should I do?', 'Try clearing your browser cache, disabling extensions, or using a different browser. If the issue persists, contact support.'),
('general', 'How do I cancel my subscription?', 'You can cancel your subscription anytime from Account Settings > Subscription > Cancel Plan.'),
('general', 'What are your support hours?', 'Our support team is available Monday to Friday, 9 AM to 6 PM EST.');
