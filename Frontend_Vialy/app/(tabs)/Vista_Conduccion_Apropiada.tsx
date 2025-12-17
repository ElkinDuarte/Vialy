import { DrawerNavigationProp } from '@react-navigation/drawer';
import { LinearGradient } from 'expo-linear-gradient';
import React, { useEffect, useRef, useState } from 'react';
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

type DrivingScreenProps = {
  navigation: DrawerNavigationProp<any>;
};

interface ConsejoItem {
  id: number;
  titulo: string;
  icono: string;
  contenido: string[];
}

const CONSEJOS_CONDUCCION: ConsejoItem[] = [
  {
    id: 1,
    titulo: 'Posición correcta al conducir',
    icono: '🪑',
    contenido: [
      '✓ Ajusta el asiento para que tus brazos queden ligeramente flexionados al agarrar el volante',
      '✓ El respaldo debe estar reclinado entre 100° y 110°',
      '✓ Los pies deben alcanzar cómodamente los pedales sin estirar las piernas',
      '✓ La cabeza debe estar a unos 25-30 cm del airbag',
      '✓ Usa reposacabezas para evitar lesiones en el cuello',
    ],
  },
  {
    id: 2,
    titulo: 'Uso correcto de los espejos',
    icono: '🪞',
    contenido: [
      '✓ Ajusta el espejo retrovisor para ver toda la luneta trasera',
      '✓ Los espejos laterales deben mostrar un poco de tu vehículo y la mayoría de la carretera',
      '✓ Revisa los espejos cada 5-8 segundos mientras conduces',
      '✓ Recuerda que los espejos laterales tienen puntos ciegos',
      '✓ Gira tu cabeza para verificar antes de cambiar de carril',
    ],
  },
  {
    id: 3,
    titulo: 'Técnica de frenado seguro',
    icono: '🛑',
    contenido: [
      '✓ Presiona el pedal de freno suavemente y de manera progresiva',
      '✓ No hagas frenazos abruptos a menos que sea una emergencia',
      '✓ Aumenta la distancia de frenado en condiciones mojadas o de hielo',
      '✓ Mantén el volante firme durante el frenado',
      '✓ Si pierdes los frenos, busca una pendiente hacia arriba o usa el freno de emergencia',
    ],
  },
  {
    id: 4,
    titulo: 'Conducción en lluvia',
    icono: '🌧️',
    contenido: [
      '✓ Reduce la velocidad y aumenta la distancia de seguimiento',
      '✓ Asegúrate de que los limpiaparabrisas funcionen correctamente',
      '✓ Enciende las luces bajas incluso durante el día',
      '✓ Evita frenar bruscamente en superficies mojadas',
      '✓ Ten cuidado con los charcos, pueden ocultar baches profundos',
    ],
  },
  {
    id: 5,
    titulo: 'Conducción nocturna',
    icono: '🌙',
    contenido: [
      '✓ Enciende los faros 30 minutos antes del anochecer',
      '✓ Reduce la velocidad para aumentar tu tiempo de reacción',
      '✓ Usa las luces altas solo en carreteras sin tráfico opuesto',
      '✓ Limpia regularmente los faros para máxima visibilidad',
      '✓ Descansa si te sientes cansado; la fatiga es peligrosa',
    ],
  },
  {
    id: 6,
    titulo: 'Cambios de carril seguros',
    icono: '↔️',
    contenido: [
      '✓ Verifica los espejos y gira la cabeza para ver puntos ciegos',
      '✓ Usa los intermitentes con 3-4 segundos de anticipación',
      '✓ Asegúrate de que hay suficiente espacio (al menos 1.5 veces la longitud del vehículo)',
      '✓ Realiza el cambio suavemente sin aceleraciones bruscas',
      '✓ Apaga el intermitente después de completar el cambio',
    ],
  },
  {
    id: 7,
    titulo: 'Distancia de seguridad',
    icono: '📏',
    contenido: [
      '✓ Mantén una distancia de al menos 2 segundos del vehículo delantero',
      '✓ En carreteras a alta velocidad, aumenta a 3-4 segundos',
      '✓ En lluvia o nieve, duplica la distancia normal',
      '✓ Usa la regla: Por cada 10 km/h, una longitud de vehículo',
      '✓ Mayor distancia = más tiempo para reaccionar ante emergencias',
    ],
  },
  {
    id: 8,
    titulo: 'Conducción defensiva',
    icono: '🛡️',
    contenido: [
      '✓ Anticipa las acciones de otros conductores',
      '✓ Mantén una velocidad constante y predecible',
      '✓ Busca rutas alternativas si hay mucho tráfico',
      '✓ No respondas agresivamente a los errores de otros',
      '✓ Mantén tu atención en la carretera, no distracciones',
    ],
  },
  {
    id: 9,
    titulo: 'Control del estrés y fatiga',
    icono: '😴',
    contenido: [
      '✓ Toma descansos cada 2 horas en viajes largos',
      '✓ Duerme lo suficiente antes de conducir largas distancias',
      '✓ Si sientes sueño, estaciona en un lugar seguro y descansa',
      '✓ Mantén la cabina a temperatura moderada',
      '✓ Escucha música para mantenerte alerta pero concentrado',
    ],
  },
  {
    id: 10,
    titulo: 'Mantenimiento del vehículo',
    icono: '🔧',
    contenido: [
      '✓ Revisa el nivel de aceite cada mes',
      '✓ Verifica la presión de llantas mensualmente',
      '✓ Cambia el filtro de aire cada 15,000-30,000 km',
      '✓ Inspecciona los frenos regularmente',
      '✓ Realiza servicio completo cada 10,000-15,000 km',
    ],
  },
  {
    id: 11,
    titulo: 'Conducción en carreteras',
    icono: '🛣️',
    contenido: [
      '✓ Aumenta la distancia de seguimiento en carreteras',
      '✓ Usa los intermitentes al cambiar de carril o virar',
      '✓ Mantén una velocidad constante y moderada',
      '✓ Ten cuidado en curvas: reduce velocidad antes de entrar',
      '✓ En autopistas, mantén el carril derecho excepto para adelantar',
    ],
  },
  {
    id: 12,
    titulo: 'Conducción en pendientes',
    icono: '⛰️',
    contenido: [
      '✓ En bajadas, usa cambios bajos para usar el freno motor',
      '✓ No mantengas presionado el pedal de freno continuamente',
      '✓ En subidas, acelera suavemente para mantener el impulso',
      '✓ Ten cuidado con los puntos ciegos en curvas de montaña',
      '✓ Cede el paso a vehículos que suben si es posible',
    ],
  },
];

