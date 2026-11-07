import { resolveQaSelection } from "#/screens/Home/fixtures/qaScenario";

describe("QA cold-launch selection", () => {
  test("release ignores URL and environment controls", () => {
    expect(resolveQaSelection(false, "vvpapp:///home?qa_scenario=long_headline", "long_headline"))
      .toEqual({ status: "normal", source: "disabled" });
  });
  test("legacy environment remains supported", () => {
    expect(resolveQaSelection(true, null, "long_headline"))
      .toEqual({ status: "active", id: "long_headline", source: "environment" });
  });
  test("no authorized input is normal", () => {
    expect(resolveQaSelection(true, null)).toEqual({ status: "normal", source: "none" });
  });
  test.each(["empty_feed"])(
    "%s is an explicit active selection that cannot fall back to long_headline", (id) => {
      expect(resolveQaSelection(true, `vvpapp:///home?qa_scenario=${id}`, "long_headline"))
        .toEqual({ status: "active", id, source: "launch" });
      expect(resolveQaSelection(false, `vvpapp:///home?qa_scenario=${id}`, id))
        .toEqual({ status: "normal", source: "disabled" });
    },
  );
  test.each(["unknown", "toString", "", "long_headline&qa_scenario=empty_feed"])(
    "invalid selection %s fails closed", (id) => {
      expect(resolveQaSelection(true, `vvpapp:///home?qa_scenario=${id}`, "long_headline").status)
        .toBe("invalid");
    },
  );
  test("explicit none suppresses the compatibility fallback", () => {
    expect(resolveQaSelection(true, "vvpapp:///home?qa_scenario=none", "long_headline"))
      .toEqual({ status: "normal", source: "launch" });
  });
  test("explicit supported selection overrides invalid environment", () => {
    expect(resolveQaSelection(true, "vvpapp:///home?qa_scenario=long_headline", "bad").status)
      .toBe("active");
  });
  test("dev-client outer selection wins without treating the Metro URL as a scenario", () => {
    expect(resolveQaSelection(true,
      "exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=long_headline",
      "bad")).toEqual({ status: "active", id: "long_headline", source: "launch" });
  });
  test("unknown environment does not enable a fixture", () => {
    expect(resolveQaSelection(true, null, "bad").status).toBe("invalid");
  });
  test("result is immutable", () => {
    expect(Object.isFrozen(resolveQaSelection(true, null, "long_headline"))).toBe(true);
  });
  test("initialization waits for URL and ignores later selections within this JS launch", async () => {
    jest.resetModules();
    const scenario = require("#/screens/Home/fixtures/qaScenario") as typeof import("#/screens/Home/fixtures/qaScenario");
    let deliver!: (url: string) => void;
    const first = scenario.initializeQaScenario(() => new Promise((resolve) => { deliver = resolve; }));
    expect(scenario.qaFixtureEnabled).toBe(false);
    deliver("vvpapp:///home?qa_scenario=long_headline");
    expect((await first).id).toBe("long_headline");
    expect(scenario.qaFixtureEnabled).toBe(true);
    const next = jest.fn(async () => "vvpapp:///home?qa_scenario=empty_feed");
    expect(scenario.initializeQaScenario(next)).toBe(first);
    expect(next).not.toHaveBeenCalled();
  });
  test("initial URL failure blocks initialization", async () => {
    jest.resetModules();
    const scenario = require("#/screens/Home/fixtures/qaScenario") as typeof import("#/screens/Home/fixtures/qaScenario");
    expect((await scenario.initializeQaScenario(async () => { throw new Error("URL unavailable"); })).status)
      .toBe("invalid");
    expect(scenario.qaFixtureEnabled).toBe(false);
  });
  test("fresh JS initialization does not inherit the previous supported selection", async () => {
    for (const [id, status] of [["long_headline", "active"], ["empty_feed", "active"], ["bad", "invalid"], ["none", "normal"]]) {
      jest.resetModules();
      const scenario = require("#/screens/Home/fixtures/qaScenario") as typeof import("#/screens/Home/fixtures/qaScenario");
      expect((await scenario.initializeQaScenario(async () => `vvpapp:///home?qa_scenario=${id}`)).status)
        .toBe(status);
      expect(scenario.qaFixtureEnabled).toBe(status === "active");
    }
  });
});

test("breaking selection wins over legacy headline fixture", () => {
  expect(resolveQaSelection(true, "vvpapp:///home?qa_scenario=breaking_news", "long_headline"))
    .toEqual({ status: "active", id: "breaking_news", source: "launch" });
  expect(resolveQaSelection(false, "vvpapp:///home?qa_scenario=breaking_news", "breaking_news"))
    .toEqual({ status: "normal", source: "disabled" });
});

test("no_image is an explicit capture-supported launch selection and stays release-disabled", () => {
  expect(resolveQaSelection(true, "vvpapp:///home?qa_scenario=no_image", "long_headline"))
    .toEqual({ status: "active", id: "no_image", source: "launch" });
  expect(resolveQaSelection(false, "vvpapp:///home?qa_scenario=no_image", "no_image"))
    .toEqual({ status: "normal", source: "disabled" });
});

test("theme overrides are immutable-launch, development-only and absent for normal launches", async () => {
  for (const [id, theme] of [["dark_article", "dark"], ["long_headline", "light"], ["breaking_news", "light"], ["none", undefined], ["no_image", "light"], ["empty_feed", "light"]]) {
    jest.resetModules();
    const scenario = require("#/screens/Home/fixtures/qaScenario") as typeof import("#/screens/Home/fixtures/qaScenario");
    expect(scenario.getQaThemeOverride()).toBeUndefined();
    await scenario.initializeQaScenario(async () => `vvpapp:///home?qa_scenario=${id}`);
    expect(scenario.getQaThemeOverride()).toBe(theme);
    const globals = globalThis as unknown as { __DEV__: boolean };
    const previous = globals.__DEV__;
    try {
      globals.__DEV__ = false;
      expect(scenario.getQaThemeOverride()).toBeUndefined();
    } finally { globals.__DEV__ = previous; }
  }
});
