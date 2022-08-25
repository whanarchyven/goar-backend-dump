
def test_chat(auth_client, auth_client2):
    res = auth_client.get(
        "/api/chat-message/"
    )
    assert res.status_code == 200
    assert res.json()['count'] == 0

    res = auth_client.post(
        "/api/chat-message/",
        {
            "message": "Вопрос",
            "message_type": "question"
        }
    )
    assert res.status_code == 201
    res = auth_client.get(
        "/api/chat-message/"
    )
    assert res.status_code == 200
    assert res.json()['count'] == 1

    res2 = auth_client2.get(
        "/api/chat-message/"
    )
    assert res2.status_code == 200
    assert res2.json()['count'] == 0

