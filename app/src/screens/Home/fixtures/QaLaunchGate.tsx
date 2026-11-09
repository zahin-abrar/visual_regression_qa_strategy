import * as SplashScreen from "expo-splash-screen";
import { type PropsWithChildren, useEffect, useState } from "react";
import { Linking, Text, View } from "react-native";

import { initializeQaScenario, type QaSelection } from "./qaScenario";

/** Nothing below this gate (including providers/effects/feed) mounts until resolved. */
const QaLaunchGate = ({ children }: PropsWithChildren) => {
  const [selection, setSelection] = useState<QaSelection | null>(null);
  useEffect(() => {
    let mounted = true;
    initializeQaScenario(() => Linking.getInitialURL()).then((resolved) => {
      if (mounted) setSelection(resolved);
    });
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    if (selection?.status === "invalid" || selection?.status === "unsupported") {
      void SplashScreen.hideAsync();
    }
  }, [selection]);

  useEffect(() => {
    if (selection?.status === "active") {
      // Development-only diagnostic: JS has rendered the identity marker (Appium exposure is separate).
      console.info(`[qa-scenario] marker rendered qa-scenario:${selection.id}`);
    }
  }, [selection]);

  if (!selection) return null;
  if (selection.status === "invalid" || selection.status === "unsupported") {
    // No providers, normal feeds, fixture requests or article-ready identifiers.
    return (
      <View style={{ flex: 1, justifyContent: "center", padding: 24 }}>
        <Text testID={`qa-scenario-${selection.status}`}>
          QA scenario unavailable: {selection.id ?? "invalid launch selection"}
        </Text>
      </View>
    );
  }
  return (
    <>
      {children}
      {selection.status === "active" && (
        <View
          accessible
          accessibilityLabel={`qa-scenario:${selection.id}`}
          testID={`qa-scenario-${selection.id}`}
          pointerEvents="none"
          // Keep accessibility bounds below the system status bar and left of the card.
          style={{ position: "absolute", top: 64, left: 0, width: 1, height: 1, zIndex: 1 }}
        />
      )}
    </>
  );
};

export default QaLaunchGate;
