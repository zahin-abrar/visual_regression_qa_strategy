/** EXEC-031: real Feed + EmptyComponent readiness for the empty_feed scenario. */
import { act, fireEvent, render, screen } from "@testing-library/react-native";
import React from "react";

import Feed from "#/screens/Home/components/Feed";
import { qaFeedFetcher } from "#/screens/Home/fixtures/qaFeed";
import type { Post } from "#/types";

const mockQa: { enabled: boolean; scenario: string | undefined } = {
  enabled: true,
  scenario: "empty_feed",
};
jest.mock("#/screens/Home/fixtures/qaScenario", () => {
  const actual = jest.requireActual("#/screens/Home/fixtures/qaScenario");
  // Live getters (like ES module bindings); defined explicitly so they are not
  // evaluated eagerly by object-spread transpilation.
  const mocked = { ...actual };
  Object.defineProperty(mocked, "qaFixtureEnabled", { get: () => mockQa.enabled });
  Object.defineProperty(mocked, "qaActiveScenario", { get: () => mockQa.scenario });
  return mocked;
});
jest.mock("expo-router", () => ({
  __esModule: true,
  useRouter: () => ({ push: jest.fn() }),
  useScrollToTop: () => {},
}));
jest.mock("#/components/Icons", () => ({
  HeartIcon: () => null,
  SearchIcon: () => null,
  SettingsIcon: () => null,
  WorldIcon: () => null,
}));
jest.mock("#/components/ui/UiSpinner", () => {
  const { Text } = require("react-native");
  return () => <Text testID="feed-spinner">Lade Feed...</Text>;
});
jest.mock("#/components/views/Donate", () => () => null);
jest.mock("#/components/posts/GenericPost", () => {
  const { View } = require("react-native");
  return () => <View testID="post-item" />;
});
jest.mock("#/screens/Home/fixtures/QaBreakingBanner", () => {
  const { View } = require("react-native");
  return () => <View testID="qa-breaking-banner" />;
});
jest.mock("#/hooks/useAppColorScheme", () => ({
  useAppColorScheme: () => "light",
  useCorporateColor: () => "#000",
}));

// RNTL 14 fireEvent is async and already wrapped in act.
const layout = async (testID: string) =>
  fireEvent(screen.getByTestId(testID), "layout", {
    nativeEvent: { layout: { x: 0, y: 0, width: 300, height: 120 } },
  });

const MESSAGE = /Keine Ergebnisse\. Versuche es später erneut/;

describe("Feed empty_feed readiness", () => {
  beforeEach(() => {
    mockQa.enabled = true;
    mockQa.scenario = "empty_feed";
  });

  test("successful zero-item fetch renders the real empty state, then becomes ready after layout", async () => {
    await render(<Feed fetchers={[{ fetcher: qaFeedFetcher }]} />);
    expect(await screen.findByText(MESSAGE)).toBeTruthy();
    expect(screen.queryByTestId("feed-spinner")).toBeNull();
    expect(screen.queryByTestId("qa-empty-feed-ready")).toBeNull();
    await layout("qa-empty-feed");
    const ready = screen.getByTestId("qa-empty-feed-ready");
    expect(ready.props.accessibilityLabel).toBe("qa-theme:light");
    expect(screen.queryByTestId("post-item")).toBeNull();
    expect(screen.queryByTestId("qa-breaking-banner")).toBeNull();
    expect(screen.queryByTestId("feed-spinner")).toBeNull();
  });

  test("a failed fetch shows the same empty UI but never the successful-empty marker", async () => {
    const error = jest.spyOn(console, "error").mockImplementation(() => {});
    // Leave a stale success behind first; Feed must clear it per request.
    await qaFeedFetcher({ page: 1 });
    const failing = jest.fn(async (): Promise<Post<unknown>[]> => {
      throw new Error("HTTP 503");
    });
    await render(<Feed fetchers={[{ fetcher: failing }]} />);
    expect(await screen.findByText(MESSAGE)).toBeTruthy();
    await layout("qa-empty-feed");
    expect(screen.queryByTestId("qa-empty-feed-ready")).toBeNull();
    expect(screen.getByTestId("qa-empty-feed")).toBeTruthy();
    expect(failing).toHaveBeenCalled();
    error.mockRestore();
  });

  test("loading state exposes neither the empty state nor readiness", async () => {
    let resolve!: (posts: Post<unknown>[]) => void;
    const pending = () => new Promise<Post<unknown>[]>((r) => (resolve = r));
    await render(<Feed fetchers={[{ fetcher: pending }]} />);
    expect(screen.getByTestId("feed-spinner")).toBeTruthy();
    expect(screen.queryByTestId("qa-empty-feed")).toBeNull();
    expect(screen.queryByTestId("qa-empty-feed-ready")).toBeNull();
    await act(async () => resolve([]));
  });

  test.each([
    ["production (fixtures disabled)", false, undefined],
    ["another QA scenario", true, "long_headline"],
  ])("%s keeps the empty state free of QA markers", async (_name, enabled, scenario) => {
    mockQa.enabled = enabled;
    mockQa.scenario = scenario;
    await render(<Feed fetchers={[{ fetcher: async () => [] }]} />);
    expect(await screen.findByText(MESSAGE)).toBeTruthy();
    expect(screen.queryByTestId("qa-empty-feed")).toBeNull();
    expect(screen.queryByTestId("qa-empty-feed-ready")).toBeNull();
  });

  test("release builds expose no QA empty-feed markers", async () => {
    const globals = globalThis as unknown as { __DEV__: boolean };
    const previous = globals.__DEV__;
    globals.__DEV__ = false;
    try {
      await render(<Feed fetchers={[{ fetcher: qaFeedFetcher }]} />);
      expect(await screen.findByText(MESSAGE)).toBeTruthy();
      expect(screen.queryByTestId("qa-empty-feed")).toBeNull();
      expect(screen.queryByTestId("qa-empty-feed-ready")).toBeNull();
    } finally {
      globals.__DEV__ = previous;
    }
  });
});
