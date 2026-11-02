/**
 * Bounded screenshot-feasibility scenario; never activates in release builds.
 * Set EXPO_PUBLIC_QA_SCENARIO=long_headline before starting Metro.
 */
export const QA_ARTICLE_SLUG = "qa-long-headline";
export const qaFixtureEnabled =
  __DEV__ && process.env.EXPO_PUBLIC_QA_SCENARIO === "long_headline";
