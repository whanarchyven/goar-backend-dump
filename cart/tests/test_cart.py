from django.contrib.auth import get_user_model

User = get_user_model()


def test_add_delete_update_product_to_cart(auth_client, auth_client2, user1, user2, product_2, product_1):
    """Добавление продукта в корзину."""

    res = auth_client.post(
        "/api/cart/add/",
        {
            "product_id": product_1.id
        }
    )
    assert res.status_code == 201

    res = auth_client2.post(
        "/api/cart/add/",
        {
            "product_id": product_2.id
        }
    )
    assert res.status_code == 201

    res = auth_client.get(
        "/api/cart/"
    )
    assert res.status_code == 200
    assert res.json()[0]["items"][0]["product"]["name"] == "Рис"
    assert res.json()[0]["items"][0]["purchased"] is False

    res = auth_client2.get(
        "/api/cart/"
    )
    assert res.status_code == 200
    assert res.json()[0]["items"][0]["product"]["name"] == "Греча"
    assert res.json()[0]["items"][0]["purchased"] is False

    # Удалить

    res = auth_client2.post(
        "/api/cart/delete/",
        {
            "product_id": product_2.id
        }
    )
    assert res.status_code == 200
    assert len(res.json()['items']) == 0

    # Обновить

    res = auth_client.post(
        "/api/cart/update-status/",
        {
            "product_id": product_1.id,
            "purchased": True
        }
    )
    assert res.status_code == 200
    assert res.json()["items"][0]["product"]["name"] == "Рис"
    assert res.json()["items"][0]["purchased"] is True



