const express = require('express');

const app = express();
app.use(express.json());

// Placeholder search endpoint
app.get('/search/:cpf', async (req, res) => {
  const { cpf } = req.params;
  // TODO: integrate with Directd API using environment variables for credentials.
  // For now, respond with sample data to allow tests to run without external calls.
  res.json({
    cpf,
    nome: 'Fulano de Tal',
    renda: 1000,
  });
});

module.exports = app;
