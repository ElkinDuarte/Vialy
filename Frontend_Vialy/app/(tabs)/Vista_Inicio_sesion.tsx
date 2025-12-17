import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import React, { useState, useEffect, useRef } from 'react';
import LogoSvg from '../../assets/images/logo.svg';


import {
  AppState,
  AppStateStatus,
  Dimensions,
  KeyboardAvoidingView,
  Keyboard,
  Platform,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View
} from 'react-native';
import { API_ENDPOINTS, apiRequest } from '../../config/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Alert } from 'react-native';

const { height } = Dimensions.get('window');

export default function LoginScreen() {
  const navigation = useNavigation<any>();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  
  const appState = useRef(AppState.currentState);

  // Manejar ciclo de vida de la app
  useEffect(() => {
    const subscription = AppState.addEventListener('change', handleAppStateChange);
    return () => {
      subscription.remove();
    };
  }, []);

  const handleAppStateChange = (nextAppState: AppStateStatus) => {
    if (
      appState.current.match(/inactive|background/) &&
      nextAppState === 'active'
    ) {
      // App ha pasado de background a foreground
      Keyboard.dismiss();
    }
    appState.current = nextAppState;
  };

  const handleGoogleLogin = () => {
    console.log('Google login');
  };

  const handleFacebookLogin = () => {
    console.log('Facebook login');
  };

 const handleLogin = async () => {
  if (!email || !password) {
    Alert.alert('Error', 'Ingrese email y contraseña');
    return;
  }

  try {
    const data = await apiRequest(API_ENDPOINTS.LOGIN, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    // Login exitoso
    if (data.success) {
      await AsyncStorage.setItem('access_token', data.access_token);
      await AsyncStorage.setItem('user', JSON.stringify(data.user));
      await AsyncStorage.setItem('user_id', String(data.user.id));

      if (data.session_id) {
        await AsyncStorage.setItem('session_id', data.session_id);
      }

      navigation.navigate('Chat');
    } else {
      // Backend devolvió success = false
      Alert.alert('Error', data.message || 'Credenciales incorrectas');
    }

  } catch (error: any) {
    // Error HTTP específico
    if (error.message.includes('HTTP 401')) {
      Alert.alert('Error', 'Usuario o contraseña incorrectos');
    } else if (error.message.includes('HTTP 400')) {
      Alert.alert('Error', 'Datos enviados incorrectos');
    } else {
      console.error('Login error:', error);
      Alert.alert('Error', 'No se pudo conectar al servidor');
    }
  }
};
  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0A1F3E" translucent={false} />
      
      {/* Header con gradiente */}
      <LinearGradient
        colors={['#0A1F3E', '#0A1F3E', '#0A1F3E']}
        style={styles.header}
      >
        <View style={styles.stars}>
          {[...Array(20)].map((_, i) => (
            <View
              key={i}
              style={[
                styles.star,
                {
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                  opacity: Math.random() * 0.5 + 0.3,
                }
              ]}
            />
          ))}
        </View>
        
        {/* Logo */}
        <View style={styles.logoContainer}>
          <View>
            <LogoSvg width={40} height={40} />
          </View>
          <Text style={styles.logoText}>Vialy</Text>
        </View>

        <Text style={styles.title}>Inicia sesión</Text>
        <View style={styles.signupContainer}>
          <Text style={styles.noAccountText}>No tienes una Cuenta </Text>
          <TouchableOpacity onPress={() => navigation.navigate('Register')}>
            <Text style={styles.createAccountLink}>Cree una</Text>
          </TouchableOpacity>
        </View>

      </LinearGradient>

      {/* Formulario */}
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'padding'}
        style={styles.flex}
        enabled={true}
      >
        <View style={styles.formContainer}>
        {/* Email Input */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Email</Text>
          <TextInput
            style={styles.input}
            value={email}
            onChangeText={setEmail}
            placeholder="Loisbecket@gmail.com"
            keyboardType="email-address"
            autoCapitalize="none"
            placeholderTextColor="#999"
          />
        </View>

        {/* Password Input */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Contraseña</Text>
          <View style={styles.passwordContainer}>
            <TextInput
              style={styles.passwordInput}
              value={password}
              onChangeText={setPassword}
              placeholder="*******"
              secureTextEntry={!showPassword}
              placeholderTextColor="#999"
            />
            <TouchableOpacity
              style={styles.eyeIcon}
              onPress={() => setShowPassword(!showPassword)}
            >
              <Text style={styles.eyeText}>{showPassword ? '👁️' : '👁️‍🗨️'}</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Recordar y Olvidaste contraseña */}
        <View style={styles.optionsContainer}>
          <TouchableOpacity
            style={styles.checkboxContainer}
            onPress={() => setRememberMe(!rememberMe)}
          >
            <View style={[styles.checkbox, rememberMe && styles.checkboxChecked]}>
              {rememberMe && <Text style={styles.checkmark}>✓</Text>}
            </View>
            <Text style={styles.rememberText}>Recordar</Text>
          </TouchableOpacity>

          <TouchableOpacity>
            <Text style={styles.forgotPassword}>Olvidaste tu Contraseña ?</Text>
          </TouchableOpacity>
        </View>

        {/* Botón Log In */}
        <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
          <Text style={styles.loginButtonText}>Log In</Text>
        </TouchableOpacity>

        {/* Separador */}
        <Text style={styles.separator}>O inicia sesión con</Text>

        {/* Botones de redes sociales */}
        <View style={styles.socialContainer}>
          <TouchableOpacity
            style={styles.socialButton}
            onPress={handleGoogleLogin}
          >
            <Text style={styles.socialIcon}>G</Text>
            <Text style={styles.socialText}>Google</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.socialButton}
            onPress={handleFacebookLogin}
          >
            <Text style={styles.socialIcon}>f</Text>
            <Text style={styles.socialText}>Facebook</Text>
          </TouchableOpacity>
        </View>

        {/* Términos */}
        <Text style={styles.termsText}>
          Al registrarse, acepta los Términos de servicio y el Acuerdo de procesamiento de datos.
        </Text>
        </View>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  flex: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  header: {
    paddingTop: 20,
    paddingBottom: 30,
    paddingHorizontal: 20,
    position: 'relative',
    overflow: 'hidden',
  },
  stars: {
    position: 'absolute',
    width: '100%',
    height: '100%',
  },
  star: {
    position: 'absolute',
    width: 2,
    height: 2,
    backgroundColor: '#fff',
    borderRadius: 1,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 30,
  },
  logoBox: {
    width: 50,
    height: 50,
    backgroundColor: '#fff',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  logoIcon: {
    fontSize: 28,
  },
  logoText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 15,
    lineHeight: 50,
  },
  signupContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  noAccountText: {
    color: '#fff',
    fontSize: 16,
  },
  createAccountLink: {
    color: '#5eb3f6',
    fontSize: 16,
    fontWeight: '600',
  },
  formContainer: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 30,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    color: '#888',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    color: '#000',
  },
  passwordContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
  },
  passwordInput: {
    flex: 1,
    padding: 16,
    fontSize: 16,
    color: '#000',
  },
  eyeIcon: {
    padding: 16,
  },
  eyeText: {
    fontSize: 20,
  },
  optionsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 30,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkbox: {
    width: 22,
    height: 22,
    borderWidth: 2,
    borderColor: '#ddd',
    borderRadius: 4,
    marginRight: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: '#0A1F3E',
    borderColor: '#0A1F3E',
  },
  checkmark: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  rememberText: {
    fontSize: 16,
    color: '#666',
  },
  forgotPassword: {
    color: '#5eb3f6',
    fontSize: 16,
    fontWeight: '500',
  },
  loginButton: {
    backgroundColor: '#0A1F3E',
    borderRadius: 12,
    padding: 18,
    alignItems: 'center',
    marginBottom: 25,
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  separator: {
    textAlign: 'center',
    color: '#999',
    fontSize: 15,
    marginBottom: 20,
  },
  socialContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  socialButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    padding: 14,
    marginHorizontal: 6,
  },
  socialIcon: {
    fontSize: 22,
    marginRight: 8,
    fontWeight: 'bold',
  },
  socialText: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  termsText: {
    textAlign: 'center',
    color: '#999',
    fontSize: 13,
    lineHeight: 20,
    paddingHorizontal: 10,
  },
});