import { StyleSheet, Text, View } from "react-native";
import React from "react";
import { Button } from "react-native-paper";
import { router } from "expo-router";

const Index = () => {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        gap: 10,
        padding: 20,
      }}
    >
      <Button
        mode="contained"
        style={{ width: "100%" }}
        onPress={() => router.push("/encode")}
      >
        Encode
      </Button>
      <Button
        mode="contained"
        style={{ width: "100%" }}
        onPress={() => router.push("/decode")}
      >
        Decode
      </Button>
    </View>
  );
};

export default Index;

const styles = StyleSheet.create({});
