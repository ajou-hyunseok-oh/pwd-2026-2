const express = require('express');

function createFoodRouter(controller) {
  const router = express.Router();
  router.get('/', controller.list);
  router.get('/:id', controller.get);
  router.post('/', controller.create);
  return router;
}

module.exports = { createFoodRouter };
