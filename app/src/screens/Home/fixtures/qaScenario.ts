/** Development-only launch selection. No event listener or persisted selection. */
export const QA_ARTICLE_SLUG = "qa-long-headline";
/** Synthetic article whose featured media is intentionally absent (not a broken URL). */
export const QA_NO_IMAGE_SLUG = "qa-no-image";

export const qaScenarios = Object.freeze({
  long_headline: { captureSupported: true },
  breaking_news: { captureSupported: true },
  dark_article: { captureSupported: true },
  no_image: { captureSupported: true },
  empty_feed: { captureSupported: true },
});
export type QaScenarioId = keyof typeof qaScenarios;
export type QaSelection = Readonly<{
  status: "normal" | "active" | "unsupported" | "invalid";
  id?: string;
  source: "disabled" | "launch" | "environment" | "none";
}>;

/** Explicit URL selection wins, including `none`; malformed QA input fails closed. */
export function resolveQaSelection(
  development: boolean,
  initialUrl: string | null,
  environmentScenario?: string,
): QaSelection {
  if (!development) return Object.freeze({ status: "normal", source: "disabled" });
  let id = environmentScenario || undefined;
  let source: QaSelection["source"] = id ? "environment" : "none";
  if (initialUrl) {
    try {
      const url = new URL(initialUrl);
      const selections = url.searchParams.getAll("qa_scenario");
      if (selections.length) {
        source = "launch";
        if (selections.length !== 1 || !selections[0]) {
          return Object.freeze({ status: "invalid", source });
        }
        id = selections[0];
      }
    } catch {
      return Object.freeze({ status: "invalid", source: "launch" });
    }
  }
  if (!id || id === "none") return Object.freeze({ status: "normal", source });
  if (!Object.prototype.hasOwnProperty.call(qaScenarios, id)) {
    return Object.freeze({ status: "invalid", id, source });
  }
  return Object.freeze({
    status: qaScenarios[id as QaScenarioId].captureSupported ? "active" : "unsupported",
    id,
    source,
  });
}

// ES module live binding: updated once, before the application subtree mounts.
export let qaFixtureEnabled = false;
export let qaActiveScenario: QaScenarioId | undefined;
/** Read-only override; resolved before providers mount, never saved to settings. */
export function getQaThemeOverride(): "light" | "dark" | undefined {
  if (!__DEV__ || !qaFixtureEnabled || !qaActiveScenario) return undefined;
  return qaActiveScenario === "dark_article" ? "dark" : "light";
}
/**
 * Explicit QA media contract for synthetic articles. `undefined` means the
 * article is not a QA fixture and keeps normal production rendering.
 */
export type QaArticleMedia = "bundled-cover" | "none";
export function getQaArticleMedia(slug: string): QaArticleMedia | undefined {
  if (!__DEV__ || !qaFixtureEnabled) return undefined;
  if (slug === QA_ARTICLE_SLUG) return "bundled-cover";
  if (slug === QA_NO_IMAGE_SLUG && qaActiveScenario === "no_image") return "none";
  return undefined;
}
let initialization: Promise<QaSelection> | undefined;

/** Log-safe launch URL: scheme, host and path plus only the qa_scenario values (no other query data). */
export function describeQaLaunchUrl(url: string | null): string {
  if (!url) return "<none>";
  try {
    const parsed = new URL(url);
    const selections = parsed.searchParams.getAll("qa_scenario");
    return `${parsed.protocol}//${parsed.host}${parsed.pathname} qa_scenario=${JSON.stringify(selections)}`;
  } catch {
    return "<unparseable>";
  }
}

export function initializeQaScenario(getInitialUrl: () => Promise<string | null>) {
  if (!initialization) {
    initialization = (__DEV__ ? getInitialUrl() : Promise.resolve(null))
      .then((url) => {
        const selection = resolveQaSelection(__DEV__, url, process.env.EXPO_PUBLIC_QA_SCENARIO);
        // Development-only diagnostic (initialization never runs this path in release builds).
        console.info(
          `[qa-scenario] initial URL ${describeQaLaunchUrl(url)} -> status=${selection.status} ` +
            `id=${selection.id ?? "-"} source=${selection.source}`,
        );
        return selection;
      })
      .catch((): QaSelection => Object.freeze({ status: "invalid", source: "launch" }))
      .then((selection) => {
        qaFixtureEnabled = selection.status === "active";
        qaActiveScenario = qaFixtureEnabled ? selection.id as QaScenarioId : undefined;
        return selection;
      });
  }
  return initialization;
}
