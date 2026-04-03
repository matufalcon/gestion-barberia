from sqlalchemy import Column, Integer, String, Numeric
from src.database import Base

class Servicio(Base):
    __tablename__= "servicios"

    servicio_id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(100), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False) # 10 dígitos, 2 decimales
    duracion = Column(Integer, nullable=False)

