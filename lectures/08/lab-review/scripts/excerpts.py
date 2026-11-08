"""Ordered verbatim ranges from the Week 7 lab. End markers are inclusive."""

EXCERPTS = {
    'schema': ('supabase/schema.sql', 'text', [
        ('create table', ');')]),
    'db-grants': ('supabase/schema.sql', 'text', [
        ('alter table public.restaurants', 'grant usage, select, update on sequence')]),
    'seed': ('supabase/seed.sql', 'text', [('do $$', '$$;')]),
    'db-types': ('src/types/database.types.ts', 'typescript', [
        ('export type RestaurantRow', "Partial<Omit<RestaurantRow")]),
    'dotenv': ('server.ts', 'typescript', [("import 'dotenv/config';", "import createApp")]),
    'connection': ('src/config/supabase.ts', 'typescript', [
        ('  const url =', '  const key ='),
        ('  client = createClient', '  return client;')]),
    'select': ('src/services/restaurants.service.ts', 'typescript', [
        ('  const { data, error } = await getSupabase()', '  const restaurants = (data ?? [])')]),
    'list-response': ('src/controllers/restaurants.controller.ts', 'typescript', [
        ('  const restaurants = await restaurantService.getAllRestaurants();', '  res.json({ data: restaurants });')]),
    'mapping': ('src/models/restaurant.model.ts', 'typescript', [
        ('    return new Restaurant({', '    });')]),
    'insert-row': ('src/services/restaurants.service.ts', 'typescript', [
        ('  const row: RestaurantInsert = {', '  };')]),
    'insert': ('src/services/restaurants.service.ts', 'typescript', [
        ('  // id는', '  const restaurant = Restaurant.fromDatabase(data!);', 1)]),
    'created-response': ('src/controllers/restaurants.controller.ts', 'typescript', [
        ('  const restaurant = await restaurantService.createRestaurant(payload);', '  res.status(201)')]),
    'db-error': ('src/config/supabase.ts', 'typescript', [
        ("  console.error('[Supabase]'", "  throw new HttpError(503")]),
    'write-routes': ('src/routes/restaurants.routes.ts', 'typescript', [
        ("router.post('/',", "router.post('/reset-demo',")]),
    'client-get': ('client:src/services/api.ts', 'typescript', [
        ('async function getData<T>', '}')]),
    'client-query': ('client:src/pages/ListPage.tsx', 'typescript', [
        ('  const { data, isLoading, error } = useQuery', '  });'),
        ('  const filteredData =', ': data?.data.filter')]),
}
