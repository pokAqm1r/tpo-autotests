const sent = JSON.parse(pm.request.body.raw);
// в теле запроса email задан переменной, берём её подставленное значение
sent.email = pm.collectionVariables.get("newEmail");

pm.test("Статус-код 201 Created", function () {
    pm.response.to.have.status(201);
});

pm.test("В ответе возвращается id нового пользователя", function () {
    const body = pm.response.json();
    pm.expect(body.id).to.be.a("number");
    pm.expect(body.id).to.eql(11);
    pm.collectionVariables.set("createdId", body.id);
});

pm.test("Ответ содержит отправленные данные", function () {
    const body = pm.response.json();
    pm.expect(body.name).to.eql(sent.name);
    pm.expect(body.username).to.eql(sent.username);
    pm.expect(body.email).to.eql(sent.email);
});
