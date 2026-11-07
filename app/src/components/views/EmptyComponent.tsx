import React, { type ReactNode } from "react";
import { type LayoutChangeEvent, View } from "react-native";

import { HeartIcon } from "#/components/Icons";
import UiCard from "#/components/ui/UiCard";
import UiEmptyState from "#/components/ui/UiEmptyState";
import UiText from "#/components/ui/UiText";
import Donate from "#/components/views/Donate";
import { globalStyles } from "#/constants/GlobalStyles";
import { iconSizes } from "#/constants/IconSizes";
import { spacing } from "#/constants/Spacing";
import { useCorporateColor } from "#/hooks/useAppColorScheme";

interface EmptyComponentProperties {
  text: string;
  icon: React.ReactElement<{ color?: string }>;
  onPress?: () => void;
  children?: ReactNode;
  /** Optional, development-only QA hooks for the message region; unset in production. */
  messageTestID?: string;
  messageAccessibilityLabel?: string;
  onMessageLayout?: (event: LayoutChangeEvent) => void;
}

const EmptyComponent = ({
  text,
  icon,
  onPress,
  children,
  messageTestID,
  messageAccessibilityLabel,
  onMessageLayout,
}: EmptyComponentProperties) => {
  const corporate = useCorporateColor();

  return (
    <>
      <View
        style={{ marginVertical: spacing.huge }}
        testID={messageTestID}
        accessibilityLabel={messageAccessibilityLabel}
        onLayout={onMessageLayout}
        collapsable={messageTestID ? false : undefined}
      >
        <UiEmptyState icon={icon} onPress={onPress}>
          {text}
        </UiEmptyState>
      </View>
      {children}
      <UiCard
        style={[
          globalStyles.centered,
          {
            marginBottom: spacing.huge,
            paddingHorizontal: spacing.xl,
            paddingVertical: spacing.huge,
            gap: spacing.xl,
            overflow: "hidden",
          },
        ]}
      >
        <HeartIcon color={corporate} size={iconSizes.xl} />
        <UiText size="lg">
          Unterstütze uns im unermüdlichen Kampf gegen Fake News und verzerrte
          Narrative
        </UiText>
        <Donate paypalAlways={true} />
      </UiCard>
    </>
  );
};

export default EmptyComponent;
