def test_dairy(auth_client, auth_client2, course_day, course_day2):
    res = auth_client.get(
        "/api/dairy/"
    )
    assert res.status_code == 200
    assert res.json()['count'] == 2
    assert res.json()['results'][0]['tasks'][0]['done'] is False
    res = auth_client.post(
        f"/api/course/{res.json()['results'][0]['id']}/toggle-task-status/",
        {
            "task_id": 1
        }
    )
    assert res.status_code == 201
    res = auth_client.get(
        "/api/dairy/"
    )
    assert res.status_code == 200
    assert res.json()['count'] == 2
    assert res.json()['results'][0]['tasks'][0]['done'] is True

    res2 = auth_client2.get(
        "/api/dairy/"
    )
    assert res2.status_code == 200
    assert res2.json()['count'] == 2
    assert res2.json()['results'][0]['tasks'][0]['done'] is False

    res = auth_client.post(
        f"/api/course/{res.json()['results'][0]['id']}/update-user-dairy-day/",
        {
            "water": 20
        }
    )

    assert res.status_code == 200

    res = auth_client.get(
        "/api/dairy/"
    )
    assert res.status_code == 200
    assert res.json()['count'] == 2
    assert res.json()['results'][0]['water'] == 20

    res2 = auth_client2.get(
        "/api/dairy/"
    )
    assert res2.status_code == 200
    assert res2.json()['count'] == 2
    assert res2.json()['results'][0]['water'] is False


