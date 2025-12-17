// Configuración de URLs según entorno
const API_URLS = {
  production: {
    base: 'http://10.191.36.210:8000',
  },
  development: {
    android: 'http://10.0.2.2:5000', // Flask usa 5000
    ios: 'http://localhost:5000',
    physical: 'http://10.191.36.210:8000', // IP correcta local
  }
};


// Detectar el entorno y plataforma
import { Platform } from 'react-native';
import Constants from 'expo-constants';
import AsyncStorage from '@react-native-async-storage/async-storage';


const isProduction = Constants.expoConfig?.extra?.production || false;


// Función para obtener la URL base de la API
export const getApiUrl = (): string => {
  return API_URLS.development.physical;
};


// Endpoints de la API
export const API_ENDPOINTS = {
  ASK: '/ask',
  HEALTH: '/health',
  REGISTER: '/register',
  LOGIN: '/login',
  CONVERSATIONS: '/conversations',
  MESSAGES: '/messages',
};


// Función helper para hacer peticiones
export const apiRequest = async (
  endpoint: string,
  options: RequestInit = {}
): Promise<any> => {
  const url = `${getApiUrl()}${endpoint}`;

  // Obtener user_id guardado en AsyncStorage
  const user_id = await AsyncStorage.getItem('user_id');

  // Construir headers combinando defaults con los que vienen en options
  const headers = {
    'Content-Type': 'application/json',
    ...(user_id ? { 'X-User-ID': user_id } : {}),
    ...(options.headers || {}),
  };

  const finalOptions: RequestInit = {
    ...options,
    headers: headers, // Aseguramos que usamos los headers combinados
  };

  try {
    const response = await fetch(url, finalOptions);

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`HTTP ${response.status}: ${text}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
};


export const getBaseUrl = (): string => {
  // ahora mismo es la misma que la de la API
  return getApiUrl();
};