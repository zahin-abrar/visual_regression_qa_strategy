/** EXEC-029: QA-only no-image rendering inside the real ArticlePost. */
import { act, render } from "@testing-library/react-native";
import { Image } from "expo-image";
import React from "react";

import ArticlePost from "#/components/posts/ArticlePost";
import {
  QA_ARTICLE_SLUG,
  QA_NO_IMAGE_SLUG,
  initializeQaScenario,
} from "#/screens/Home/fixtures/qaScenario";
import type { ArticleProperties, HttpsUrl } from "#/types";

jest.mock("expo-image", () => ({ Image: jest.fn(() => null) }));
jest.mock("expo-router", () => ({
  useRouter: jest.fn(() => ({ push: jest.fn(), back: jest.fn() })),
  useFocusEffect: jest.fn(),
}));
jest.mock("#/components/counter/ViewCounter", () => ({ __esModule: true, default: () => null }));
jest.mock("#/components/ui/UiSpinner", () => ({ __esModule: true, default: () => null }));
jest.mock("#/components/ui/UiBadge", () => ({ __esModule: true, default: () => null }));
jest.mock("#/constants/Config", () => ({ __esModule: true, default: { importantCats: {} } }));
jest.mock("#/helpers/AppImages", () => ({ AppImages: { loadingAnimation: null } }));
jest.mock("#/helpers/Linking", () => ({ onLinkPress: jest.fn() }));
jest.mock("#/helpers/Sharing", () => ({ onShare: jest.fn() }));
jest.mock("#/helpers/Stores/ContentStore", () => ({
  __esModule: true, default: { setStoredArticle: jest.fn() },
}));
jest.mock("#/helpers/Stores/PersonalStore", () => ({
  __esModule: true, default: { getScrollPosition: jest.fn().mockResolvedValue(null) },
}));
jest.mock("#/helpers/network/WordPressAPI", () => ({
  __esModule: true, default: { getFeatureImage: jest.fn().mockResolvedValue({ image: "" }) },
}));
jest.mock("#/hooks/useFeedDimensions", () => ({ useFeedDimensions: () => ({ width: 400 }) }));

const article = (slug: string, withMediaLink = false): ArticleProperties => ({
  _links: withMediaLink ? { "wp:featuredmedia": [{ href: "https://example.com/m" }] } : {},
  date: "2026-10-12T09:00:00",
  date_gmt: "2026-10-12T09:00:00",
  link: `https://example.org/${slug}/` as HttpsUrl,
  description: "Synthetische Testdaten",
  categories: [],
  id: 1,
  slug,
  title: "QA-FIXTUR: Titel",
  authors: [{ display_name: "QA Redaktion", slug: "qa" }],
});

type Node = { type: unknown; props: Record<string, unknown>; children: (Node | string)[] };
/** Host elements carrying an onLayout handler (RNTL 14 has no UNSAFE_root). */
const layoutHosts = (root: unknown): Node[] => {
  const found: Node[] = [];
  const walk = (node: Node | string) => {
    if (typeof node === "string") return;
    if (typeof node.type === "string" && typeof node.props.onLayout === "function") found.push(node);
    node.children.forEach(walk);
  };
  walk(root as Node);
  return found;
};

const layoutTextBlock = async (screen: { container: unknown }) => {
  const hosts = layoutHosts(screen.container);
  expect(hosts).toHaveLength(1);
  await act(async () => {
    (hosts[0].props.onLayout as (event: unknown) => void)({
      nativeEvent: { layout: { x: 0, y: 0, width: 400, height: 120 } },
    });
  });
};

const imageMock = Image as unknown as jest.Mock;

describe("fixtures disabled (normal launch)", () => {
  beforeEach(() => imageMock.mockClear());

  test("an article using the no-image slug keeps production image rendering", async () => {
    const screen = await render(<ArticlePost article={article(QA_NO_IMAGE_SLUG)} inView={false} />);
    expect(imageMock).toHaveBeenCalled();
    expect(screen.queryByTestId("qa-article-no-image-ready")).toBeNull();
    expect(screen.queryByTestId("qa-article-title")).toBeNull();
    // Production cards get no QA onLayout hook.
    expect(layoutHosts(screen.container)).toHaveLength(0);
  });
});

describe("no_image scenario active", () => {
  beforeAll(async () => {
    await initializeQaScenario(async () => "vvpapp:///home?qa_scenario=no_image");
  });
  beforeEach(() => imageMock.mockClear());

  test("renders title/metadata/summary with no image panel, placeholder or remote fetch", async () => {
    const screen = await render(<ArticlePost article={article(QA_NO_IMAGE_SLUG)} inView />);
    expect(imageMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("qa-article-title")).toBeTruthy();
    expect(screen.getByText(/QA Redaktion/)).toBeTruthy();
    expect(screen.getByText("Synthetische Testdaten")).toBeTruthy();
    expect(screen.getByTestId("article-progress-bar")).toBeTruthy();
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    expect(require("#/helpers/network/WordPressAPI").default.getFeatureImage).not.toHaveBeenCalled();
  });

  test("readiness follows text layout, never image onLoad", async () => {
    const screen = await render(<ArticlePost article={article(QA_NO_IMAGE_SLUG)} inView={false} />);
    expect(screen.queryByTestId("qa-article-no-image-ready")).toBeNull();
    await layoutTextBlock(screen);
    const ready = screen.getByTestId("qa-article-no-image-ready");
    expect(ready.props.accessibilityLabel).toBe("qa-theme:light");
    expect(screen.queryByTestId("qa-article-card-ready")).toBeNull();
  });

  test("ordinary production articles still render their image path unchanged", async () => {
    const screen = await render(<ArticlePost article={article("prod-article", true)} inView={false} />);
    expect(imageMock).toHaveBeenCalled();
    expect(screen.queryByTestId("qa-article-no-image-ready")).toBeNull();
    expect(screen.queryByTestId("qa-article-title")).toBeNull();
  });

  test("the image-bearing QA slug keeps its bundled cover and onLoad readiness", async () => {
    const screen = await render(<ArticlePost article={article(QA_ARTICLE_SLUG)} inView={false} />);
    expect(imageMock).toHaveBeenCalled();
    expect(screen.queryByTestId("qa-article-card-ready")).toBeNull();
    const { onLoad } = imageMock.mock.calls.at(-1)[0];
    await act(async () => onLoad());
    expect(screen.getByTestId("qa-article-card-ready")).toBeTruthy();
    expect(screen.queryByTestId("qa-article-no-image-ready")).toBeNull();
  });
});
