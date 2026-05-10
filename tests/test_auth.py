from src.auth.security import get_password_hash

def test_crear_usuario_y_login(client):
    """Test: Crear usuario y hacer login"""

    #creacion del usuario
    usuario_data = {
        "nombre": "Test",
        "apellido": "User",
        "email": "test@example.com",
        "usuario": "testuser",
        "password": "soyuntest123",
        "telefono": "3794881881"
    }

    response = client.post("/usuarios", json=usuario_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data #no debe devolver la contraseña

    #login
    login_data = {
        "email": "test@example.com",
        "password": "soyuntest123"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_credenciales_incorrectas(client):
    """Test: Login con credenciales incorrectas"""

    #usuario
    usuario_data = {
        "nombre": "Test",
        "apellido": "User",
        "email": "test@example.com",
        "usuario": "testuser",
        "password": "soyuntest123",
        "telefono": "3794881881"
    }
    client.post("/usuarios/", json=usuario_data)

    #intentar loguearse con contraseña incorrecta
    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas"