const sent = JSON.parse(pm.request.body.raw);

pm.test("Статус-код 200", function () {
    pm.response.to.have.status(200);
});

pm.test("id пользователя не изменился", function () {
    pm.expect(pm.response.json().id).to.eql(1);
});

pm.test("Поля обновлены переданными значениями", function () {
    const body = pm.response.json();
    pm.expect(body.name).to.eql(sent.name);
    pm.expect(body.username).to.eql(sent.username);
    pm.expect(body.email).to.eql(sent.email);
});

pm.test("PUT заменяет ресурс целиком: старых полей нет", function () {
    pm.expect(pm.response.json()).to.not.have.property("address");
});
