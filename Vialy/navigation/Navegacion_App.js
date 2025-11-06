import EditProfileScreen from '@/app/(tabs)/Vista_Editar_Info';
import ProfileScreen from '@/app/(tabs)/Vista_Informacion_Usuario';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { createStackNavigator } from '@react-navigation/stack';
import React from 'react';
import ChatScreen from '../app/(tabs)/Vista_ChatBot';
import LoginScreen from '../app/(tabs)/Vista_Inicio_sesion';
import RegisterScreen from '../app/(tabs)/Vista_Registro';
import CustomDrawer from '../components/menu';


const Stack = createStackNavigator();
const Drawer = createDrawerNavigator();

function ChatDrawer() {
  return (
    <Drawer.Navigator
      drawerContent={(props) => <CustomDrawer {...props} />}
      screenOptions={{
        headerShown: false,
        drawerType: 'slide',
        drawerStyle: {
          width: '80%',
        },
      }}
    >
      <Drawer.Screen name="ChatMain" component={ChatScreen} />
    </Drawer.Navigator>
  );
}


export default function AppNavigator() {
  return (
      <Stack.Navigator
        initialRouteName="Login"
        screenOptions={{
          headerShown: false,
        }}
      >
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="Chat" component={ChatDrawer} />
        <Stack.Screen name="Profile" component={ProfileScreen}/>
        <Stack.Screen name="Edit_Profile" component={EditProfileScreen}/>
      </Stack.Navigator>
  );
}