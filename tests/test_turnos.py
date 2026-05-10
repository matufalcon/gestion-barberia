from datetime import datetime, timedelta

def test_crear_turno_exitoso(client):
    """Test: Crear turno exitoso con datos validos"""

    #creacion del usuario y token
    usuario_data = {
        "nombre": "Cliente",
        "apellido": "Test",
        "email": "cliente@test.com",
        "usuario": "testclient",
        "password": "cliente123",
        "telefono": "3794033333"
    }
    client.post("/usuarios/", json=usuario_data)

    login = client.post("/auth/login", json = {
        "email": "cliente@test.com",
        "password": "cliente123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    #creacion de servicio
    servicio_data = {
        "descripcion": "Corte clásico",
        "precio": 7000.0,
        "duracion": 30
    }
    servicio_resp = client.post("/servicios/", json=servicio_data, headers=headers)
    servicio_id = servicio_resp.json()["servicio_id"]

    #creacion de barbero
    barbero_usuario = {
        "nombre": "Mauro",
        "apellido": "Lopez",
        "email": "barbero@test.com",
        "usuario": "maurobarber",
        "password": "pass123",
        "telefono": "3794789456"
    }
    user_resp = client.post("/usuarios/", json=barbero_usuario)
    usuario_id = user_resp.json()["usuario_id"]
    
    barbero_data = {
        "usuario_id": usuario_id,
        "especialidad": "Cortes clásicos",
        "activo": True
    }
    barbero_resp = client.post("/barberos/", json=barbero_data, headers=headers)
    barbero_id = barbero_resp.json()["barbero_id"]

    #creacion de turno
    fecha_futura = (datetime.now() + timedelta(days=1)).isoformat()
    turno_data = {
        "cliente_id": user_resp.json()["usuario_id"],
        "barbero_id": barbero_id,
        "servicio_id": servicio_id,
        "fecha_hora": fecha_futura,
        "estado": "pendiente"
    }
    
    response = client.post("/turnos/", json=turno_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["barbero_id"] == barbero_id
    assert data["servicio_id"] == servicio_id

def test_turno_fecha_pasada(client):
    """Test: No permite crear turno en fecha pasada"""
    
    # (usuario, servicio, barbero)
    usuario_data = {
        "nombre": "Test", "apellido": "User",
        "email": "user@test.com", "usuario": "test",
        "password": "pass", "telefono": "3794123385"
    }
    client.post("/usuarios/", json=usuario_data)
    login = client.post("/auth/login", json={"email": "user@test.com", "password": "pass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    servicio = client.post("/servicios/", json={
        "descripcion": "Corte", "precio": 10000.0, "duracion": 30
    }, headers=headers)
    
    barbero_user = client.post("/usuarios/", json={
        "nombre": "Benicio", "apellido": "Vicuña", "email": "beni@test.com",
        "usuario": "beniciobarber", "password": "pass123", "telefono": "3794456677"
    })
    barbero = client.post("/barberos/", json={
        "usuario_id": barbero_user.json()["usuario_id"],
        "especialidad": "Todo", "activo": True
    }, headers=headers)
    
    # Intentar crear turno en el pasado
    fecha_pasada = (datetime.now() - timedelta(days=1)).isoformat()
    turno_data = {
        "cliente_id": barbero_user.json()["usuario_id"],
        "barbero_id": barbero.json()["barbero_id"],
        "servicio_id": servicio.json()["servicio_id"],
        "fecha_hora": fecha_pasada,
        "estado": "pendiente"
    }
    
    response = client.post("/turnos/", json=turno_data, headers=headers)
    assert response.status_code == 400
    assert "fecha" in response.json()["detail"].lower()