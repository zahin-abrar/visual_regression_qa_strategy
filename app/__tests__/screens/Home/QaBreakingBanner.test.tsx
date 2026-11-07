import { fireEvent, render } from "@testing-library/react-native";

import QaBreakingBanner from "#/screens/Home/fixtures/QaBreakingBanner";
import { qaBreakingNews } from "#/screens/Home/fixtures/qaBreakingNews";

jest.mock("#/screens/Home/fixtures/qaScenario", () => ({
  qaFixtureEnabled: true,
  qaActiveScenario: "breaking_news",
}));

test("readiness requires positive banner AND headline layouts", async () => {
  const screen = await render(<QaBreakingBanner />);
  expect(screen.getByText("EILMELDUNG")).toBeTruthy();
  expect(screen.getByText(qaBreakingNews.title)).toBeTruthy();
  expect(screen.queryByTestId("qa-breaking-banner-ready")).toBeNull();
  await fireEvent(screen.getByTestId("qa-breaking-banner"), "layout", { nativeEvent: { layout: { width: 390, height: 180 } } });
  expect(screen.queryByTestId("qa-breaking-banner-ready")).toBeNull();
  await fireEvent(screen.getByTestId("qa-breaking-banner-title"), "layout", { nativeEvent: { layout: { width: 340, height: 100 } } });
  expect(screen.getByTestId("qa-breaking-banner-ready")).toBeTruthy();
});

test("other-scenario launches do not render banner", async () => {
  const mutable = jest.requireMock("#/screens/Home/fixtures/qaScenario") as { qaActiveScenario: string };
  mutable.qaActiveScenario = "long_headline";
  try {
    const screen = await render(<QaBreakingBanner />);
    expect(screen.queryByText("EILMELDUNG")).toBeNull();
  } finally {
    mutable.qaActiveScenario = "breaking_news";
  }
});

test("disabled fixture mode does not render banner", async () => {
  const mutable = jest.requireMock("#/screens/Home/fixtures/qaScenario") as { qaFixtureEnabled: boolean };
  mutable.qaFixtureEnabled = false;
  try {
    const screen = await render(<QaBreakingBanner />);
    expect(screen.queryByText("EILMELDUNG")).toBeNull();
  } finally {
    mutable.qaFixtureEnabled = true;
  }
});

test("release gate hides banner even with mocked active QA state", async () => {
  const development = __DEV__;
  (globalThis as unknown as { __DEV__: boolean }).__DEV__ = false;
  try {
    const screen = await render(<QaBreakingBanner />);
    expect(screen.queryByText("EILMELDUNG")).toBeNull();
  } finally {
    (globalThis as unknown as { __DEV__: boolean }).__DEV__ = development;
  }
});
