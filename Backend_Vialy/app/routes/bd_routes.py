from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.models import Usuario, Conversation, Message
import bcrypt
from datetime import datetime

# Crear blueprint para rutas
bd_routes = Blueprint('routes', __name__)

def register_routes(app):
    app.register_blueprint(routes_bp)

# Función auxiliar para obtener DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta de registro de usuario
@bd_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    birth_date = data.get('birth_date')  # Formato: 'YYYY-MM-DD'
    phone_number = data.get('phone_number')
    country_code = data.get('country_code', '+57')
    password = data.get('password')

    if not all([first_name, last_name, email, password]):
        return jsonify({'error': 'Campos obligatorios faltantes'}), 400

    db = next(get_db())
    if db.query(Usuario).filter_by(email=email).first():
        return jsonify({'error': 'Email ya registrado'}), 400

    # Hash de password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    nuevo_usuario = Usuario(
        first_name=first_name,
        last_name=last_name,
        email=email,
        birth_date = datetime.strptime(birth_date, '%d/%m/%Y') if birth_date else None,
        phone_number=phone_number,
        country_code=country_code,
        password_hash=hashed.decode('utf-8')
    )
    db.add(nuevo_usuario)
    db.commit()
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

@bd_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email y password requeridos'}), 400

    db = next(get_db())
    usuario = db.query(Usuario).filter_by(email=email).first()
    if not usuario or not bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
        return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401

    access_token = create_access_token(identity=str(usuario.id))
    
    return jsonify({
        'success': True,
        'access_token': access_token,
        'user': {
            'id': usuario.id,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name
        }
    }), 200

# Ruta para crear conversación (requiere auth)
@bd_routes.route('/conversations', methods=['POST'])
@jwt_required()
def create_conversation():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    session_id = data.get('session_id')

    if not session_id:
        return jsonify({'error': 'session_id requerido'}), 400

    db = next(get_db())
    nueva_conv = Conversation(usuario_id=user_id, session_id=session_id)
    db.add(nueva_conv)
    db.commit()
    return jsonify({'id': nueva_conv.id, 'message': 'Conversación creada'}), 201

# Ruta para listar conversaciones del usuario (requiere auth)
@bd_routes.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    user_id = int(get_jwt_identity())
    db = next(get_db())
    convs = db.query(Conversation).filter_by(usuario_id=user_id).order_by(Conversation.started_at.desc()).all()
    
    result = []
    for c in convs:
        # Contar mensajes de la conversación
        message_count = db.query(Message).filter_by(conversacion_id=c.id).count()
        
        # Obtener último mensaje para preview
        last_message = db.query(Message).filter_by(conversacion_id=c.id).order_by(Message.created_at.desc()).first()
        last_message_preview = last_message.message[:100] if last_message else "Sin mensajes"
        last_message_time = last_message.created_at.isoformat() if last_message else c.started_at.isoformat()
        
        result.append({
            'id': c.id,
            'session_id': c.session_id,
            'status': c.status,
            'started_at': c.started_at.isoformat(),
            'ended_at': c.ended_at.isoformat() if c.ended_at else None,
            'message_count': message_count,
            'last_message_preview': last_message_preview,
            'last_message_time': last_message_time
        })
    
    return jsonify(result), 200

# Ruta para enviar mensaje (requiere auth)
@bd_routes.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    message = data.get('message')

    if not conversation_id or not message:
        return jsonify({'error': 'conversation_id y message requeridos'}), 400

    db = next(get_db())
    conv = db.query(Conversation).filter_by(id=conversation_id, usuario_id=user_id).first()
    if not conv:
        return jsonify({'error': 'Conversación no encontrada'}), 404

    nuevo_msg = Message(conversacion_id=conversation_id, sender='usuario', message=message)
    db.add(nuevo_msg)
    db.commit()

    # Aquí puedes agregar lógica para respuesta del chatbot (ej. llamar a una función de IA)
    # Por ahora, solo guardamos el mensaje del usuario

    return jsonify({'id': nuevo_msg.id, 'message': 'Mensaje enviado'}), 201

# Ruta para obtener mensajes de una conversación (requiere auth)
@bd_routes.route('/messages/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    user_id = int(get_jwt_identity())
    db = next(get_db())
    conv = db.query(Conversation).filter_by(id=conversation_id, usuario_id=user_id).first()
    if not conv:
        return jsonify({'error': 'Conversación no encontrada'}), 404

    msgs = db.query(Message).filter_by(conversacion_id=conversation_id).order_by(Message.created_at).all()
    result = [{'id': m.id, 'sender': m.sender, 'message': m.message, 'created_at': m.created_at.isoformat()} for m in msgs]
    return jsonify(result), 200
