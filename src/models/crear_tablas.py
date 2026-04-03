from src.database import engine, Base
from src.models import Usuario, Servicio, Barbero, Turno

def crear_tablas():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente")

if __name__ == "__main__":
    crear_tablas()