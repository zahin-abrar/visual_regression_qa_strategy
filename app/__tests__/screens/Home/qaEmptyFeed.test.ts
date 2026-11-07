/** EXEC-031: empty_feed is a successful zero-item response, not an error. */
type ScenarioModule = typeof import("#/screens/Home/fixtures/qaScenario");
type FeedModule = typeof import("#/screens/Home/fixtures/qaFeed");
type UtilitiesModule = typeof import("#/screens/Home/fetchers/FetcherUtilities");

const load = async (id: string | null) => {
  jest.resetModules();
  const scenario = require("#/screens/Home/fixtures/qaScenario") as ScenarioModule;
  const feed = require("#/screens/Home/fixtures/qaFeed") as FeedModule;
  const utilities = (require("#/screens/Home/fetchers/FetcherUtilities") as UtilitiesModule).default;
  await scenario.initializeQaScenario(async () => (id ? `vvpapp:///home?qa_scenario=${id}` : null));
  return { scenario, feed, utilities };
};

describe("empty_feed fixture contract", () => {
  test("one configured source resolves successfully with zero items", async () => {
    const { scenario, feed, utilities } = await load("empty_feed");
    expect(scenario.qaActiveScenario).toBe("empty_feed");
    expect(feed.getQaFeedOutcome()).toBeUndefined();
    expect(feed.isQaSuccessfulEmptyFeed()).toBe(false);
    const posts = await utilities.fetchAndProcessPosts([{ fetcher: feed.qaFeedFetcher }], { page: 1 });
    expect(posts).toEqual([]);
    expect(feed.getQaFeedOutcome()).toEqual({ scenario: "empty_feed", status: "success", count: 0 });
    expect(Object.isFrozen(feed.getQaFeedOutcome())).toBe(true);
    expect(feed.isQaSuccessfulEmptyFeed()).toBe(true);
  });

  test("a failed request also yields [] but never records a successful outcome", async () => {
    const { feed, utilities } = await load("empty_feed");
    const error = jest.spyOn(console, "error").mockImplementation(() => {});
    const failing = jest.fn(async () => {
      throw new Error("HTTP 503");
    });
    feed.resetQaFeedOutcome();
    const posts = await utilities.fetchAndProcessPosts([{ fetcher: failing }], { page: 1 });
    expect(posts).toEqual([]); // Indistinguishable by list content alone.
    expect(feed.getQaFeedOutcome()).toBeUndefined();
    expect(feed.isQaSuccessfulEmptyFeed()).toBe(false);
    error.mockRestore();
  });

  test("a later request clears an earlier success until it resolves", async () => {
    const { feed } = await load("empty_feed");
    await feed.qaFeedFetcher({ page: 1 });
    expect(feed.isQaSuccessfulEmptyFeed()).toBe(true);
    feed.resetQaFeedOutcome();
    expect(feed.isQaSuccessfulEmptyFeed()).toBe(false);
  });

  test.each(["long_headline", "breaking_news", "dark_article", "no_image"])(
    "%s still returns its populated fixture and never reports successful-empty", async (id) => {
      const { feed } = await load(id);
      const posts = await feed.qaFeedFetcher({ page: 1 });
      expect(posts).toHaveLength(1);
      expect(feed.isQaSuccessfulEmptyFeed()).toBe(false);
    },
  );

  test.each([null, "none"])("non-active launch %s never reports successful-empty", async (id) => {
    const { feed } = await load(id);
    expect(feed.isQaSuccessfulEmptyFeed()).toBe(false);
  });

  test("release builds never report successful-empty", async () => {
    const { feed } = await load("empty_feed");
    await feed.qaFeedFetcher({ page: 1 });
    const globals = globalThis as unknown as { __DEV__: boolean };
    const previous = globals.__DEV__;
    try {
      globals.__DEV__ = false;
      expect(feed.isQaSuccessfulEmptyFeed()).toBe(false);
    } finally {
      globals.__DEV__ = previous;
    }
  });
});
