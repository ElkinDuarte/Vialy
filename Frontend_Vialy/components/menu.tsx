import { DrawerContentComponentProps } from '@react-navigation/drawer';
import React, { useState, useEffect } from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  ActivityIndicator,
  Alert
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_ENDPOINTS, apiRequest } from '../config/api';
import { useFocusEffect } from '@react-navigation/native';

interface MenuItem {
  id: number;
  title: string;
  icon: string;
}

interface Conversation {
  id: number;
  session_id: string;
  status: string;
  started_at: string;
  last_message_preview?: string;
  last_message_time?: string;
  message_count?: number;
}

export default function CustomDrawer({ navigation }: DrawerContentComponentProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loadingConversations, setLoadingConversations] = useState(false);

  const menuItems: MenuItem[] = [
    { id: 1, title: 'Codigo de Transito', icon: '📋' },
    { id: 2, title: 'Infracciones Comunes', icon: '⚠️' },
    { id: 3, title: 'Como Conducir Apropiadamente', icon: '🚗' },
  ];

  // Cargar conversaciones cada vez que se abre el menú
  useFocusEffect(
    React.useCallback(() => {
      loadConversations();
    }, [])
  );

  const loadConversations = async () => {
    setLoadingConversations(true);
    try {
      const token = await AsyncStorage.getItem('access_token');
      if (token) {
        const data = await apiRequest(API_ENDPOINTS.CONVERSATIONS, {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${token}` }
        });
        setConversations(data);
      }
    } catch (error) {
      console.error('Error cargando conversaciones en menú:', error);
    } finally {
      setLoadingConversations(false);
    }
  };

  const handleProfilePress = () => {
    navigation.navigate('Profile');
    navigation.closeDrawer();
  };

  const handleMenuItemPress = (item: MenuItem) => {
    if (item.id === 1) {
      navigation.navigate('CodigoTransito');
    } else if (item.id === 2) {
      navigation.navigate('Infractions');
    } else if (item.id === 3) {
      navigation.navigate('Driving');
    }
    navigation.closeDrawer();
  };

  const handleNewConversation = async () => {
    // Generar nueva sesión limpia
    await AsyncStorage.removeItem('current_session_id');
    navigation.navigate('ChatMain', { sessionId: null, reset: true, timestamp: Date.now() });
    navigation.closeDrawer();
  };

  const handleConversationPress = (conversation: Conversation) => {
    console.log('Navegando a conversación:', conversation.id, conversation.session_id);
    // Navegar al chat con el ID de sesión específico para cargar historial
    navigation.navigate('ChatMain', {
      sessionId: conversation.session_id,
      conversationId: conversation.id, // ID numérico de BD
      reset: true, // Forzar recarga
      timestamp: Date.now() // Forzar actualización de params
    });
    navigation.closeDrawer();
  };

  const handleCloseDrawer = () => {
    navigation.closeDrawer();
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const today = new Date();

    if (date.toDateString() === today.toDateString()) {
      return date.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' });
    }
    return date.toLocaleDateString('es-CO', { day: '2-digit', month: '2-digit' });
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.profileContainer}
          onPress={handleProfilePress}
        >
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>👤</Text>
          </View>
          <View style={styles.profileInfo}>
            <Text style={styles.profileName}>Mi Perfil</Text>
            <Text style={styles.profileSubtext}>Ver información personal</Text>
          </View>
        </TouchableOpacity>
        <TouchableOpacity onPress={handleCloseDrawer} style={styles.closeButton}>
          <Text style={styles.closeButtonText}>✕</Text>
        </TouchableOpacity>
      </View>

      {/* Menu Items */}
      <ScrollView style={styles.menuContainer}>
        {menuItems.map((item) => (
          <TouchableOpacity
            key={item.id}
            style={styles.menuItem}
            onPress={() => handleMenuItemPress(item)}
          >
            <View style={styles.menuIconContainer}>
              <Text style={styles.menuIcon}>{item.icon}</Text>
            </View>
            <Text style={styles.menuItemText}>{item.title}</Text>
          </TouchableOpacity>
        ))}

        {/* Conversaciones Section */}
        <View style={styles.conversationsSection}>
          <View style={styles.conversationsHeader}>
            <Text style={styles.conversationsTitle}>Historial de Conversaciones</Text>
            <TouchableOpacity onPress={handleNewConversation}>
              <View style={styles.addButtonContainer}>
                <Text style={styles.addButton}>+</Text>
              </View>
            </TouchableOpacity>
          </View>

          {loadingConversations ? (
            <ActivityIndicator size="small" color="#2d4a75" style={{ marginTop: 10 }} />
          ) : conversations.length === 0 ? (
            <Text style={styles.noConversationsText}>No tienes conversaciones recientes</Text>
          ) : (
            conversations.map((conv) => (
              <TouchableOpacity
                key={conv.id}
                style={styles.conversationItem}
                onPress={() => handleConversationPress(conv)}
              >
                <View style={styles.conversationIconContainer}>
                  <Text style={styles.conversationIcon}>💬</Text>
                </View>
                <View style={styles.conversationInfo}>
                  <Text style={styles.conversationTitle} numberOfLines={1}>
                    {conv.last_message_preview || "Conversación nueva"}
                  </Text>
                  <Text style={styles.conversationSubtext} numberOfLines={1}>
                    {conv.message_count ? `${conv.message_count} mensajes` : 'Sin mensajes'} • {conv.status === 'activa' ? 'En curso' : 'Finalizada'}
                  </Text>
                  <Text style={styles.conversationTime}>
                    {formatDate(conv.last_message_time || conv.started_at)}
                  </Text>
                </View>
              </TouchableOpacity>
            ))
          )}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    backgroundColor: '#2d4a75',
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  profileContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#5eb3f6',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  avatarText: {
    fontSize: 28,
  },
  profileInfo: {
    flex: 1,
  },
  profileName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  profileSubtext: {
    fontSize: 13,
    color: 'rgba(255, 255, 255, 0.8)',
  },
  closeButton: {
    padding: 5,
  },
  closeButtonText: {
    fontSize: 24,
    color: '#fff',
    fontWeight: '300',
  },
  menuContainer: {
    flex: 1,
    paddingTop: 10,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  menuIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: '#e8f4f8',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  menuIcon: {
    fontSize: 20,
  },
  menuItemText: {
    fontSize: 16,
    color: '#333',
    flex: 1,
  },
  conversationsSection: {
    marginTop: 20,
    paddingHorizontal: 20,
    paddingBottom: 30,
  },
  conversationsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  conversationsTitle: {
    fontSize: 14,
    color: '#999',
    fontWeight: '600',
  },
  addButtonContainer: {
    backgroundColor: '#e8f4f8',
    width: 30,
    height: 30,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
  },
  addButton: {
    fontSize: 20,
    color: '#2d4a75',
    fontWeight: '600',
    marginTop: -2,
  },
  conversationItem: {
    flexDirection: 'row',
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 12,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#eee',
  },
  conversationIconContainer: {
    width: 36,
    height: 36,
    borderRadius: 8,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
    borderWidth: 1,
    borderColor: '#eee',
  },
  conversationIcon: {
    fontSize: 18,
  },
  conversationInfo: {
    flex: 1,
  },
  conversationTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  conversationSubtext: {
    fontSize: 12,
    color: '#666',
    marginBottom: 2,
  },
  conversationTime: {
    fontSize: 11,
    color: '#999',
    textAlign: 'right',
    marginTop: -16,
  },
  noConversationsText: {
    fontSize: 13,
    color: '#999',
    fontStyle: 'italic',
    textAlign: 'center',
    marginTop: 10,
  }
});