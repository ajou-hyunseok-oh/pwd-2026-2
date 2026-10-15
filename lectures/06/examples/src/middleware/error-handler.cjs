function errorHandler(err, req, res, next) {
  if (res.headersSent) return next(err);
  const status = [400, 404, 413, 415].includes(err.status)
    ? err.status
    : 500;
  const message = status === 500 ? 'Internal server error' : err.message;
  res.status(status).json({ error: message });
}

module.exports = { errorHandler };
