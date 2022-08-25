
def test_toggle_favorites(user1, recipe, auth_client):
    res = auth_client.post(
        "/api/recipes/toggle-favorites/",
        {"recipe_id": recipe.id}
    )
    assert res.status_code == 201

    res = auth_client.post(
        "/api/recipes/toggle-favorites/",
        {"recipe_id": recipe.id}
    )
    assert res.status_code == 204


def test_food_intake(user1, recipe, auth_client, user2, auth_client2, recipe2, course_day):
    res = auth_client.post(
        "/api/food-intake/",
        {
            "recipe": recipe.id,
            "course_day": course_day.id
        }
    )
    assert res.status_code == 201

    res = auth_client.post(
        "/api/food-intake/",
        {
            "recipe_id": recipe2.id,
            "course_day": course_day.id
        }
    )
    assert res.status_code == 201

    res = auth_client.get(
        "/api/food-intake/"
    )
    assert res.status_code == 200
    assert len(res.json()['results']) == 2

    res = auth_client2.get(
        "/api/food-intake/"
    )
    assert res.status_code == 200
    assert len(res.json()['results']) == 0

    res = auth_client2.post(
        "/api/food-intake/",
        {
            "recipe": recipe.id,
            "course_day": course_day.id
        }
    )
    assert res.status_code == 201

    res = auth_client2.get(
        "/api/food-intake/"
    )
    assert res.status_code == 200
    assert len(res.json()['results']) == 1

    res = auth_client.get(
        "/api/food-intake/"
    )
    assert res.status_code == 200
    assert len(res.json()['results']) == 2

    res2 = auth_client2.delete(
        f"/api/food-intake/{res.json()['results'][0]['id']}/",
    )
    assert res2.status_code == 403

    res3 = auth_client.delete(
        f"/api/food-intake/{res.json()['results'][0]['id']}/",
    )
    assert res3.status_code == 204


