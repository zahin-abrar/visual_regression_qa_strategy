/** Synthetic sample-app extension, not an upstream VVP breaking-news feature. */
export type QaBreakingNews = Readonly<{ label: string; title: string }>;

export const qaBreakingNews: QaBreakingNews = Object.freeze({
  label: "EILMELDUNG",
  title: "QA-Test: Redaktion meldet wichtige Neuigkeiten zur synthetischen Testausgabe für alle Leserinnen und Leser",
});
