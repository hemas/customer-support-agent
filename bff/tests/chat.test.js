const request = require('supertest') //makes fake http requests
const { app, server } = require('../src/index') //imports index.js file from the src folder


describe('Health Check', () => {
    test('should return status ok', async () => {
        const response = await request(app).get('/health')
        expect(response.status).toBe(200)
        expect(response.body.status).toBe('ok')
    })
})

describe('Chat Routes', () => {
    test('Should return 400 if message is missing', async() => {
        const response = await request(app)
        .post('/api/chat/process')
        .send({
            customer_name: 'John',
            customer_email: 'john@gmail.com'
        })
        expect(response.status).toBe(400)
        expect(response.body.error).toBe('Message and email are required')
    })
    test('Should return 400 if email is missing', async() => {
        const response = await request(app)
        .post('/api/chat/process')
        .send({
            message: 'I need help',
            customer_name: 'John'
        })
        expect(response.status).toBe(400)
        expect(response.body.error).toBe('Message and email are required')
    })
})

afterAll(() => {
  server.close()
})