import { createStackNavigator } from '@react-navigation/stack';
import ChatScreen from '../app/(tabs)/Vista_ChatBot';
import LoginScreen from '../app/(tabs)/Vista_Inicio_sesion';
import RegisterScreen from '../app/(tabs)/Vista_Registro';


const Stack = createStackNavigator();

export default function AppNavigator() {
  return (
    <Stack.Navigator
      initialRouteName="Login"
      screenOptions={{ headerShown: false }}
    >
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="Chat" component={ChatScreen} />
    </Stack.Navigator>
  );
}