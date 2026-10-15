function createFoodModel() {
  const foods = [{ id: 1, name: 'Campus Noodles' }];
  let nextId = 2;

  async function findAll() {
    return foods.map(food => ({ ...food }));
  }

  async function findById(id) {
    const food = foods.find(food => food.id === id);
    return food ? { ...food } : null;
  }

  async function create(name) {
    const food = { id: nextId++, name };
    foods.push(food);
    return { ...food };
  }

  return { findAll, findById, create };
}

module.exports = { createFoodModel };
