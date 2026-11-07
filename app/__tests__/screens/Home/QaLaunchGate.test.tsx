import { act, render, waitFor } from "@testing-library/react-native";
import { useEffect } from "react";
import { Text } from "react-native";

import QaLaunchGate from "#/screens/Home/fixtures/QaLaunchGate";
import { initializeQaScenario, type QaSelection } from "#/screens/Home/fixtures/qaScenario";

jest.mock("#/screens/Home/fixtures/qaScenario", () => ({ initializeQaScenario: jest.fn() }));

test("feed effects cannot run before selection; identity is separate from readiness", async () => {
  let deliver!: (selection: QaSelection) => void;
  jest.mocked(initializeQaScenario).mockReturnValue(new Promise((resolve) => { deliver = resolve; }));
  const request = jest.fn();
  const Feed = () => {
    useEffect(() => { request(); }, []);
    return <Text testID="feed">feed</Text>;
  };
  const screen = await render(<QaLaunchGate><Feed /></QaLaunchGate>);
  expect(request).not.toHaveBeenCalled();
  expect(screen.queryByTestId("feed")).toBeNull();
  await act(async () => { deliver({ status: "active", id: "long_headline", source: "launch" }); });
  await waitFor(() => expect(request).toHaveBeenCalledTimes(1));
  expect(screen.getByLabelText("qa-scenario:long_headline")).toBeTruthy();
  expect(screen.queryByTestId("qa-article-card-ready")).toBeNull();
});

test.each(["invalid", "unsupported"] as const)("%s never mounts feed", async (status) => {
  jest.mocked(initializeQaScenario).mockResolvedValue({ status, id: "empty_feed", source: "launch" });
  const screen = await render(<QaLaunchGate><Text testID="feed">feed</Text></QaLaunchGate>);
  await waitFor(() => expect(screen.getByTestId(`qa-scenario-${status}`)).toBeTruthy());
  expect(screen.queryByTestId("feed")).toBeNull();
  expect(screen.queryByLabelText("qa-scenario:long_headline")).toBeNull();
});

test("normal launch has no QA identity", async () => {
  jest.mocked(initializeQaScenario).mockResolvedValue({ status: "normal", source: "none" });
  const screen = await render(<QaLaunchGate><Text testID="feed">normal app</Text></QaLaunchGate>);
  await waitFor(() => expect(screen.getByTestId("feed")).toBeTruthy());
  expect(screen.queryByLabelText("qa-scenario:long_headline")).toBeNull();
});
