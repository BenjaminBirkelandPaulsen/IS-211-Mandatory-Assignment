def test_homepage_renders_navigation(client):
    resp = client.get("/")

    assert resp.status_code == 200
    page = resp.get_data(as_text=True)
    assert "BUA Renting Service" in page
    assert 'href="/users/"' in page
    assert 'href="/items/"' in page
    assert 'href="/loans/"' in page