# 🎯 VIALY - Presentación Ejecutiva

## Diapositivas para Presentación

---

# DIAPOSITIVA 1: PORTADA

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                    🚗 VIALY                                   ║
║                                                                ║
║         Asistente Inteligente de Tránsito                     ║
║               de Colombia                                      ║
║                                                                ║
║    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
║                                                                ║
║         Aplicación Móvil con Inteligencia Artificial          ║
║                                                                ║
║                                                                ║
║                  Diciembre 2025                                ║
║                  Elkin Duarte                                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

# DIAPOSITIVA 2: EL PROBLEMA

## ¿Por qué VIALY?

### 📌 Problemática Actual

- 📚 El Código de Tránsito tiene más de **400 páginas**
- ⏱️ Los ciudadanos no tienen tiempo para leerlo completo
- ❓ Existe confusión sobre multas y procedimientos
- 🔍 La información está dispersa y es difícil de consultar
- 💰 Muchos conductores pagan multas por desconocimiento

### 💡 Nuestra Solución

> **Un asistente de IA que responde preguntas sobre tránsito
> en lenguaje natural, 24/7, desde tu celular**

---

# DIAPOSITIVA 3: LA SOLUCIÓN

## ¿Qué es VIALY?

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   📱 Una app móvil que permite:                           │
│                                                            │
│   ✅ Preguntar sobre multas de tránsito                   │
│   ✅ Consultar procedimientos legales                     │
│   ✅ Conocer requisitos para conducir                     │
│   ✅ Entender la normativa vial                           │
│                                                            │
│   🤖 Usando Inteligencia Artificial                       │
│   📄 Basada en el Código de Tránsito oficial              │
│   💬 Con una interfaz conversacional amigable             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

# DIAPOSITIVA 4: CARACTERÍSTICAS PRINCIPALES

## Funcionalidades Clave

| Característica | Descripción |
|---|---|
| 🤖 **Chat Inteligente** | Conversación natural con IA |
| 📋 **Clasificación Automática** | Identifica el tipo de consulta |
| 📚 **Fuentes Citadas** | Muestra de dónde viene la información |
| 💾 **Historial Persistente** | Guarda todas tus conversaciones |
| 👤 **Perfil de Usuario** | Registro y gestión de cuenta |
| 📄 **Visor PDF** | Acceso al código completo |

---

# DIAPOSITIVA 5: ARQUITECTURA TÉCNICA

## Cómo funciona por dentro

```
   ┌──────────────┐              ┌─────────────────────┐
   │              │    REST      │                     │
   │  📱 APP      │ ◄──────────► │  🖥️ SERVIDOR       │
   │  MÓVIL      │    API       │                     │
   │              │              │  ┌───────────────┐  │
   │  React       │              │  │ 🧠 IA         │  │
   │  Native      │              │  │ • LangChain   │  │
   │              │              │  │ • Ollama      │  │
   │              │              │  │ • ChromaDB    │  │
   │              │              │  └───────────────┘  │
   │              │              │                     │
   │              │              │  ┌───────────────┐  │
   │              │              │  │ 🗄️ BASE DATOS │  │
   │              │              │  │ SQLite        │  │
   │              │              │  └───────────────┘  │
   └──────────────┘              └─────────────────────┘
```

---

# DIAPOSITIVA 6: TECNOLOGÍAS UTILIZADAS

## Stack Tecnológico

### Frontend (Móvil)
- **React Native** + Expo
- **TypeScript** 
- **React Navigation**

### Backend (Servidor)
- **Python** + Flask
- **SQLAlchemy** + SQLite
- **JWT** para autenticación

### Inteligencia Artificial
- **LangChain** - Framework de IA
- **Ollama** - Modelos locales
- **ChromaDB** - Base vectorial
- **Mistral** - Modelo de lenguaje

---

# DIAPOSITIVA 7: FLUJO DE USO

## ¿Cómo usa la app el usuario?

```
1️⃣ REGISTRO/LOGIN
   ↓
2️⃣ PANTALLA DE CHAT
   ↓
3️⃣ USUARIO ESCRIBE PREGUNTA
   Ej: "¿Cuánto cuesta la multa por no usar cinturón?"
   ↓
4️⃣ LA IA PROCESA LA CONSULTA
   • Clasifica la pregunta
   • Busca en el código de tránsito
   • Genera respuesta
   ↓
5️⃣ USUARIO RECIBE RESPUESTA
   Con la información precisa + fuentes
   ↓
6️⃣ CONVERSACIÓN GUARDADA
   Para consultar después
```

---

# DIAPOSITIVA 8: SISTEMA RAG

## ¿Cómo responde la IA?

