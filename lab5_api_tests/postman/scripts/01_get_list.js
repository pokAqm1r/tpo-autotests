pm.test("Статус-код 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Ответ в формате JSON", function () {
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});

pm.test("Возвращается массив из 10 пользователей", function () {
    const users = pm.response.json();
    pm.expect(users).to.be.an("array").that.has.lengthOf(10);
});

pm.test("У каждого пользователя есть id, name, username, email", function () {
    pm.response.json().forEach(function (user) {
        pm.expect(user).to.include.all.keys("id", "name", "username", "email");
        pm.expect(user.email).to.include("@");
    });
});
