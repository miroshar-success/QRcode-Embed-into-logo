import React, { useState, useEffect } from "react";
import { View, Text, ScrollView } from "react-native";
import { Buffer } from "buffer";
import * as ImagePicker from "expo-image-picker";
import { Camera } from "expo-camera";
import {
  ActivityIndicator,
  Appbar,
  Button,
  Portal,
  Modal,
} from "react-native-paper";
import { decodeMessageFromImage } from "@/servers/api";

if (typeof global.Buffer === "undefined") {
  global.Buffer = Buffer;
}

const App = () => {
  const [hasPermission, setHasPermission] = useState(false);
  const [decodedMessage, setDecodedMessage] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  // 7. Decode the QR Code from the Image
  const extractQRCodeFromImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });

    if (result.canceled) return;
    setLoading(true);
    const { uri } = result.assets[0];

    if (uri) {
      setLoading(true);
      const message = await decodeMessageFromImage(uri);
      setDecodedMessage(message as string);
    }

    setLoading(false);
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
        <Appbar.Content title="Decode" />
      </Appbar.Header>
      <ScrollView
        style={{ padding: 20 }}
        contentContainerStyle={{ padding: 20 }}
      >
        <Button mode="contained" onPress={extractQRCodeFromImage}>
          Decode Image
        </Button>

        {decodedMessage && (
          <View style={{ marginTop: 30 }}>
            <Text>Decoded Message from QR Code:</Text>
            <Text>{decodedMessage}</Text>
          </View>
        )}
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
            <Text style={{ marginBottom: 20 }}>Decoding message...</Text>
            <ActivityIndicator size={"large"} />
          </Modal>
        </Portal>
      </ScrollView>
    </>
  );
};

export default App;