### RAG = Retrieval-Augmented Generation

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   📄 CÓDIGO DE TRÁNSITO (PDF)                              │
│          ↓                                                  │
│   ✂️ DIVIDIR EN FRAGMENTOS                                 │
│          ↓                                                  │
│   🔢 CONVERTIR A VECTORES (Embeddings)                     │
│          ↓                                                  │
│   💾 ALMACENAR EN ChromaDB                                 │
│                                                             │
│   ────────────────────────────────────────────────────────  │
│                                                             │
│   ❓ USUARIO PREGUNTA                                       │
│          ↓                                                  │
│   🔍 BUSCAR FRAGMENTOS RELEVANTES                          │
│          ↓                                                  │
│   🧠 GENERAR RESPUESTA CON LLM                             │
│          ↓                                                  │
│   ✅ RESPUESTA PRECISA + FUENTES                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

# DIAPOSITIVA 9: CAPTURAS DE PANTALLA

## Pantallas Principales

### 📱 Login y Registro
- Autenticación segura con email y contraseña
- Validación de datos en tiempo real

### 💬 Chat Principal
- Interfaz conversacional moderna
- Indicador de escritura
- Mensajes con timestamp

### 📋 Menú Lateral
- Acceso a todas las funciones
- Historial de conversaciones
- Perfil de usuario

### 📄 Visor de PDF
- Código de tránsito completo
- Navegación fácil

---

# DIAPOSITIVA 10: SEGURIDAD

## Medidas de Protección

| Aspecto | Implementación |
|---|---|
| 🔐 **Contraseñas** | Hash con Bcrypt |
| 🎫 **Sesiones** | Tokens JWT con expiración |
| ✅ **Validación** | Sanitización de entrada |
| 🔒 **Rutas** | Protección con decoradores |
| 🆔 **Identificación** | Headers seguros (X-User-ID) |

---

# DIAPOSITIVA 11: BASE DE DATOS

## Modelo de Datos

```
┌─────────────┐      ┌─────────────────┐      ┌─────────────┐
│  USUARIOS   │      │ CONVERSACIONES  │      │  MENSAJES   │
├─────────────┤      ├─────────────────┤      ├─────────────┤
│ id          │──┐   │ id              │──┐   │ id          │
│ nombre      │  └──►│ usuario_id      │  └──►│ conv_id     │
│ email       │      │ session_id      │      │ sender      │
│ contraseña  │      │ estado          │      │ mensaje     │
│ teléfono    │      │ fechas          │      │ fecha       │
└─────────────┘      └─────────────────┘      └─────────────┘
```

---

# DIAPOSITIVA 12: DEMOSTRACIÓN

## Demo en Vivo

### Escenarios de prueba:

1. **Registro de usuario nuevo**
2. **Login con credenciales**
3. **Pregunta sobre multas:**
   > "¿Cuánto es la multa por exceso de velocidad?"
4. **Pregunta sobre requisitos:**
   > "¿Qué documentos necesito para la licencia?"
5. **Ver historial de conversaciones**
6. **Continuar conversación anterior**

---

# DIAPOSITIVA 13: PRÓXIMOS PASOS

## Roadmap Futuro

### Corto Plazo (1-3 meses)
- 🔔 Notificaciones push
- 🌙 Modo oscuro
- 📊 Dashboard de estadísticas

### Mediano Plazo (3-6 meses)
- 🗣️ Reconocimiento de voz
- 🌐 Múltiples idiomas
- 🗺️ Integración con mapas

### Largo Plazo (6-12 meses)
- 📸 Escaneo de comparendos
- 💳 Pago de multas
- 🚗 Alertas personalizadas

---

# DIAPOSITIVA 14: CONCLUSIONES

## Resumen

### ✅ Lo que logramos:

- 📱 Aplicación móvil funcional
- 🤖 Integración de IA para consultas
- 💾 Sistema de usuarios y sesiones
- 📚 Consultas basadas en documentos oficiales
- 🔐 Seguridad implementada

### 💡 Valor agregado:

> **VIALY democratiza el acceso a la información
> de tránsito, permitiendo a cualquier ciudadano
> resolver sus dudas de forma rápida e inteligente**

---

# DIAPOSITIVA 15: PREGUNTAS

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                     ¿Preguntas?                               ║
║                                                                ║
║                        🙋‍♂️                                     ║
║                                                                ║
║    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
║                                                                ║
║                   ¡Gracias por su atención!                   ║
║                                                                ║
║                                                                ║
║                    📧 Contacto:                               ║
║                    Elkin Duarte                               ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 📝 NOTAS PARA EL PRESENTADOR

### Puntos clave a enfatizar:

1. **Problema real**: Mencionar estadísticas de multas por desconocimiento
2. **Solución innovadora**: Uso de IA para resolver un problema cotidiano
3. **Tecnología moderna**: Stack actualizado y escalable
4. **Seguridad**: Datos del usuario protegidos
5. **Escalabilidad**: Puede adaptarse a otros países/regulaciones

### Tiempo sugerido por sección:

| Sección | Tiempo |
|---------|--------|
| Introducción (1-3) | 3 min |
| Características (4-6) | 5 min |
| Técnico (7-9) | 5 min |
| Demo | 5 min |
| Futuro y cierre (10-15) | 2 min |
| **TOTAL** | **20 min** |

---

*Presentación preparada para: 16 de Diciembre 2025*
