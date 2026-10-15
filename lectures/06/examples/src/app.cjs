const express = require('express');
const cors = require('cors');
const { createFoodModel } = require('./models/food-model.cjs');
const { createFoodService } = require('./services/food-service.cjs');
const { createFoodController } = require('./controllers/food-controller.cjs');
const { createFoodRouter } = require('./routes/food-routes.cjs');
const { errorHandler } = require('./middleware/error-handler.cjs');

function createApp({ model = createFoodModel(), origin = 'http://localhost:5173' } = {}) {
  const app = express();
  app.use(cors({ origin }));
  app.use(express.json({ limit: '10kb' }));
  app.get('/health', (req, res) => res.json({ status: 'ok' }));
  const service = createFoodService(model);
  const controller = createFoodController(service);
  app.use('/foods', createFoodRouter(controller));
  app.use((req, res) => res.status(404).json({ error: 'Route not found' }));
  app.use(errorHandler);
  return app;
}

module.exports = { createApp };
