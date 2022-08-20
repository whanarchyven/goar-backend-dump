
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

