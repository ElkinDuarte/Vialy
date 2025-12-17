import { DrawerNavigationProp } from '@react-navigation/drawer';
import { LinearGradient } from 'expo-linear-gradient';
import React, { useEffect, useRef } from 'react';
import {
  AppState,
  AppStateStatus,
  Keyboard,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

type InfractionsScreenProps = {
  navigation: DrawerNavigationProp<any>;
};

const INFRACCIONES_COMUNES = [
  {
    id: 1,
    titulo: '¿Qué es una infracción de tránsito?',
    pregunta: '¿Qué es una infracción de tránsito?',
  },
  {
    id: 2,
    titulo: 'Límites de velocidad',
    pregunta: '¿Cuáles son los límites de velocidad en Colombia?',
  },
  {
    id: 3,
    titulo: 'Estacionamiento prohibido',
    pregunta: '¿En dónde está prohibido estacionar según el código de tránsito?',
  },
  {
    id: 4,
    titulo: 'Documentación requerida',
    pregunta: '¿Qué documentos debo llevar cuando conduzco un vehículo?',
  },
  {
    id: 5,
    titulo: 'Multas y sanciones',
    pregunta: '¿Cuáles son las multas y sanciones por infracciones de tránsito?',
  },
  {
    id: 6,
    titulo: 'Casco de seguridad',
    pregunta: '¿Es obligatorio usar casco de seguridad en motocicleta?',
  },
  {
    id: 7,
    titulo: 'Cinturón de seguridad',
    pregunta: '¿Es obligatorio usar cinturón de seguridad en automóvil?',
  },
  {
    id: 8,
    titulo: 'Conducir bajo influencia',
    pregunta: '¿Cuáles son las consecuencias de conducir bajo influencia de alcohol?',
  },
  {
    id: 9,
    titulo: 'Luces del vehículo',
    pregunta: '¿Cuándo debo usar las luces del vehículo?',
  },
  {
    id: 10,
    titulo: 'Señales de tránsito',
    pregunta: '¿Cuál es el significado de las principales señales de tránsito?',
  },
];

export default function InfractionsScreen({ navigation }: InfractionsScreenProps) {
  const appState = useRef(AppState.currentState);

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
      Keyboard.dismiss();
    }
    appState.current = nextAppState;
  };

  const handleMenuPress = () => {
    navigation.openDrawer();
  };

  const handleSelectInfraction = (pregunta: string) => {
    navigation.navigate('ChatMain', {
      initialQuery: pregunta,
    });
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0A1F3E" translucent={false} />

      {/* Header */}
      <LinearGradient
        colors={['#0A1F3E', '#0A1F3E']}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <View style={styles.headerLeft}>
            <TouchableOpacity onPress={handleMenuPress} style={styles.menuButton}>
              <View style={styles.menuLine} />
              <View style={styles.menuLine} />
              <View style={styles.menuLine} />
            </TouchableOpacity>
          </View>

          <View style={styles.headerCenter}>
            <Text style={styles.headerTitle}>Infracciones Comunes</Text>
            <Text style={styles.headerSubtitle}>Preguntas frecuentes</Text>
          </View>
        </View>
      </LinearGradient>

      {/* Lista de infracciones */}
      <ScrollView 
        style={styles.content}
        showsVerticalScrollIndicator={true}
      >
        <View style={styles.listContainer}>
          {INFRACCIONES_COMUNES.map((infraccion) => (
            <TouchableOpacity
              key={infraccion.id}
              style={styles.infractionItem}
              onPress={() => handleSelectInfraction(infraccion.pregunta)}
              activeOpacity={0.7}
            >
              <View style={styles.itemContent}>
                <Text style={styles.itemTitle}>{infraccion.titulo}</Text>
                <Text style={styles.itemDescription}>{infraccion.pregunta}</Text>
              </View>
              <View style={styles.arrowContainer}>
                <Text style={styles.arrow}>→</Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {/* Espacio al final */}
        <View style={styles.bottomSpacing} />
      </ScrollView>
    </View>
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
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  menuButton: {
    padding: 8,
    marginRight: 12,
  },
  menuLine: {
    width: 24,
    height: 3,
    backgroundColor: '#fff',
    marginBottom: 4,
    borderRadius: 2,
  },
  headerCenter: {
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
  listContainer: {
    paddingHorizontal: 15,
    paddingVertical: 15,
  },
  infractionItem: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  itemContent: {
    flex: 1,
    marginRight: 12,
  },
  itemTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2d4a75',
    marginBottom: 6,
  },
  itemDescription: {
    fontSize: 13,
    color: '#666',
    lineHeight: 18,
  },
  arrowContainer: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#e8eef5',
    justifyContent: 'center',
    alignItems: 'center',
  },
  arrow: {
    fontSize: 18,
    color: '#2d4a75',
    fontWeight: '600',
  },
  bottomSpacing: {
    height: 20,
  },
});
