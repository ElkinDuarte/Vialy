import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';
import React, { useState, useEffect, useRef } from 'react';
import {
  Alert,
  AppState,
  AppStateStatus,
  Dimensions,
  KeyboardAvoidingView,
  Keyboard,
  Platform,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View
} from 'react-native';
import { API_ENDPOINTS, apiRequest } from '../../config/api';

const { height } = Dimensions.get('window');

export default function RegisterScreen() {
  const navigation = useNavigation<any>();
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [countryCode, setCountryCode] = useState('+57');
  const [isLoading, setIsLoading] = useState(false);

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

  const handleGoBack = () => {
    navigation.goBack();
  };

  const handleRegister = async () => {
    setIsLoading(true);
    try {
      const data = await apiRequest(API_ENDPOINTS.REGISTER, {
        method: 'POST',
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          email: email,
          birth_date: birthDate,
          phone_number: phoneNumber,
          country_code: countryCode,
          password: password,
        }),
      });
      Alert.alert('Éxito', 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.');
      navigation.navigate('Login');
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'Error al registrar usuario. Verifica tu conexión.');
    } finally {
      setIsLoading(false);
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

        {/* Botón de regreso */}
        <TouchableOpacity style={styles.backButton} onPress={handleGoBack}>
          <Text style={styles.backArrow}>←</Text>
        </TouchableOpacity>

        <Text style={styles.title}>Registrese</Text>
        <View style={styles.signupContainer}>
          <Text style={styles.noAccountText}>Ya tienes una Cuenta </Text>
          <TouchableOpacity onPress={() => navigation.navigate('Login')}>
            <Text style={styles.createAccountLink}>Inicie Sesion</Text>
          </TouchableOpacity>
        </View>
      </LinearGradient>

      {/* Formulario */}
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'padding'}
        style={styles.flex}
        enabled={true}
      >
        <ScrollView 
          style={styles.formContainer} 
          showsVerticalScrollIndicator={false}
          scrollEnabled={true}
        >
        {/* Nombre y Apellido */}
        <View style={styles.rowInputs}>
          <View style={[styles.inputGroup, styles.halfInput]}>
            <Text style={styles.label}>Nombre</Text>
            <TextInput
              style={styles.input}
              value={firstName}
              onChangeText={setFirstName}
              placeholder="Lois"
              placeholderTextColor="#999"
            />
          </View>

          <View style={[styles.inputGroup, styles.halfInput]}>
            <Text style={styles.label}>Apellido</Text>
            <TextInput
              style={styles.input}
              value={lastName}
              onChangeText={setLastName}
              placeholder="Becket"
              placeholderTextColor="#999"
            />
          </View>
        </View>

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

        {/* Fecha de Nacimiento */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Fecha de Nacimiento</Text>
          <View style={styles.dateContainer}>
            <TextInput
              style={styles.dateInput}
              value={birthDate}
              onChangeText={setBirthDate}
              placeholder="18/03/2024"
              placeholderTextColor="#999"
            />
            <Text style={styles.calendarIcon}>📅</Text>
          </View>
        </View>

        {/* Número de Teléfono */}
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Numero de Telefono</Text>
          <View style={styles.phoneContainer}>
            <View style={styles.countryCodeContainer}>
              <Text style={styles.flagIcon}>🇨🇴</Text>
              <Text style={styles.countryCode}>{countryCode}</Text>
              <Text style={styles.dropdownIcon}>▼</Text>
            </View>
            <TextInput
              style={styles.phoneInput}
              value={phoneNumber}
              onChangeText={setPhoneNumber}
              placeholder="(300) 000-0000"
              keyboardType="phone-pad"
              placeholderTextColor="#999"
            />
          </View>
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

        {/* Botón Registrar */}
        <TouchableOpacity style={styles.registerButton} onPress={handleRegister}>
          <Text style={styles.registerButtonText}>Registrar</Text>
        </TouchableOpacity>
        </ScrollView>
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
  backButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    marginBottom: 20,
  },
  backArrow: {
    fontSize: 32,
    color: '#fff',
    fontWeight: '300',
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
  rowInputs: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  inputGroup: {
    marginBottom: 20,
  },
  halfInput: {
    width: '48%',
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
    backgroundColor: '#fff',
  },
  dateContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    backgroundColor: '#fff',
  },
  dateInput: {
    flex: 1,
    padding: 16,
    fontSize: 16,
    color: '#000',
  },
  calendarIcon: {
    padding: 16,
    fontSize: 20,
  },
  phoneContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    backgroundColor: '#fff',
  },
  countryCodeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingLeft: 16,
    paddingRight: 12,
    borderRightWidth: 1,
    borderRightColor: '#ddd',
  },
  flagIcon: {
    fontSize: 20,
    marginRight: 8,
  },
  countryCode: {
    fontSize: 16,
    color: '#000',
    marginRight: 4,
  },
  dropdownIcon: {
    fontSize: 10,
    color: '#666',
  },
  phoneInput: {
    flex: 1,
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
    backgroundColor: '#fff',
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
  registerButton: {
    backgroundColor: '#152947',
    borderRadius: 12,
    padding: 18,
    alignItems: 'center',
    marginBottom: 40,
  },
  registerButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});