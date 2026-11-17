const userSchema = {
    type: "object",
    required: ["id", "name", "username", "email", "address", "phone", "company"],
    properties: {
        id: { type: "integer" },
        name: { type: "string" },
        username: { type: "string" },
        email: { type: "string" },
        address: {
            type: "object",
            required: ["street", "city", "zipcode", "geo"],
            properties: {
                city: { type: "string" },
                geo: {
                    type: "object",
                    required: ["lat", "lng"]
                }
            }
        },
        phone: { type: "string" },
        company: { type: "object", required: ["name"] }
    }
};

pm.test("Статус-код 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Время ответа меньше 2000 мс", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Структура JSON соответствует схеме", function () {
    pm.response.to.have.jsonSchema(userSchema);
});

pm.test("Значения полей пользователя с id = 1", function () {
    const user = pm.response.json();
    pm.expect(user.id).to.eql(1);
    pm.expect(user.name).to.eql("Leanne Graham");
    pm.expect(user.username).to.eql("Bret");
    pm.expect(user.email).to.eql("Sincere@april.biz");
    pm.expect(user.address.city).to.eql("Gwenborough");
});
