import type { FeedFetcherProperties } from "#/screens/Home/components/Feed";
import { WordPressFetcher } from "#/screens/Home/fetchers/WordPressFetcher";
import { QA_ARTICLE_SLUG } from "./qaScenario";
import type { LoadArticlePostProperties, Post } from "#/types";

/** Synthetic content, not an actual publication or real WordPress response. */
const qaArticle: LoadArticlePostProperties = {
  _links: {}, // No WordPress featured-media network request
  id: 910001,
  slug: QA_ARTICLE_SLUG,
  date: "2026-10-12T09:00:00",
  date_gmt: "2026-10-12T09:00:00",
  link: "https://example.org/qa-long-headline/",
  title: {
    rendered:
      "QA-FIXTUR: Ein absichtlich sehr langer Nachrichtenartikel-Titel prüft den Zeilenumbruch auf kleinen Smartphone-Bildschirmen",
  },
  description: "",
  yoast_head_json: {
    description:
      "Synthetische Testdaten für einen stabilen visuellen Vergleich – keine echten Nachrichten.",
  },
  categories: [],
  authors: [{ display_name: "QA Redaktion", slug: "qa-redaktion" }],
  reading_time: 4,
};

/** Uses the production WordPress mapping and real ArticlePost component. */
export const qaFeedFetcher = async ({
  page = 1,
}: FeedFetcherProperties = {}): Promise<Post<unknown>[]> => {
  if (page !== 1) return [];
  const post = WordPressFetcher.mapArticleToPost(qaArticle, 0);
  // Engagement/share widgets make unrelated network calls in this app.
  // The test scenario focuses on the article card itself, not engagement.
  post.shareable = undefined;
  post.contentFavIdentifier = undefined;
  post.contentType = undefined;
  return [post];
};
