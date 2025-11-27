// config/api.ts

// Configuración de URLs según el entorno
const API_URLS = {
  // Para desarrollo local
  development: {
    // Si pruebas en Android Emulator usa: 'http://10.0.2.2:8000'
    // Si pruebas en iOS Simulator usa: 'http://localhost:8000'
    // Si pruebas en dispositivo físico usa tu IP local: 'http://192.168.1.XXX:8000'
    android: 'http://10.0.2.2:8000',
    ios: 'http://localhost:8000',
    physical: 'http://192.168.68.172:8000', // Cambia por tu IP local
  },
  
  // Para producción
  production: {
    url: 'https://tu-dominio.com/api', // Tu URL de producción
  }
};

// Detectar el entorno y plataforma
import { Platform } from 'react-native';
import Constants from 'expo-constants';

const isProduction = Constants.expoConfig?.extra?.production || false;

// Función para obtener la URL base de la API
export const getApiUrl = (): string => {
  if (isProduction) {
    return API_URLS.production.url;
  }

  // Desarrollo
  if (Platform.OS === 'android') {
    return API_URLS.development.android;
  } else if (Platform.OS === 'ios') {
    return API_URLS.development.ios;
  } else {
    // Web o dispositivo físico - usa tu IP local
    return API_URLS.development.physical;
  }
};

// Endpoints de la API
export const API_ENDPOINTS = {
  ASK: '/ask',
  HEALTH: '/health',
};

// Función helper para hacer peticiones
export const apiRequest = async (
  endpoint: string,
  options: RequestInit = {}
): Promise<any> => {
  const url = `${getApiUrl()}${endpoint}`;
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
};