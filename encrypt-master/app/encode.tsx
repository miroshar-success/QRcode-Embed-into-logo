import React, { useState, useEffect } from "react";
import {
  View,
  Image,
  Text,
  ScrollView,
  TouchableOpacity,
  Alert,
} from "react-native";
import { Buffer } from "buffer";
import * as ImagePicker from "expo-image-picker";
import { Camera } from "expo-camera";
import * as Sharing from "expo-sharing";
import {
  TextInput,
  Button,
  Appbar,
  Modal,
  Portal,
  ActivityIndicator,
} from "react-native-paper";
import { Feather, Ionicons } from "@expo/vector-icons";
import { encodeMessageIntoImage } from "@/servers/api";

if (typeof global.Buffer === "undefined") {
  global.Buffer = Buffer;
}

const App = () => {
  const [message, setMessage] = useState("");
  const [imageUri, setImageUri] = useState("");
  const [image, setImage] = useState("");
  const [hasPermission, setHasPermission] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  // 1. Select Image using Expo ImagePicker
  const selectImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });

    if (!result.canceled) {
      const { uri } = result.assets[0];
      setImageUri(uri);
    }
  };

  const handleEncode = async () => {
    if (imageUri) {
      setLoading(true);
      const imageUrl = await encodeMessageIntoImage(imageUri, message);
      setImage(imageUrl as string);
    }
    setLoading(false);
  };

  const download = async () => {
    console.log(image);
    // Prompt user to download or share the image
    if (await Sharing.isAvailableAsync()) {
      await Sharing.shareAsync(image, {
        mimeType: "image/png",
        dialogTitle: "Save QR Code Image",
      });
    } else {
      Alert.alert("Sharing is not available on this device.");
    }
  };

  if (hasPermission === null) {
    return <Text>Requesting camera permission</Text>;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <>
      <Appbar.Header>
        <Appbar.BackAction onPress={() => {}} />
        <Appbar.Content title="Encode" />
      </Appbar.Header>
      <ScrollView
        style={{ padding: 20 }}
        contentContainerStyle={{ padding: 20 }}
      >
        <View
          style={{
            marginBottom: 20,
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          {imageUri ? (
            <View
              style={{
                flex: 1,
                width: 200,
                height: 200,
                borderWidth: 1,
                borderRadius: 10,
              }}
            >
              <Image
                source={{ uri: imageUri }}
                style={{ width: "100%", height: "100%" }}
                resizeMode="contain"
              />
              <Feather
                name="edit"
                size={20}
                style={{
                  position: "absolute",
                  bottom: 5,
                  right: 5,
                  backgroundColor: "white",
                }}
                onPress={selectImage}
              />
            </View>
          ) : (
            <TouchableOpacity
              onPress={selectImage}
              style={{
                borderWidth: 1,
                borderStyle: "dashed",
                borderRadius: 10,
                justifyContent: "center",
                alignItems: "center",
                // height: 100,
                flex: 1,
              }}
            >
              <Ionicons name="image" size={20} />
              <Text style={{ fontWeight: "500" }}>
                {imageUri ? "Change" : "Add Image"}
              </Text>
            </TouchableOpacity>
          )}
        </View>

        <TextInput
          mode="outlined"
          placeholder="Enter message"
          value={message}
          onChangeText={(text) => setMessage(text)}
          style={{ marginBottom: 20 }}
        />
        <Button mode="contained" onPress={handleEncode}>
          Encode Image with QR Code
        </Button>
        <Portal>
          <Modal
            visible={Boolean(image)}
            onDismiss={() => setImage("")}
            contentContainerStyle={{
              backgroundColor: "white",
              padding: 20,
              justifyContent: "center",
              alignItems: "center",
              height: "80%",
            }}
          >
            <Text style={{ fontWeight: "500", marginBottom: 20 }}>
              Ecoded Image
            </Text>
            <Image
              source={{ uri: image }}
              style={{
                width: 200,
                height: 200,
                borderWidth: 2,
                marginBottom: 20,
              }}
            />
            <Button mode="contained" onPress={download}>
              Download
            </Button>
          </Modal>
        </Portal>
        <Portal>
          <Modal
            visible={loading}
            contentContainerStyle={{
              padding: 20,
              justifyContent: "center",
              alignItems: "center",
              backgroundColor: "white",
            }}
          >
            <Text style={{ marginBottom: 20 }}>Encoding message...</Text>
            <ActivityIndicator size={"large"} />
          </Modal>
        </Portal>
      </ScrollView>
    </>
  );
};

export default App;