export default function DrivingScreen({ navigation }: DrivingScreenProps) {
  const appState = useRef(AppState.currentState);
  const [expandedId, setExpandedId] = useState<number | null>(null);

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

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
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
            <Text style={styles.headerTitle}>Conducción Segura</Text>
            <Text style={styles.headerSubtitle}>Guía completa</Text>
          </View>
        </View>
      </LinearGradient>

      {/* Lista de consejos expandibles */}
      <ScrollView 
        style={styles.content}
        showsVerticalScrollIndicator={true}
      >
        <View style={styles.listContainer}>
          {CONSEJOS_CONDUCCION.map((consejo) => (
            <View key={consejo.id}>
              <TouchableOpacity
                style={styles.consejoHeader}
                onPress={() => toggleExpand(consejo.id)}
                activeOpacity={0.7}
              >
                <View style={styles.headerLeftContent}>
                  <Text style={styles.icono}>{consejo.icono}</Text>
                  <Text style={styles.itemTitle}>{consejo.titulo}</Text>
                </View>
                <Text style={[
                  styles.expandIcon,
                  expandedId === consejo.id && styles.expandIconRotated
                ]}>
                  ▼
                </Text>
              </TouchableOpacity>

              {expandedId === consejo.id && (
                <View style={styles.consejoContent}>
                  {consejo.contenido.map((linea, index) => (
                    <Text key={index} style={styles.contenidoLinea}>
                      {linea}
                    </Text>
                  ))}
                </View>
              )}
            </View>
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
  consejoHeader: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  headerLeftContent: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  icono: {
    fontSize: 24,
    marginRight: 12,
  },
  itemTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2d4a75',
    flex: 1,
  },
  expandIcon: {
    fontSize: 16,
    color: '#2d4a75',
    fontWeight: '600',
  },
  expandIconRotated: {
    transform: [{ rotate: '180deg' }],
  },
  consejoContent: {
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    marginTop: -8,
    borderLeftWidth: 4,
    borderLeftColor: '#2d4a75',
  },
  contenidoLinea: {
    fontSize: 14,
    color: '#333',
    lineHeight: 22,
    marginBottom: 8,
  },
  bottomSpacing: {
    height: 20,
  },
});
