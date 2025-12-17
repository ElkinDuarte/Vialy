from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuario(Base):
    """Tabla de Usuarios - Vinculada a conversaciones"""
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    birth_date = Column(DateTime, nullable=True)  # Usé DateTime para flexibilidad; si prefieres DATE, cambia a Date
    phone_number = Column(String(20), nullable=True)
    country_code = Column(String(5), default='+57')
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relación con conversaciones
    conversaciones = relationship('Conversation', back_populates='usuario', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

class Conversation(Base):
    """Tabla de Conversaciones - Adaptada al esquema SQL"""
    __tablename__ = 'conversaciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    session_id = Column(String(100), nullable=False, unique=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Mapea a created_at en tu SQL
    ended_at = Column(DateTime, nullable=True)
    status = Column(Enum('activa', 'finalizada'), default='activa')
    
    # Relaciones
    usuario = relationship('Usuario', back_populates='conversaciones')
    messages = relationship('Message', back_populates='conversation', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Conversation {self.session_id}>'

class Message(Base):
    """Tabla de Mensajes - Adaptada al esquema SQL"""
    __tablename__ = 'mensajes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversacion_id = Column(Integer, ForeignKey('conversaciones.id'), nullable=False, index=True)
    sender = Column(Enum('usuario', 'chatbot'), nullable=False)  # Valores: 'usuario' o 'chatbot'
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación
    conversation = relationship('Conversation', back_populates='messages')
    
    def __repr__(self):
        return f'<Message {self.id}>'