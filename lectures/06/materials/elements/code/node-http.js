const http = require('http');

http.createServer((req, res) => {
  if (req.url ==='/') {
    res.write('Hello World');
  } else if(req.url === '/hello') {
    res.write('World');
  }
  res.end();
}).listen(3000);
