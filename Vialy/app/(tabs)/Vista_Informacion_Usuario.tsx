import { StackNavigationProp } from '@react-navigation/stack';
import { LinearGradient } from 'expo-linear-gradient';
import React from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

type ProfileScreenProps = {
  navigation: StackNavigationProp<any>;
};

export default function ProfileScreen({ navigation }: ProfileScreenProps) {
  // Datos del usuario (estos vendrían de tu estado global o API)
  const userData = {
    name: 'Juan Pérez García',
    email: 'usuario@ejemplo.com',
    phone: '+57 300 000 0000',
    city: 'Bogotá, Colombia'
  };

  const handleGoBack = () => {
    navigation.goBack();
  };

  const handleEditProfile = () => {
    navigation.navigate('Edit_Profile', { userData });
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
            <Text style={styles.headerTitle}>Mi Perfil</Text>
            <Text style={styles.headerSubtitle}>Información personal</Text>
          </View>
        </View>
      </LinearGradient>

      <ScrollView style={styles.content}>
        {/* Avatar Section */}
        <View style={styles.avatarSection}>
          <View style={styles.avatar}>
            <Text style={styles.avatarIcon}>👤</Text>
          </View>
          <Text style={styles.userName}>Usuario</Text>
          <Text style={styles.userRole}>Conductor</Text>
          <TouchableOpacity style={styles.editButton} onPress={handleEditProfile}>
            <Text style={styles.editButtonText}>Editar Perfil</Text>
          </TouchableOpacity>
        </View>

        {/* Información Personal */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Información Personal</Text>

          <View style={styles.infoItem}>
            <View style={styles.infoIconContainer}>
              <Text style={styles.infoIcon}>👤</Text>
            </View>
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>Nombre completo</Text>
              <Text style={styles.infoValue}>{userData.name}</Text>
            </View>
          </View>

          <View style={styles.infoItem}>
            <View style={styles.infoIconContainer}>
              <Text style={styles.infoIcon}>✉️</Text>
            </View>
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>Correo electrónico</Text>
              <Text style={styles.infoValue}>{userData.email}</Text>
            </View>
          </View>

          <View style={styles.infoItem}>
            <View style={styles.infoIconContainer}>
              <Text style={styles.infoIcon}>📞</Text>
            </View>
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>Teléfono</Text>
              <Text style={styles.infoValue}>{userData.phone}</Text>
            </View>
          </View>

          <View style={styles.infoItem}>
            <View style={styles.infoIconContainer}>
              <Text style={styles.infoIcon}>📍</Text>
            </View>
            <View style={styles.infoContent}>
              <Text style={styles.infoLabel}>Ciudad</Text>
              <Text style={styles.infoValue}>{userData.city}</Text>
            </View>
          </View>
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
  userName: {
    fontSize: 22,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  userRole: {
    fontSize: 16,
    color: '#666',
    marginBottom: 20,
  },
  editButton: {
    paddingHorizontal: 30,
    paddingVertical: 10,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#2d4a75',
  },
  editButtonText: {
    fontSize: 16,
    color: '#2d4a75',
    fontWeight: '500',
  },
  section: {
    backgroundColor: '#fff',
    marginTop: 15,
    paddingVertical: 10,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    paddingHorizontal: 20,
    paddingVertical: 10,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  infoIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  infoIcon: {
    fontSize: 20,
  },
  infoContent: {
    flex: 1,
  },
  infoLabel: {
    fontSize: 14,
    color: '#999',
    marginBottom: 4,
  },
  infoValue: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
});