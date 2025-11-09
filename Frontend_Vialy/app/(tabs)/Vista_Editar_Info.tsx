import { RouteProp } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { LinearGradient } from 'expo-linear-gradient';
import React, { useState } from 'react';
import {
    Alert,
    SafeAreaView,
    ScrollView,
    StatusBar,
    StyleSheet,
    Text,
    TextInput,
    TouchableOpacity,
    View,
} from 'react-native';

type EditProfileScreenProps = {
  navigation: StackNavigationProp<any>;
  route: RouteProp<any>;
};

export default function EditProfileScreen({ navigation, route }: EditProfileScreenProps) {
  const { userData } = route.params || {};

  const [name, setName] = useState(userData?.name || '');
  const [email, setEmail] = useState(userData?.email || '');
  const [phone, setPhone] = useState(userData?.phone || '');
  const [city, setCity] = useState(userData?.city || '');

  const handleGoBack = () => {
    navigation.goBack();
  };

  const handleSave = () => {
    // Aquí guardarías los datos en tu estado global o API
    console.log('Guardando datos:', {
      name,
      email,
      phone,
      city
    });

    Alert.alert(
      'Perfil Actualizado',
      'Tu información ha sido guardada correctamente',
      [
        {
          text: 'OK',
          onPress: () => navigation.goBack(),
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      {/* Header */}
      <LinearGradient colors={['#0A1F3E', '#0A1F3E']} style={styles.header}>
        <View style={styles.headerContent}>
          <TouchableOpacity onPress={handleGoBack} style={styles.backButton}>
            <Text style={styles.backArrow}>←</Text>
          </TouchableOpacity>
          <View style={styles.headerTextContainer}>
            <Text style={styles.headerTitle}>Editar Perfil</Text>
            <Text style={styles.headerSubtitle}>Actualiza tu información</Text>
          </View>
        </View>
      </LinearGradient>

      <ScrollView style={styles.content}>
        {/* Avatar Section */}
        <View style={styles.avatarSection}>
          <View style={styles.avatar}>
            <Text style={styles.avatarIcon}>👤</Text>
          </View>
          <TouchableOpacity style={styles.changePhotoButton}>
            <Text style={styles.changePhotoText}>Cambiar foto</Text>
          </TouchableOpacity>
        </View>

        {/* Formulario de Edición */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Información Personal</Text>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Nombre completo</Text>
            <TextInput
              style={styles.input}
              value={name}
              onChangeText={setName}
              placeholder="Ingresa tu nombre completo"
              placeholderTextColor="#999"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Correo electrónico</Text>
            <TextInput
              style={styles.input}
              value={email}
              onChangeText={setEmail}
              placeholder="correo@ejemplo.com"
              keyboardType="email-address"
              autoCapitalize="none"
              placeholderTextColor="#999"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Teléfono</Text>
            <TextInput
              style={styles.input}
              value={phone}
              onChangeText={setPhone}
              placeholder="+57 300 000 0000"
              keyboardType="phone-pad"
              placeholderTextColor="#999"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Ciudad</Text>
            <TextInput
              style={styles.input}
              value={city}
              onChangeText={setCity}
              placeholder="Bogotá, Colombia"
              placeholderTextColor="#999"
            />
          </View>
        </View>

        {/* Botón Guardar */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.saveButton} onPress={handleSave}>
            <Text style={styles.saveButtonText}>Guardar Cambios</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    paddingTop: 10,
    paddingBottom: 15,
    paddingHorizontal: 15,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  backButton: {
    padding: 8,
    marginRight: 12,
  },
  backArrow: {
    fontSize: 28,
    color: '#fff',
    fontWeight: '300',
  },
  headerTextContainer: {
    flex: 1,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 2,
  },
  headerSubtitle: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
  },
  content: {
    flex: 1,
  },
  avatarSection: {
    backgroundColor: '#fff',
    alignItems: 'center',
    paddingVertical: 30,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#5eb3f6',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  avatarIcon: {
    fontSize: 50,
  },
  changePhotoButton: {
    paddingHorizontal: 20,
    paddingVertical: 8,
  },
  changePhotoText: {
    fontSize: 16,
    color: '#2d4a75',
    fontWeight: '500',
  },
  section: {
    backgroundColor: '#fff',
    marginTop: 15,
    paddingVertical: 20,
    paddingHorizontal: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 20,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    fontWeight: '500',
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
  buttonContainer: {
    padding: 20,
    backgroundColor: '#fff',
    marginTop: 15,
  },
  saveButton: {
    backgroundColor: '#2d4a75',
    borderRadius: 12,
    padding: 18,
    alignItems: 'center',
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});