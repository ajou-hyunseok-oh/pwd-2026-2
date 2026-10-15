function createFoodController(service) {
  async function list(req, res) {
    res.json(await service.listFoods());
  }

  async function get(req, res) {
    const food = await service.getFood(Number(req.params.id));
    res.json(food);
  }

  async function create(req, res) {
    const food = await service.addFood(req.body);
    res.status(201).location(`/foods/${food.id}`).json(food);
  }

  return { list, get, create };
}

module.exports = { createFoodController };
