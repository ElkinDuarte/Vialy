import React, { useState, useEffect, useRef } from 'react';
import {
  AppState,
  AppStateStatus,
  Keyboard,
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
  Platform,
  Linking,
  Alert
} from 'react-native';
import { WebView } from 'react-native-webview';
import { LinearGradient } from 'expo-linear-gradient';
import { DrawerNavigationProp } from '@react-navigation/drawer';
import { getBaseUrl } from '../../config/api';

type CodigoTransitoScreenProps = {
  navigation: DrawerNavigationProp<any>;
};

const BASE_URL = getBaseUrl();
const PDF_FILENAME = 'codigo_transito.pdf'; 
const PDF_URL = `${BASE_URL}/pdf/view/${PDF_FILENAME}`;

export default function CodigoTransitoScreen({ navigation }: CodigoTransitoScreenProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const isIOS = Platform.OS === 'ios';
  const appState = useRef(AppState.currentState);

  // En Android, abrir automáticamente el PDF al cargar la pantalla
  useEffect(() => {
    const subscription = AppState.addEventListener('change', handleAppStateChange);
    
    if (!isIOS) {
      setLoading(false);
    }
    
    return () => {
      subscription.remove();
    };
  }, [isIOS]);

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

  const handleMenuPress = () => {
    navigation.openDrawer();
  };

  const handleDownload = () => {
    Alert.alert(
      'Descargar PDF',
      '¿Deseas descargar el Código de Tránsito?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Descargar',
          onPress: async () => {
            try {
              const downloadUrl = `${BASE_URL}/pdf/download/${PDF_FILENAME}`;
              await Linking.openURL(downloadUrl);
            } catch (err) {
              Alert.alert('Error', 'No se pudo descargar el PDF');
            }
          }
        }
      ]
    );
  };

  const handleOpenExternal = async () => {
    try {
      const supported = await Linking.canOpenURL(PDF_URL);
      if (supported) {
        await Linking.openURL(PDF_URL);
      } else {
        Alert.alert('Error', 'No se puede abrir el PDF');
      }
    } catch (err) {
      Alert.alert('Error', 'No se pudo abrir el PDF');
    }
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
            
            <Text style={styles.headerTitle}>Código de Tránsito</Text>
          </View>

          <View style={styles.headerRight}>
            <TouchableOpacity
              onPress={handleOpenExternal}
              style={styles.iconButton}
            >
              <Text style={styles.iconText}>🌐</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              onPress={handleDownload}
              style={styles.iconButton}
            >
              <Text style={styles.iconText}>⬇️</Text>
            </TouchableOpacity>
          </View>
        </View>
      </LinearGradient>

      {/* PDF Viewer - Solo para iOS */}
      <View style={styles.content}>
        {isIOS && loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#2d4a75" />
            <Text style={styles.loadingText}>Cargando Código de Tránsito...</Text>
          </View>
        )}

        {isIOS && error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorIcon}>⚠️</Text>
            <Text style={styles.errorTitle}>Error al cargar el PDF</Text>
            <Text style={styles.errorText}>
              No se pudo cargar el documento.{'\n'}
              Verifica tu conexión a internet.
            </Text>
            <TouchableOpacity
              style={styles.retryButton}
              onPress={() => {
                setError(false);
                setLoading(true);
              }}
            >
              <Text style={styles.retryButtonText}>Reintentar</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.openExternalButton}
              onPress={handleOpenExternal}
            >
              <Text style={styles.openExternalText}>Abrir en navegador</Text>
            </TouchableOpacity>
          </View>
        )}
        
        {/* WebView solo para iOS */}
        {isIOS && !error && (
          <WebView
            source={{ uri: PDF_URL }}
            style={styles.webview}
            onLoadStart={() => setLoading(true)}
            onLoadEnd={() => setLoading(false)}
            onError={(syntheticEvent) => {
              const { nativeEvent } = syntheticEvent;
              console.error('WebView error: ', nativeEvent);
              setLoading(false);
              setError(true);
            }}
            javaScriptEnabled={true}
            domStorageEnabled={true}
            startInLoadingState={true}
            scalesPageToFit={true}
          />
        )}

        {/* Pantalla para Android - abrir PDF externamente */}
        {!isIOS && (
          <View style={styles.androidContainer}>
            <View style={styles.pdfIconContainer}>
              <Text style={styles.pdfIconLarge}>📄</Text>
            </View>
            <Text style={styles.androidTitle}>Código Nacional de Tránsito</Text>
            <Text style={styles.androidSubtitle}>
              Toca el botón para abrir el documento{'\n'}en tu visor de PDFs
            </Text>
            <TouchableOpacity
              style={styles.openPdfButton}
              onPress={handleOpenExternal}
            >
              <Text style={styles.openPdfButtonText}>📖 Abrir PDF</Text>
            </TouchableOpacity>
            
            <View style={styles.orDivider}>
              <View style={styles.dividerLine} />
              <Text style={styles.orText}>o</Text>
              <View style={styles.dividerLine} />
            </View>

            <TouchableOpacity
              style={styles.downloadButton}
              onPress={handleDownload}
            >
              <Text style={styles.downloadButtonText}>⬇️ Descargar PDF</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>

      {/* Info footer - solo para iOS cuando carga bien */}
      {isIOS && !loading && !error && (
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            📄 Código Nacional de Tránsito Colombiano
          </Text>
        </View>
      )}
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
    justifyContent: 'space-between',
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  headerRight: {
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
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    flex: 1,
  },
  iconButton: {
    padding: 8,
    marginLeft: 8,
  },
  iconText: {
    fontSize: 20,
  },
  content: {
    flex: 1,
    backgroundColor: '#fff',
  },
  webview: {
    flex: 1,
    backgroundColor: '#fff',
  },
  loadingContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
    zIndex: 1000,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',
  },
  errorIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  errorTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  errorText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 24,
  },
  retryButton: {
    backgroundColor: '#2d4a75',
    paddingHorizontal: 32,
    paddingVertical: 12,
    borderRadius: 8,
    marginBottom: 12,
  },
  retryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  openExternalButton: {
    paddingHorizontal: 32,
    paddingVertical: 12,
  },
  openExternalText: {
    color: '#2d4a75',
    fontSize: 16,
    fontWeight: '600',
  },
  footer: {
    backgroundColor: '#e8eef5',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  footerText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  // Estilos nuevos para Android
  androidContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
    backgroundColor: '#fff',
  },
  pdfIconContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#e8f4f8',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
  },
  pdfIconLarge: {
    fontSize: 64,
  },
  androidTitle: {
    fontSize: 22,
    fontWeight: '600',
    color: '#333',
    textAlign: 'center',
    marginBottom: 12,
  },
  androidSubtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 32,
    lineHeight: 24,
  },
  openPdfButton: {
    backgroundColor: '#2d4a75',
    paddingHorizontal: 40,
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 16,
    minWidth: 200,
  },
  openPdfButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    textAlign: 'center',
  },
  orDivider: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 20,
    width: '100%',
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: '#ddd',
  },
  orText: {
    marginHorizontal: 16,
    fontSize: 14,
    color: '#999',
  },
  downloadButton: {
    borderWidth: 2,
    borderColor: '#2d4a75',
    paddingHorizontal: 40,
    paddingVertical: 14,
    borderRadius: 12,
    minWidth: 200,
  },
  downloadButtonText: {
    color: '#2d4a75',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
});
