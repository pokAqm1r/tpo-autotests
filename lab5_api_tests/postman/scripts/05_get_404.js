pm.test("Статус-код 404 Not Found", function () {
    pm.response.to.have.status(404);
});

pm.test("Тело ответа — пустой объект", function () {
    pm.expect(pm.response.json()).to.eql({});
});
