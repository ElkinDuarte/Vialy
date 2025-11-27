import { DrawerNavigationProp } from '@react-navigation/drawer';
import { LinearGradient } from 'expo-linear-gradient';
import React, { useRef, useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View
} from 'react-native';
import SendSvg from '../../assets/images/btn_enviar.svg';
import LogoSvg from '../../assets/images/logo.svg';
import { apiRequest, API_ENDPOINTS } from '../../config/api';


interface Message {
  id: number;
  text: string;
  isBot: boolean;
  timestamp: Date;
  sources?: Array<{
    extracto: string;
    pagina: string | null;
    archivo: string;
  }>;
}

type ChatScreenProps = {
  navigation: DrawerNavigationProp<any>;
};


export default function ChatScreen({ navigation }: ChatScreenProps) {
  const [message, setMessage] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: '¡Hola! Soy tu asistente del Código Nacional de Tránsito de Colombia. ¿En qué puedo ayudarte?',
      isBot: true,
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  const scrollViewRef = useRef<ScrollView>(null);

  // Función para enviar mensaje a la API
  const sendMessageToAPI = async (userMessage: string) => {
    try {
      setIsLoading(true);

      const data = await apiRequest(API_ENDPOINTS.ASK, {
        method: 'POST',
        body: JSON.stringify({
          query: userMessage
        }),
      });

      // Crear mensaje del bot con la respuesta
      const botResponse: Message = {
        id: messages.length + 2,
        text: data.response || data.message || "Sin respuesta del servidor.",
        isBot: true,
        timestamp: new Date(),
        sources: data.context_used ? data.sources : undefined
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error('Error al comunicarse con la API:', error);
      
      // Mensaje de error amigable
      const errorMessage: Message = {
        id: messages.length + 2,
        text: 'Lo siento, hubo un problema al procesar tu consulta. Por favor, intenta nuevamente.',
        isBot: true,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      
      Alert.alert(
        'Error de conexión',
        'No se pudo conectar con el servidor. Verifica tu conexión e intenta nuevamente.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (message.trim() && !isLoading) {
      const userMessage: Message = {
        id: messages.length + 1,
        text: message,
        isBot: false,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, userMessage]);
      const currentMessage = message;
      setMessage('');
      
      // Enviar mensaje a la API
      await sendMessageToAPI(currentMessage);
    }
  };

  const handleMenuPress = () => {
    navigation.openDrawer();
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      
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
            
            <View style={styles.logoIcon}>
              <LogoSvg width={40} height={40} />
            </View>
          </View>

          <View style={styles.headerCenter}>
            <Text style={styles.headerTitle}>Asistente de Transito</Text>
            <Text style={styles.headerSubtitle}>Colombia</Text>
          </View>
        </View>
      </LinearGradient>

      {/* Chat de mensajes */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
        onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
      >
        {messages.map((msg) => (
          <View key={msg.id}>
            <View
              style={[
                styles.messageRow,
                msg.isBot ? styles.botMessageRow : styles.userMessageRow
              ]}
            >
              {msg.isBot && (
                <View style={styles.botAvatar}>
                  <Text style={styles.botAvatarText}>🤖</Text>
                </View>
              )}
              
              <View
                style={[
                  styles.messageBubble,
                  msg.isBot ? styles.botBubble : styles.userBubble
                ]}
              >
                <Text
                  style={[
                    styles.messageText,
                    msg.isBot ? styles.botText : styles.userText
                  ]}
                >
                  {msg.text}
                </Text>
              </View>

              {!msg.isBot && (
                <View style={styles.userAvatar}>
                  <Text style={styles.userAvatarText}>👤</Text>
                </View>
              )}
            </View>

            {/* Mostrar fuentes si existen */}
            {msg.isBot && msg.sources && msg.sources.length > 0 && (
              <View style={styles.sourcesContainer}>
                <Text style={styles.sourcesTitle}>📚 Fuentes consultadas:</Text>
                {msg.sources.map((source, index) => (
                  <View key={index} style={styles.sourceItem}>
                    <Text style={styles.sourceText}>
                      • {source.archivo}
                      {source.pagina && ` (Pág. ${source.pagina})`}
                    </Text>
                  </View>
                ))}
              </View>
            )}
          </View>
        ))}

        {/* Indicador de carga */}
        {isLoading && (
          <View style={styles.loadingContainer}>
            <View style={styles.botAvatar}>
              <Text style={styles.botAvatarText}>🤖</Text>
            </View>
            <View style={styles.loadingBubble}>
              <ActivityIndicator size="small" color="#2d4a75" />
              <Text style={styles.loadingText}>Consultando...</Text>
            </View>
          </View>
        )}
      </ScrollView>

      {/* Area de mensajes de entrada*/}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 0}
      >
        <View style={styles.inputContainer}>
          <View style={styles.inputWrapper}>
            <TextInput
              style={styles.input}
              value={message}
              onChangeText={setMessage}
              placeholder="Escribe tu Consulta"
              placeholderTextColor="#999"
              multiline
              editable={!isLoading}
            />
            <TouchableOpacity
              style={[
                styles.sendButton,
                (isLoading || !message.trim()) && styles.sendButtonDisabled
              ]}
              onPress={handleSendMessage}
              disabled={isLoading || !message.trim()}
            >
              {isLoading ? (
                <ActivityIndicator size="small" color="#fff" />
              ) : (
                <SendSvg width={30} height={20} color={'white'}/>
              )}
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
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
  logoIcon: {
    width: 40,
    height: 40,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
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
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 15,
  },
  messageRow: {
    flexDirection: 'row',
    marginBottom: 15,
    alignItems: 'flex-end',
  },
  botMessageRow: {
    justifyContent: 'flex-start',
  },
  userMessageRow: {
    justifyContent: 'flex-end',
  },
  botAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#e8eef5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },
  botAvatarText: {
    fontSize: 20,
  },
  userAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#e8eef5',
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 8,
  },
  userAvatarText: {
    fontSize: 20,
  },
  messageBubble: {
    maxWidth: '70%',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
  },
  botBubble: {
    backgroundColor: '#e8eef5',
    borderBottomLeftRadius: 4,
  },
  userBubble: {
    backgroundColor: '#2d4a75',
    borderBottomRightRadius: 4,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  botText: {
    color: '#333',
  },
  userText: {
    color: '#fff',
  },
  sourcesContainer: {
    marginLeft: 44,
    marginBottom: 15,
    marginTop: -10,
    backgroundColor: '#f9f9f9',
    borderRadius: 10,
    padding: 10,
    borderLeftWidth: 3,
    borderLeftColor: '#2d4a75',
  },
  sourcesTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#666',
    marginBottom: 5,
  },
  sourceItem: {
    marginTop: 3,
  },
  sourceText: {
    fontSize: 11,
    color: '#888',
    lineHeight: 16,
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  loadingBubble: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e8eef5',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
    borderBottomLeftRadius: 4,
  },
  loadingText: {
    marginLeft: 8,
    fontSize: 14,
    color: '#666',
  },
  inputContainer: {
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    paddingHorizontal: 15,
    paddingVertical: 10,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f0f0',
    borderRadius: 25,
    paddingHorizontal: 15,
    paddingVertical: 8,
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: '#333',
    maxHeight: 100,
    paddingVertical: 8,
  },
  sendButton: {
    width: 44,
    height: 44,
    backgroundColor: '#2d4a75',
    borderRadius: 17,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 8,
  },
  sendButtonDisabled: {
    backgroundColor: '#a0a0a0',
  },
});