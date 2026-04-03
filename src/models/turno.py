from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from src.database import Base

class Turno(Base):
    __tablename__="turnos"

    turno_id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    barbero_id = Column(Integer, ForeignKey("barberos.barbero_id"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.servicio_id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")
    notas = Column(Text, nullable=True)

    #relaciones entre tablas
    cliente = relationship("Usuario", foreign_keys=[cliente_id])
    barbero = relationship("Usuario", foreign_keys=[barbero_id])
    servicio = relationship("Servicio", foreign_keys=[servicio_id])