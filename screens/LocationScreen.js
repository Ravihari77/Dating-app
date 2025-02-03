import React, { useState, useEffect } from 'react';
import { View, Text, Button, PermissionsAndroid, Platform, ActivityIndicator } from 'react-native';
import Geolocation from '@react-native-community/geolocation';
import { useNavigation } from '@react-navigation/native';

const LocationScreen = () => {
  const [location, setLocation] = useState(null); // To store the fetched location
  const [loading, setLoading] = useState(false);  // To handle loading state
  const navigation = useNavigation(); // Navigation hook

  const requestLocationPermission = async () => {
    if (Platform.OS === 'android') {
      try {
        setLoading(true); // Show loading indicator while requesting permission
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
          {
            title: 'Location Permission',
            message: 'We need access to your location to provide better services.',
            buttonNeutral: 'Ask Me Later',
            buttonNegative: 'Cancel',
            buttonPositive: 'OK',
          }
        );

        if (granted === PermissionsAndroid.RESULTS.GRANTED) {
          console.log('Location permission granted');
          getLocation(); // Fetch the location if permission is granted
        } else {
          console.log('Location permission denied');
          setLoading(false); // Hide loading if permission is denied
        }
      } catch (err) {
        console.warn(err);
        setLoading(false); // Hide loading if there’s an error
      }
    }
  };

  const getLocation = () => {
    Geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setLocation({ latitude, longitude }); // Save the location to state
        setLoading(false); // Hide loading after location is fetched
        // After location is fetched, navigate to the Gender screen
        navigation.navigate('Gender', { latitude, longitude }); 
      },
      (error) => {
        console.error('Error getting location:', error);
        setLoading(false); // Hide loading on error
      },
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 }
    );
  };

  useEffect(() => {
    requestLocationPermission(); // Request permission on component mount
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" /> // Show loading indicator while fetching location
      ) : location ? (
        <Text>Location: {location.latitude}, {location.longitude}</Text> // Display location if available
      ) : (
        <Text>Location not available</Text>
      )}
    </View>
  );
};

export default LocationScreen;
