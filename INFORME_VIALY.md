# 🚗 VIALY - Asistente Inteligente de Tránsito de Colombia

## Informe Técnico y Funcional de la Aplicación

**Fecha de presentación:** 16 de Diciembre de 2025  
**Versión:** 1.0

---

## 📋 ÍNDICE

1. [Descripción General](#1-descripción-general)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Tecnologías Utilizadas](#3-tecnologías-utilizadas)
4. [Funcionalidades Principales](#4-funcionalidades-principales)
5. [Estructura del Proyecto](#5-estructura-del-proyecto)
6. [Flujo de la Aplicación](#6-flujo-de-la-aplicación)
7. [Base de Datos](#7-base-de-datos)
8. [Sistema de Inteligencia Artificial](#8-sistema-de-inteligencia-artificial)
9. [API y Endpoints](#9-api-y-endpoints)
10. [Seguridad](#10-seguridad)
11. [Instrucciones de Ejecución](#11-instrucciones-de-ejecución)

---

## 1. DESCRIPCIÓN GENERAL

**VIALY** es una aplicación móvil inteligente diseñada para responder consultas sobre el **Código Nacional de Tránsito Terrestre de Colombia**. Utiliza tecnología de Inteligencia Artificial basada en RAG (Retrieval-Augmented Generation) para proporcionar respuestas precisas y contextualizadas a los usuarios.

### Objetivo Principal
Facilitar el acceso a la información del código de tránsito colombiano a través de una interfaz conversacional moderna y amigable, permitiendo a conductores, peatones y ciudadanos obtener respuestas rápidas sobre:

- Multas y sanciones de tránsito
- Procedimientos administrativos
- Requisitos legales para conducir
- Normativas viales

---

## 2. ARQUITECTURA DEL SISTEMA

La aplicación sigue una arquitectura **Cliente-Servidor** con los siguientes componentes:

```
┌─────────────────────────────────────────────────────────────────┐
│                     ARQUITECTURA VIALY                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────────────────┐ │
│  │   FRONTEND       │   API   │        BACKEND               │ │
│  │   (React Native) │ ◄─────► │        (Flask + Python)      │ │
│  │                  │  REST   │                              │ │
│  │  • Expo          │         │  ┌────────────────────────┐  │ │
│  │  • TypeScript    │         │  │   Servicios de IA      │  │ │
│  │  • Navigation    │         │  │   • Clasificación      │  │ │
│  │                  │         │  │   • RAG System         │  │ │
│  └──────────────────┘         │  │   • Ollama LLM         │  │ │
│                               │  └────────────────────────┘  │ │
│                               │                              │ │
│                               │  ┌────────────────────────┐  │ │
│                               │  │   Base de Datos        │  │ │
│                               │  │   (SQLite)             │  │ │
│                               │  └────────────────────────┘  │ │
│                               │                              │ │
│                               │  ┌────────────────────────┐  │ │
│                               │  │   Vector Database      │  │ │
│                               │  │   (ChromaDB)           │  │ │
│                               │  └────────────────────────┘  │ │
│                               └──────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. TECNOLOGÍAS UTILIZADAS

### Frontend (Aplicación Móvil)

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| **React Native** | 0.74+ | Framework principal para desarrollo móvil |
| **Expo** | SDK 51+ | Plataforma de desarrollo y despliegue |
| **TypeScript** | 5.x | Lenguaje tipado para mayor robustez |
| **React Navigation** | 6.x | Sistema de navegación (Stack + Drawer) |
| **AsyncStorage** | - | Almacenamiento local persistente |
| **Expo Linear Gradient** | - | Efectos visuales de gradientes |

### Backend (Servidor API)

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| **Python** | 3.12+ | Lenguaje principal del backend |
| **Flask** | 3.x | Framework web para API REST |
| **Flask-JWT-Extended** | - | Autenticación con JSON Web Tokens |
| **SQLAlchemy** | 2.x | ORM para base de datos |
| **SQLite** | - | Base de datos relacional |

### Inteligencia Artificial

| Tecnología | Descripción |
|------------|-------------|
| **LangChain** | Framework para aplicaciones con LLM |
| **Ollama** | Servidor local de modelos de lenguaje |
| **Mistral** | Modelo de lenguaje utilizado |
| **ChromaDB** | Base de datos vectorial para embeddings |
| **Sentence Transformers** | Generación de embeddings de texto |

---

## 4. FUNCIONALIDADES PRINCIPALES

### 4.1 Autenticación de Usuarios
- ✅ Registro de nuevos usuarios con validación de datos
- ✅ Inicio de sesión con email y contraseña
- ✅ Gestión segura de contraseñas (hash con bcrypt)
- ✅ Tokens JWT para sesiones autenticadas

### 4.2 Chat Inteligente con IA
- ✅ Interfaz conversacional tipo chat
- ✅ Respuestas basadas en el Código de Tránsito (PDF oficial)
- ✅ Clasificación automática de consultas:
  - **MULTA**: Consultas sobre sanciones y penalidades
  - **PROCEDIMIENTO**: Procesos administrativos
  - **NORMATIVA**: Reglas y regulaciones
  - **REQUISITO**: Documentos y condiciones necesarias
- ✅ Fuentes citadas en las respuestas
- ✅ Historial de conversación persistente

### 4.3 Gestión de Conversaciones
- ✅ Historial de conversaciones guardado
- ✅ Visualización de conversaciones previas
- ✅ Continuación de conversaciones existentes
- ✅ Creación de nuevas conversaciones

### 4.4 Secciones Informativas
- ✅ **Código de Tránsito**: Visor del código completo en PDF
- ✅ **Infracciones Comunes**: Listado de infracciones frecuentes
- ✅ **Conducción Apropiada**: Consejos y buenas prácticas

### 4.5 Perfil de Usuario
- ✅ Visualización de información personal
- ✅ Edición de datos del perfil
- ✅ Cierre de sesión seguro

---

## 5. ESTRUCTURA DEL PROYECTO

```
ChatBot Transito/
│
├── Frontend_Vialy/                 # Aplicación móvil
│   ├── app/
│   │   └── (tabs)/
│   │       ├── Vista_ChatBot.tsx           # Chat principal con IA
│   │       ├── Vista_Inicio_sesion.tsx     # Login
│   │       ├── Vista_Registro.tsx          # Registro de usuarios
│   │       ├── Vista_Historial.tsx         # Historial de chats
│   │       ├── Vista_Informacion_Usuario.tsx # Perfil
│   │       ├── Vista_Editar_Info.tsx       # Editar perfil
│   │       ├── Vista_Infracciones.tsx      # Infracciones comunes
│   │       ├── Vista_Conduccion_Apropiada.tsx # Tips de conducción
│   │       └── Vista_pdf.tsx               # Visor del código
│   │
│   ├── components/
│   │   └── menu.tsx                # Menú lateral (Drawer)
│   │
│   ├── config/
│   │   └── api.ts                  # Configuración de API
│   │
│   ├── navigation/
│   │   └── Navegacion_App.js       # Sistema de navegación
│   │
│   └── assets/                     # Imágenes y recursos
│
├── Backend_Vialy/                  # Servidor API
│   ├── app/
│   │   ├── config/
│   │   │   └── database.py         # Configuración de BD
│   │   │
│   │   ├── models/
│   │   │   └── models.py           # Modelos de datos
│   │   │
│   │   ├── routes/
│   │   │   ├── bd_routes.py        # Rutas de autenticación y BD
│   │   │   └── chat_routes.py      # Rutas del chatbot
│   │   │
│   │   ├── services/
│   │   │   ├── classification_service.py  # Clasificador de consultas
│   │   │   └── response_service.py        # Generador de respuestas
│   │   │
│   │   ├── rag/
│   │   │   ├── chain.py            # Cadena RAG con LangChain
│   │   │   └── rag_system.py       # Sistema de recuperación
│   │   │
│   │   ├── core/
│   │   │   └── session_manager.py  # Gestión de sesiones de chat
│   │   │
│   │   └── data/                   # PDFs del código de tránsito
│   │
│   └── main.py                     # Punto de entrada del servidor
│
└── README.md                       # Documentación
```

---

## 6. FLUJO DE LA APLICACIÓN

### 6.1 Flujo de Autenticación

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Usuario   │────►│   Login     │────►│   Backend   │
│   Abre App  │     │   Screen    │     │   Valida    │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           │              ┌─────▼─────┐
                           │              │   JWT     │
                           │              │   Token   │
                           │              └─────┬─────┘
                           │                    │
                    ┌──────▼────────────────────▼──────┐
                    │         Chat Principal           │
                    │    (Usuario autenticado)         │
                    └──────────────────────────────────┘
```

### 6.2 Flujo de Consulta al Chatbot

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Usuario   │────►│  Frontend   │────►│   /ask      │
│   Pregunta  │     │  Envía      │     │   Endpoint  │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                        ┌──────▼──────┐
                                        │ Clasificar  │
                                        │  Consulta   │
                                        └──────┬──────┘
                                               │
                                        ┌──────▼──────┐
                                        │ Buscar en   │
                                        │ Vector DB   │
                                        └──────┬──────┘
                                               │
                                        ┌──────▼──────┐
                                        │ Generar     │
                                        │ Respuesta   │
                                        │ (LLM)       │
                                        └──────┬──────┘
                                               │
                                        ┌──────▼──────┐
                                        │ Guardar en  │
                                        │ Base Datos  │
                                        └──────┬──────┘
                                               │
                    ┌──────────────────────────▼──────┐
                    │      Mostrar Respuesta          │
                    │      + Fuentes Citadas          │
                    └─────────────────────────────────┘
```

---

## 7. BASE DE DATOS

### Modelo Entidad-Relación

```
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│     USUARIOS      │       │  CONVERSACIONES   │       │     MENSAJES      │
├───────────────────┤       ├───────────────────┤       ├───────────────────┤
│ id (PK)           │──────<│ id (PK)           │──────<│ id (PK)           │
│ first_name        │       │ usuario_id (FK)   │       │ conversacion_id   │
│ last_name         │       │ session_id        │       │ sender            │
│ email (unique)    │       │ started_at        │       │ message           │
│ birth_date        │       │ ended_at          │       │ created_at        │
│ phone_number      │       │ status            │       └───────────────────┘
│ country_code      │       └───────────────────┘
│ password_hash     │
│ created_at        │
│ updated_at        │
└───────────────────┘
```

### Tablas Principales

| Tabla | Descripción |
|-------|-------------|
| **usuarios** | Almacena información de los usuarios registrados |
| **conversaciones** | Contiene las sesiones de chat de cada usuario |
| **mensajes** | Guarda cada mensaje individual (usuario y chatbot) |

---

## 8. SISTEMA DE INTELIGENCIA ARTIFICIAL

### 8.1 RAG (Retrieval-Augmented Generation)

El sistema utiliza RAG para proporcionar respuestas precisas basadas en el documento oficial del Código de Tránsito:

1. **Procesamiento del documento**: El PDF del código de tránsito se divide en chunks de texto
2. **Generación de embeddings**: Cada chunk se convierte en un vector numérico usando Sentence Transformers
3. **Almacenamiento vectorial**: Los embeddings se guardan en ChromaDB
4. **Recuperación**: Cuando el usuario pregunta, se buscan los chunks más relevantes
5. **Generación**: El modelo LLM genera una respuesta basada en el contexto recuperado

### 8.2 Clasificación de Consultas

El sistema clasifica automáticamente cada consulta en categorías:

| Categoría | Descripción | Ejemplo |
|-----------|-------------|---------|
| **MULTA** | Sanciones económicas y penalidades | "¿Cuánto cuesta la multa por exceso de velocidad?" |
| **PROCEDIMIENTO** | Procesos y trámites | "¿Cómo impugno un comparendo?" |
| **NORMATIVA** | Reglas y regulaciones | "¿Puedo dar vuelta en U en esta calle?" |
| **REQUISITO** | Documentos necesarios | "¿Qué documentos necesito para sacar la licencia?" |

### 8.3 Modelo de Lenguaje

- **Modelo**: Mistral (via Ollama)
- **Configuración**:
  - Temperatura: 0.3 (respuestas más precisas)
  - Contexto: 8192 tokens
  - Predicción máxima: 512 tokens

---

## 9. API Y ENDPOINTS

### Endpoints de Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/register` | Registro de nuevo usuario |
| `POST` | `/login` | Inicio de sesión |

### Endpoints del Chat

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/ask` | Enviar pregunta al chatbot |
| `GET` | `/conversations` | Listar conversaciones del usuario |
| `GET` | `/messages/{id}` | Obtener mensajes de una conversación |
| `POST` | `/clear-history` | Limpiar historial de una sesión |

### Endpoints de Sistema

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/health` | Verificar estado del servidor |
| `GET` | `/sessions/active` | Número de sesiones activas |

---

## 10. SEGURIDAD

### Medidas Implementadas

1. **Autenticación JWT**: Tokens seguros con expiración
2. **Hash de contraseñas**: Bcrypt para almacenamiento seguro
3. **Validación de entrada**: Sanitización de datos del usuario
4. **Headers de seguridad**: X-User-ID para identificación
5. **Rutas protegidas**: Decoradores @jwt_required()

---

## 11. INSTRUCCIONES DE EJECUCIÓN

### Requisitos Previos

- Python 3.12+
- Node.js 18+
- Expo CLI
- Ollama instalado con modelo Mistral

### Paso 1: Iniciar Backend

```powershell
cd "c:\Users\Elkin\Desktop\ChatBot Transito\Backend_Vialy"
python main.py
```

El servidor estará disponible en: `http://192.168.1.9:8000`

### Paso 2: Iniciar Frontend

```powershell
cd "c:\Users\Elkin\Desktop\ChatBot Transito\Frontend_Vialy"
npm start
```

### Paso 3: Ejecutar en Dispositivo

1. Escanear código QR con Expo Go
2. O ejecutar en emulador Android/iOS

---

## 📊 RESUMEN TÉCNICO

| Aspecto | Detalle |
|---------|---------|
| **Tipo de aplicación** | Móvil (Android/iOS) |
| **Arquitectura** | Cliente-Servidor REST |
| **Frontend** | React Native + Expo |
| **Backend** | Flask + Python |
| **Base de datos** | SQLite |
| **IA** | LangChain + Ollama (Mistral) |
| **Vectores** | ChromaDB |
| **Autenticación** | JWT |

---

## 👥 EQUIPO DE DESARROLLO

**Desarrollador Principal:** Elkin Duarte

---

*Documento generado para presentación académica - Diciembre 2025*
