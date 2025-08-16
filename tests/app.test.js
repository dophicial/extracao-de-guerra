const request = require('supertest');
const app = require('../src/app');

describe('GET /search/:cpf', () => {
  it('returns stub data with the requested CPF', async () => {
    const res = await request(app).get('/search/12345678900');
    expect(res.status).toBe(200);
    expect(res.body).toEqual(expect.objectContaining({ cpf: '12345678900' }));
  });
});
