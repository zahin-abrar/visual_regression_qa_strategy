import { useState } from "react";
import { View } from "react-native";

import Typography from "#/components/ui/Typography";
import { radii } from "#/constants/BorderRadius";
import { spacing } from "#/constants/Spacing";

import { qaBreakingNews } from "./qaBreakingNews";
import { qaActiveScenario, qaFixtureEnabled } from "./qaScenario";

/** QA-only sample extension: no impression, action, expiry or dismiss behavior. */
const QaBreakingBanner = () => {
  const [containerReady, setContainerReady] = useState(false);
  const [titleReady, setTitleReady] = useState(false);
  if (!__DEV__ || !qaFixtureEnabled || qaActiveScenario !== "breaking_news") return null;

  return (
    <View
      testID={containerReady && titleReady ? "qa-breaking-banner-ready" : "qa-breaking-banner"}
      onLayout={({ nativeEvent: { layout } }) => setContainerReady(layout.width > 0 && layout.height > 0)}
      style={{
        padding: spacing.xl,
        gap: spacing.md,
        borderWidth: 2,
        borderColor: "#7A271A",
        borderRadius: radii.lg,
        backgroundColor: "#B42318",
      }}
    >
      <Typography type="heading" testID="qa-breaking-banner-label" style={{ color: "#FFFFFF" }}>
        {qaBreakingNews.label}
      </Typography>
      <Typography
        type="cardTitle"
        testID="qa-breaking-banner-title"
        accessibilityRole="header"
        onLayout={({ nativeEvent: { layout } }) => setTitleReady(layout.width > 0 && layout.height > 0)}
        style={{ color: "#FFFFFF" }}
      >
        {qaBreakingNews.title}
      </Typography>
    </View>
  );
};

export default QaBreakingBanner;
