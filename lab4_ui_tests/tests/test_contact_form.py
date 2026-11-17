import pytest

VALID_DATA = {
    "name": "Иван Петров",
    "email": "ivan@example.com",
    "phone": "+79991234567",
    "subject": "question",
    "message": "Здравствуйте! Подскажите сроки доставки заказа.",
    "agree": True,
}


def data_with(**changes):
    """Копия валидных данных, в которой изменены отдельные поля."""
    data = dict(VALID_DATA)
    data.update(changes)
    return data


# ---------- Позитивные сценарии ----------

def test_submit_form_with_valid_data(contact_page):
    contact_page.fill_form(**VALID_DATA).submit()

    assert (contact_page.get_success_message()
            == "Спасибо, Иван Петров! Ваше сообщение отправлено.")
    assert not contact_page.is_form_visible()


def test_submit_form_without_optional_phone(contact_page):
    contact_page.fill_form(**data_with(phone="")).submit()

    assert (contact_page.get_success_message()
            == "Спасибо, Иван Петров! Ваше сообщение отправлено.")


# ---------- Негативные сценарии: пустое обязательное поле ----------

@pytest.mark.parametrize("field, empty_value, expected_error", [
    ("name", "", "Введите имя"),
    ("email", "", "Введите email"),
    ("subject", "", "Выберите тему обращения"),
    ("message", "", "Введите сообщение"),
    ("agree", False, "Необходимо согласие на обработку данных"),
], ids=["empty_name", "empty_email", "no_subject", "empty_message",
        "no_agree"])
def test_empty_required_field_shows_error(contact_page, field,
                                          empty_value, expected_error):
    contact_page.fill_form(**data_with(**{field: empty_value})).submit()

    assert contact_page.get_error(field) == expected_error
    assert contact_page.is_form_visible()
    other_errors = {name: text for name, text
                    in contact_page.get_all_errors().items() if name != field}
    assert all(text == "" for text in other_errors.values())


# ---------- Негативные сценарии: некорректный формат ----------

@pytest.mark.parametrize("field, bad_value, expected_error", [
    ("name", "И", "Имя должно содержать от 2 до 50 букв"),
    ("name", "Ivan123", "Имя должно содержать от 2 до 50 букв"),
    ("email", "ivan@mail", "Некорректный email"),
    ("email", "ivan.example.com", "Некорректный email"),
    ("phone", "89991234567", "Телефон должен быть в формате +7XXXXXXXXXX"),
    ("message", "Коротко", "Сообщение должно содержать не менее 10 символов"),
], ids=["short_name", "name_with_digits", "email_without_domain",
        "email_without_at", "phone_wrong_format", "short_message"])
def test_invalid_value_shows_error(contact_page, field, bad_value,
                                   expected_error):
    contact_page.fill_form(**data_with(**{field: bad_value})).submit()

    assert contact_page.get_error(field) == expected_error
    assert contact_page.is_form_visible()


def test_empty_form_shows_all_required_errors(contact_page):
    contact_page.submit()

    assert contact_page.get_all_errors() == {
        "name": "Введите имя",
        "email": "Введите email",
        "phone": "",
        "subject": "Выберите тему обращения",
        "message": "Введите сообщение",
        "agree": "Необходимо согласие на обработку данных",
    }
