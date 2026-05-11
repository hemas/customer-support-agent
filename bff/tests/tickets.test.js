const request = require('supertest')
const { app, server } = require('../src/index')

describe('Tickets Routes', () => {
    test('SHould return 500 if python is not running', async () => {
        const response = await request(app).get('/api/tickets')
        expect(response.status).toBe(500)
        expect(response.body.error).toBe('Could not fetch tickets')
    })
})

afterAll(() => {
    server.close()
})