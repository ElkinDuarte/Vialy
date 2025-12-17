# 🚗 Chatbot Transito - App Móvil

Una aplicación móvil inteligente que responde preguntas sobre el **Código Nacional de Tránsito Terrestre de Colombia** usando IA.

## 📱 Features

- ✅ Chat interactivo con preguntas sobre tránsito
- ✅ Clasificación automática de preguntas (MULTA, PROCEDIMIENTO, NORMATIVA, REQUISITO)
- ✅ Respuestas basadas en PDF del Código de Tránsito 
- ✅ Historial de conversaciones persistente
- ✅ UI moderna y responsive
- ✅ Funcionamiento offline (con respuestas predefinidas)

## 🚀 Inicio Rápido

### Opción 1: Automático (Recomendado)

```powershell
# En PowerShell
cd "c:\Users\Elkin\Desktop\ChatBot Transito"
.\start_app.ps1
```

### Opción 2: Manual

**Terminal 1 - Backend:**
```bash
cd "c:\Users\Elkin\Desktop\ChatBot Transito\Backend_Vialy"
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd "c:\Users\Elkin\Desktop\ChatBot Transito\Frontend_Vialy"
npm start
```

### Opción 3: Testing

```bash
cd Backend_Vialy
python test_complete.py
```

## 📋 Requisitos

- Python 3.12+
- Node.js 18+
- npm o yarn
- Expo CLI
- Dispositivo Android/iOS o emulador

## 📚 Documentación Completa

Ver [SETUP_COMPLETO.md](./SETUP_COMPLETO.md) para instrucciones detalladas sobre instalación, configuración y troubleshooting.

## 🧪 Testing de API

```bash
cd Backend_Vialy
python test_complete.py
```

Debería mostrar:
- ✅ Health Check
- ✅ Test MULTA
- ✅ Test REQUISITO
- ✅ Test NORMATIVA
- ✅ Test PROCEDIMIENTO

## ✨ Estado Actual

- **Backend**: ✅ LISTO - Servidor Flask corriendo, PDF integrado, clasificación funcionando
- **Frontend**: ✅ LISTO - Componentes básicos listos, API integrada
- **Database**: ✅ LISTO - SQLite simplificado (Conversation + Message)
- **Tests**: ✅ PASANDO - Todos los tests de API pasando

## 🎯 Próximos Pasos

1. `npm install` en Frontend_Vialy
2. `python main.py` en Backend_Vialy
3. `npm start` en Frontend_Vialy
4. Probar desde la app móvil o web

¡La app está lista para usar! 🎉
