const { createApp } = require('./src/app.cjs');

const app = createApp({ origin: process.env.CLIENT_ORIGIN || 'http://localhost:5173' });
const port = Number(process.env.PORT || 3000);
app.listen(port, '0.0.0.0', () => {
  console.log(`Foodmap API listening on port ${port}`);
});
