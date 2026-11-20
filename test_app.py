from app import app

def test_hello_endpoint_valid():
    client = app.test_client()
    response = client.get('/hello?name=Ignacio')
    assert response.status_code == 200
    assert b"Hello, Ignacio!" in response.data

def test_hello_xss_blocked():
    client = app.test_client()
    response = client.get("/hello?name=<script>alert('XSS')</script>")
    assert response.status_code == 400