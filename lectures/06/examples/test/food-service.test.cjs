const test = require('node:test');
const assert = require('node:assert/strict');
const { createFoodModel } = require('../src/models/food-model.cjs');
const { createFoodService } = require('../src/services/food-service.cjs');

test('rejects a blank name', async () => {
  const service = createFoodService(createFoodModel());
  await assert.rejects(service.addFood({ name: '  ' }), { status: 400 });
});

test('trims names and stores the created food', async () => {
  const service = createFoodService(createFoodModel());
  const created = await service.addFood({ name: '  Campus Rice  ' });
  assert.deepEqual(created, { id: 2, name: 'Campus Rice' });
  assert.deepEqual(await service.getFood(created.id), created);
  assert.equal((await service.listFoods()).length, 2);
});

test('rejects invalid ids and distinguishes absent resources', async () => {
  const service = createFoodService(createFoodModel());
  for (const id of [NaN, 0, -1, 1.5, Infinity, Number.MAX_SAFE_INTEGER + 1]) {
    await assert.rejects(service.getFood(id), { status: 400 });
  }
  await assert.rejects(service.getFood(999), { status: 404 });
});

test('rejects missing and non-string names', async () => {
  const service = createFoodService(createFoodModel());
  for (const input of [undefined, null, {}, { name: 1 }, { name: [] }]) {
    await assert.rejects(service.addFood(input), { status: 400 });
  }
});

test('returned objects cannot mutate the in-memory model', async () => {
  const model = createFoodModel();
  const food = await model.findById(1);
  food.name = 'changed';
  const foods = await model.findAll();
  foods[0].name = 'changed again';
  assert.equal((await model.findById(1)).name, 'Campus Noodles');
});
