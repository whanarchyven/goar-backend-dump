def test_register(db, client):
    res = client.post(
        "/api/profile/register/",
        {
            "email": "vladislah@ya.ru",
            "first_name": "Владислав",
            "phone": "+79119061531",
            "code": "f"
        }
    )
    assert res.status_code == 201
