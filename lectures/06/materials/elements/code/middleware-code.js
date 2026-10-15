// 미들웨어 예시
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`); // 로깅
    next(); // 다음 미들웨어로 이동
});
