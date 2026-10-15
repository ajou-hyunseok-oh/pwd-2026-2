function createFoodService(model) {
  async function listFoods() {
    return model.findAll();
  }

  async function getFood(id) {
    if (!Number.isSafeInteger(id) || id < 1) {
      throw Object.assign(new Error('Invalid id'), { status: 400 });
    }
    const food = await model.findById(id);
    if (!food) {
      throw Object.assign(new Error('Food not found'), { status: 404 });
    }
    return food;
  }

  async function addFood(input) {
    if (typeof input?.name !== 'string' || !input.name.trim()) {
      throw Object.assign(new Error('Name is required'), { status: 400 });
    }
    return model.create(input.name.trim());
  }

  return { listFoods, getFood, addFood };
}

module.exports = { createFoodService };
