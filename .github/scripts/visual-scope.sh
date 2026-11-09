#!/usr/bin/env bash
# Map the workflow's visual_scope input to a fixed pytest selection (explicit allowlist).
# Writes VISUAL_PYTEST_TARGET and EXPECTED_VISUAL to $GITHUB_ENV (or stdout when unset).
# The input is only compared, never interpolated into a command.
set -eu
scope=${1-}
case "$scope" in
  all)           target="";                                                                    expected=5 ;;
  breaking_news) target="tests/test_breaking_news.py::test_breaking_news_banner_matches_reviewed_golden"; expected=1 ;;
  *)
    echo "::error title=Invalid visual_scope::'$scope' is not one of: all, breaking_news"
    exit 1 ;;
esac
out=${GITHUB_ENV:-/dev/stdout}
{ echo "VISUAL_PYTEST_TARGET=$target"; echo "EXPECTED_VISUAL=$expected"; } >> "$out"
echo "visual scope: $scope -> ${target:-all tests marked visual} (expected $expected)"
