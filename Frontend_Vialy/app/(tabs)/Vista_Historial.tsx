import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    FlatList,
    TouchableOpacity,
    ActivityIndicator,
    RefreshControl,
    Alert,
    Modal,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_ENDPOINTS, apiRequest } from '../../config/api';

interface Conversation {
    id: number;
    session_id: string;
    status: string;
    started_at: string;
    ended_at: string | null;
    message_count: number;
    last_message_preview: string;
    last_message_time: string;
}

interface Message {
    id: number;
    sender: 'usuario' | 'chatbot';
    message: string;
    created_at: string;
}

export default function Vista_Historial() {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [loadingMessages, setLoadingMessages] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);

    useEffect(() => {
        loadConversations();
    }, []);

    const loadConversations = async () => {
        try {
            const token = await AsyncStorage.getItem('access_token');
            if (!token) {
                Alert.alert('Error', 'No estás autenticado. Por favor inicia sesión.');
                return;
            }

            const data = await apiRequest(API_ENDPOINTS.CONVERSATIONS, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            setConversations(data);
        } catch (error) {
            console.error('Error cargando conversaciones:', error);
            Alert.alert('Error', 'No se pudieron cargar las conversaciones. Verifica tu conexión.');
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    const loadMessages = async (conversationId: number) => {
        setLoadingMessages(true);
        try {
            const token = await AsyncStorage.getItem('access_token');
            if (!token) {
                Alert.alert('Error', 'No estás autenticado');
                return;
            }

            const data = await apiRequest(`${API_ENDPOINTS.MESSAGES}/${conversationId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            setMessages(data);
            setModalVisible(true);
        } catch (error) {
            console.error('Error cargando mensajes:', error);
            Alert.alert('Error', 'No se pudieron cargar los mensajes');
        } finally {
            setLoadingMessages(false);
        }
    };

    const onRefresh = () => {
        setRefreshing(true);
        loadConversations();
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        if (date.toDateString() === today.toDateString()) {
            return `Hoy ${date.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })}`;
        } else if (date.toDateString() === yesterday.toDateString()) {
            return `Ayer ${date.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })}`;
        } else {
            return date.toLocaleDateString('es-CO', {
                day: '2-digit',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    };

    const openConversation = (conversation: Conversation) => {
        setSelectedConversation(conversation);
        loadMessages(conversation.id);
    };

    const closeModal = () => {
        setModalVisible(false);
        setSelectedConversation(null);
        setMessages([]);
    };

    const renderConversationItem = ({ item }: { item: Conversation }) => (
        <TouchableOpacity
            style={styles.conversationCard}
            onPress={() => openConversation(item)}
            activeOpacity={0.7}
        >
            <View style={styles.conversationHeader}>
                <View style={styles.iconContainer}>
                    <Ionicons name="chatbubbles" size={24} color="#2563EB" />
                </View>
                <View style={styles.conversationInfo}>
                    <View style={styles.titleRow}>
                        <Text style={styles.conversationDate}>
                            {formatDate(item.last_message_time)}
                        </Text>
                        {item.status === 'activa' && (
                            <View style={styles.activeBadge}>
                                <Text style={styles.activeBadgeText}>Activa</Text>
                            </View>
                        )}
                    </View>
                    <Text style={styles.messagePreview} numberOfLines={2}>
                        {item.last_message_preview}
                    </Text>
                    <View style={styles.conversationFooter}>
                        <Ionicons name="chatbox-outline" size={14} color="#6B7280" />
                        <Text style={styles.messageCount}>
                            {item.message_count} mensaje{item.message_count !== 1 ? 's' : ''}
                        </Text>
                    </View>
                </View>
                <Ionicons name="chevron-forward" size={20} color="#9CA3AF" />
            </View>
        </TouchableOpacity>
    );

    const renderMessage = ({ item }: { item: Message }) => (
        <View
            style={[
                styles.messageBubble,
                item.sender === 'usuario' ? styles.userMessage : styles.botMessage,
            ]}
        >
            <View style={styles.messageHeader}>
                <Text style={styles.messageSender}>
                    {item.sender === 'usuario' ? 'Tú' : 'Asistente'}
                </Text>
                <Text style={styles.messageTime}>
                    {new Date(item.created_at).toLocaleTimeString('es-CO', {
                        hour: '2-digit',
                        minute: '2-digit',
                    })}
                </Text>
            </View>
            <Text
                style={[
                    styles.messageText,
                    item.sender === 'usuario' ? styles.userMessageText : styles.botMessageText,
                ]}
            >
                {item.message}
            </Text>
        </View>
    );

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#2563EB" />
                <Text style={styles.loadingText}>Cargando conversaciones...</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Historial de Conversaciones</Text>
                <Text style={styles.headerSubtitle}>
                    {conversations.length} conversación{conversations.length !== 1 ? 'es' : ''}
                </Text>
            </View>

            {conversations.length === 0 ? (
                <View style={styles.emptyContainer}>
                    <Ionicons name="chatbubbles-outline" size={80} color="#D1D5DB" />
                    <Text style={styles.emptyTitle}>No hay conversaciones</Text>
                    <Text style={styles.emptyText}>
                        Tus conversaciones con el asistente aparecerán aquí
                    </Text>
                </View>
            ) : (
                <FlatList
                    data={conversations}
                    renderItem={renderConversationItem}
                    keyExtractor={(item) => item.id.toString()}
                    contentContainerStyle={styles.listContainer}
                    refreshControl={
                        <RefreshControl
                            refreshing={refreshing}
                            onRefresh={onRefresh}
                            colors={['#2563EB']}
                        />
                    }
                />
            )}

            {/* Modal para mostrar mensajes */}
            <Modal
                animationType="slide"
                transparent={false}
                visible={modalVisible}
                onRequestClose={closeModal}
            >
                <View style={styles.modalContainer}>
                    <View style={styles.modalHeader}>
                        <TouchableOpacity onPress={closeModal} style={styles.backButton}>
                            <Ionicons name="arrow-back" size={24} color="#1F2937" />
                        </TouchableOpacity>
                        <View style={styles.modalTitleContainer}>
                            <Text style={styles.modalTitle}>Conversación</Text>
                            {selectedConversation && (
                                <Text style={styles.modalSubtitle}>
                                    {formatDate(selectedConversation.started_at)}
                                </Text>
                            )}
                        </View>
                    </View>

                    {loadingMessages ? (
                        <View style={styles.centerContainer}>
                            <ActivityIndicator size="large" color="#2563EB" />
                        </View>
                    ) : (
                        <FlatList
                            data={messages}
                            renderItem={renderMessage}
                            keyExtractor={(item) => item.id.toString()}
                            contentContainerStyle={styles.messagesContainer}
                        />
                    )}
                </View>
            </Modal>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F9FAFB',
    },
    centerContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F9FAFB',
    },
    loadingText: {
        marginTop: 16,
        fontSize: 16,
        color: '#6B7280',
    },
    header: {
        backgroundColor: '#FFFFFF',
        padding: 20,
        paddingTop: 60,
        borderBottomWidth: 1,
        borderBottomColor: '#E5E7EB',
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: '700',
        color: '#1F2937',
        marginBottom: 4,
    },
    headerSubtitle: {
        fontSize: 14,
        color: '#6B7280',
    },
    listContainer: {
        padding: 16,
    },
    conversationCard: {
        backgroundColor: '#FFFFFF',
        borderRadius: 12,
        padding: 16,
        marginBottom: 12,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.05,
        shadowRadius: 8,
        elevation: 2,
    },
    conversationHeader: {
        flexDirection: 'row',
        alignItems: 'flex-start',
    },
    iconContainer: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: '#EFF6FF',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: 12,
    },
    conversationInfo: {
        flex: 1,
    },
    titleRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 8,
    },
    conversationDate: {
        fontSize: 14,
        fontWeight: '600',
        color: '#1F2937',
    },
    activeBadge: {
        backgroundColor: '#DEF7EC',
        paddingHorizontal: 8,
        paddingVertical: 2,
        borderRadius: 12,
    },
    activeBadgeText: {
        fontSize: 12,
        fontWeight: '600',
        color: '#03543F',
    },
    messagePreview: {
        fontSize: 14,
        color: '#6B7280',
        marginBottom: 8,
        lineHeight: 20,
    },
    conversationFooter: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    messageCount: {
        fontSize: 12,
        color: '#6B7280',
        marginLeft: 4,
    },
    emptyContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 32,
    },
    emptyTitle: {
        fontSize: 20,
        fontWeight: '600',
        color: '#1F2937',
        marginTop: 16,
        marginBottom: 8,
    },
    emptyText: {
        fontSize: 14,
        color: '#6B7280',
        textAlign: 'center',
    },
    // Modal styles
    modalContainer: {
        flex: 1,
        backgroundColor: '#F9FAFB',
    },
    modalHeader: {
        backgroundColor: '#FFFFFF',
        flexDirection: 'row',
        alignItems: 'center',
        paddingTop: 60,
        paddingBottom: 16,
        paddingHorizontal: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#E5E7EB',
    },
    backButton: {
        padding: 8,
        marginRight: 8,
    },
    modalTitleContainer: {
        flex: 1,
    },
    modalTitle: {
        fontSize: 20,
        fontWeight: '700',
        color: '#1F2937',
    },
    modalSubtitle: {
        fontSize: 14,
        color: '#6B7280',
        marginTop: 2,
    },
    messagesContainer: {
        padding: 16,
    },
    messageBubble: {
        marginBottom: 16,
        borderRadius: 12,
        padding: 12,
        maxWidth: '85%',
    },
    userMessage: {
        alignSelf: 'flex-end',
        backgroundColor: '#2563EB',
    },
    botMessage: {
        alignSelf: 'flex-start',
        backgroundColor: '#FFFFFF',
        borderWidth: 1,
        borderColor: '#E5E7EB',
    },
    messageHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 4,
    },
    messageSender: {
        fontSize: 12,
        fontWeight: '600',
        color: '#6B7280',
    },
    messageTime: {
        fontSize: 11,
        color: '#9CA3AF',
    },
    messageText: {
        fontSize: 14,
        lineHeight: 20,
    },
    userMessageText: {
        color: '#FFFFFF',
    },
    botMessageText: {
        color: '#1F2937',
    },
});
