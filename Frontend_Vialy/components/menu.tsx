import { DrawerContentComponentProps } from '@react-navigation/drawer';
import React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

interface MenuItem {
  id: number;
  title: string;
  icon: string;
}

export default function CustomDrawer({ navigation }: DrawerContentComponentProps) {
  const menuItems: MenuItem[] = [
    { id: 1, title: 'Codigo de Transito', icon: '📋' },
    { id: 2, title: 'Infracciones Comunes', icon: '⚠️' },
    { id: 3, title: 'Como Conducir Apropiadamente', icon: '🚗' },
  ];

  const handleProfilePress = () => {
    navigation.navigate('Profile');
    navigation.closeDrawer();
  };
  const handleMenuItemPress = (item: MenuItem) => {
    console.log('Menu item pressed:', item.title);
    // Aquí puedes navegar o hacer lo que necesites
  };

  const handleNewConversation = () => {
    console.log('Nueva conversación');
    navigation.navigate('Chat');
  };

  const handleCloseDrawer = () => {
    navigation.closeDrawer();
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
            <Text style={styles.conversationsTitle}>Conversaciones</Text>
            <TouchableOpacity onPress={handleNewConversation}>
              <Text style={styles.addButton}>+</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity style={styles.conversationItem}>
            <View style={styles.conversationIconContainer}>
              <Text style={styles.conversationIcon}>💬</Text>
            </View>
            <View style={styles.conversationInfo}>
              <Text style={styles.conversationTitle}>Nueva conversación</Text>
              <Text style={styles.conversationSubtext}>Conversación nueva</Text>
              <Text style={styles.conversationTime}>Hoy</Text>
            </View>
          </TouchableOpacity>
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
  addButton: {
    fontSize: 24,
    color: '#2d4a75',
    fontWeight: '300',
  },
  conversationItem: {
    flexDirection: 'row',
    padding: 15,
    backgroundColor: '#e8f4f8',
    borderRadius: 12,
    marginBottom: 10,
  },
  conversationIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  conversationIcon: {
    fontSize: 20,
  },
  conversationInfo: {
    flex: 1,
  },
  conversationTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  conversationSubtext: {
    fontSize: 13,
    color: '#666',
    marginBottom: 2,
  },
  conversationTime: {
    fontSize: 12,
    color: '#999',
  },
});