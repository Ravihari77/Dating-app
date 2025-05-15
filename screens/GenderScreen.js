import {
  StyleSheet,
  Text,
  View,
  SafeAreaView,
  Image,
  Pressable,
  TouchableOpacity,
} from 'react-native';
import React, {useState, useEffect} from 'react';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import FontAwesome from 'react-native-vector-icons/FontAwesome';
import AntDesign from 'react-native-vector-icons/AntDesign';
import {useNavigation} from '@react-navigation/native';
import { getRegistrationProgress, saveRegistrationProgress } from '../registrationUtils';

const GenderScreen = () => {
  const [gender, setGender] = useState('');
  const [isVisibleOnProfile, setIsVisibleOnProfile] = useState(false);
  const navigation = useNavigation();

  useEffect(() => {
    getRegistrationProgress('Gender').then((progressData) => {
      if (progressData) {
        setGender(progressData.gender || '');
        setIsVisibleOnProfile(progressData.isVisibleOnProfile || false);
      }
    });
  }, []);

  const handleNext = () => {
    if (gender.trim() !== '') {
      // Save the current progress data including gender and visibility status
      saveRegistrationProgress('Gender', { gender, isVisibleOnProfile });
    }
    // Navigate to the next screen
    navigation.navigate('Type');
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: 'white' }}>
      <View style={{ marginTop: 90, marginHorizontal: 20 }}>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <View
            style={{
              width: 44,
              height: 44,
              borderRadius: 22,
              borderColor: 'black',
              borderWidth: 2,
              justifyContent: 'center',
              alignItems: 'center',
            }}>
            <MaterialCommunityIcons
              name="cake-variant-outline"
              size={26}
              color="black"
            />
          </View>
          <Image
            style={{ width: 100, height: 40 }}
            source={{
              uri: 'https://cdn-icons-png.flaticon.com/128/10613/10613685.png',
            }}
          />
        </View>
        <Text
          style={{
            fontSize: 25,
            fontWeight: 'bold',
            fontFamily: 'GeezaPro-Bold',
            marginTop: 15,
          }}>
          Which gender describes you the best?
        </Text>

        <Text style={{ marginTop: 30, fontSize: 15, color: 'gray' }}>
          "Date Me" users are matched based on these three gender groups. You can
          add more about gender later.
        </Text>

        <View style={{ marginTop: 30 }}>
          {['Men', 'Women', 'Non-binary'].map((item) => (
            <View
              key={item}
              style={{
                flexDirection: 'row',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginVertical: 6,
              }}>
              <Text style={{ fontWeight: '500', fontSize: 15 }}>{item}</Text>
              <Pressable onPress={() => setGender(item)}>
                <FontAwesome
                  name="circle"
                  size={26}
                  color={gender === item ? '#4B0082' : '#F0F0F0'}
                />
              </Pressable>
            </View>
          ))}
        </View>

        {/* Toggle visibility on profile */}
        <Pressable
          onPress={() => setIsVisibleOnProfile(!isVisibleOnProfile)}
          style={{
            marginTop: 30,
            flexDirection: 'row',
            alignItems: 'center',
            gap: 8,
          }}>
          <AntDesign
            name={isVisibleOnProfile ? 'checksquare' : 'checksquareo'}
            size={26}
            color="#4B0082"
          />
          <Text style={{ fontSize: 15 }}>Visible on profile</Text>
        </Pressable>

        <TouchableOpacity
          onPress={handleNext}
          activeOpacity={0.8}
          style={{ marginTop: 30, marginLeft: 'auto' }}>
          <MaterialCommunityIcons
            name="arrow-right-circle"
            size={45}
            color="#4B0082"
            style={{ alignSelf: 'center', marginTop: 20 }}
          />
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

export default GenderScreen;

const styles = StyleSheet.create({});
