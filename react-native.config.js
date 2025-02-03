module.exports = {
  dependencies: {
    "react-native-vector-icons": {
      platforms: {
        ios: null, // Disable iOS linking
      },
    },
  },
  assets: ["./node_modules/react-native-vector-icons/Fonts"], // Manually add font assets
};
