/** EXEC-029: explicit no_image fixture and QA media contract. */
type ScenarioModule = typeof import("#/screens/Home/fixtures/qaScenario");
type FeedModule = typeof import("#/screens/Home/fixtures/qaFeed");

const load = async (id: string | null) => {
  jest.resetModules();
  const scenario = require("#/screens/Home/fixtures/qaScenario") as ScenarioModule;
  const feed = require("#/screens/Home/fixtures/qaFeed") as FeedModule;
  await scenario.initializeQaScenario(async () => (id ? `vvpapp:///home?qa_scenario=${id}` : null));
  return { scenario, feed };
};

describe("no_image fixture contract", () => {
  test("no_image feed supplies one article with genuinely absent featured media", async () => {
    const { scenario, feed } = await load("no_image");
    const posts = await feed.qaFeedFetcher({ page: 1 });
    expect(posts).toHaveLength(1);
    const { article } = posts[0].data as { article: import("#/types").ArticleProperties };
    expect(article.slug).toBe(scenario.QA_NO_IMAGE_SLUG);
    expect(article._links["wp:featuredmedia"]).toBeUndefined();
    expect(article.imageUrl).toBeUndefined();
    // Text content reused from the approved long_headline fixture.
    expect(article.title).toMatch(/^QA-FIXTUR: Ein absichtlich sehr langer/);
    expect(scenario.getQaArticleMedia(article.slug)).toBe("none");
    expect(await feed.qaFeedFetcher({ page: 2 })).toEqual([]);
  });

  test.each(["long_headline", "dark_article", "breaking_news"])(
    "%s keeps the image-bearing fixture and bundled cover", async (id) => {
      const { scenario, feed } = await load(id);
      const posts = await feed.qaFeedFetcher({ page: 1 });
      const { article } = posts[0].data as { article: import("#/types").ArticleProperties };
      expect(article.slug).toBe(scenario.QA_ARTICLE_SLUG);
      expect(scenario.getQaArticleMedia(scenario.QA_ARTICLE_SLUG)).toBe("bundled-cover");
      // The no-image slug is not a QA article outside its own scenario.
      expect(scenario.getQaArticleMedia(scenario.QA_NO_IMAGE_SLUG)).toBeUndefined();
    },
  );

  test.each([null, "none", "empty_feed"])("non-active launch %s yields no QA media contract", async (id) => {
    const { scenario } = await load(id);
    expect(scenario.getQaArticleMedia(scenario.QA_NO_IMAGE_SLUG)).toBeUndefined();
    expect(scenario.getQaArticleMedia(scenario.QA_ARTICLE_SLUG)).toBeUndefined();
    expect(scenario.getQaArticleMedia("some-production-article")).toBeUndefined();
  });

  test("release builds never apply the QA media contract", async () => {
    const { scenario } = await load("no_image");
    const globals = globalThis as unknown as { __DEV__: boolean };
    const previous = globals.__DEV__;
    try {
      globals.__DEV__ = false;
      expect(scenario.getQaArticleMedia(scenario.QA_NO_IMAGE_SLUG)).toBeUndefined();
    } finally {
      globals.__DEV__ = previous;
    }
  });
});
