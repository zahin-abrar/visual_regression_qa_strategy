"""These tests verify only the comparator; NOT a mobile screenshot test."""

from PIL import Image
import pytest

from visualqa.image_diff import compare_png


@pytest.mark.unit
def test_identical_images_pass(tmp_path):
    baseline = tmp_path / "b.png"
    actual = tmp_path / "a.png"
    Image.new("RGB", (40, 40), (255, 255, 255)).save(baseline)
    Image.new("RGB", (40, 40), (255, 255, 255)).save(actual)
    result = compare_png(baseline, actual, tmp_path / "diff.png")
    assert result.passed and result.changed_pixels == 0


@pytest.mark.unit
def test_large_visible_difference_fails(tmp_path):
    baseline = tmp_path / "b.png"
    actual = tmp_path / "a.png"
    Image.new("RGB", (40, 40), (255, 255, 255)).save(baseline)
    Image.new("RGB", (40, 40), (0, 0, 0)).save(actual)
    result = compare_png(baseline, actual, tmp_path / "diff.png")
    assert not result.passed and result.changed_ratio == 1.0
    assert (tmp_path / "diff.png").is_file()


@pytest.mark.unit
def test_different_dimensions_fail(tmp_path):
    baseline = tmp_path / "b.png"
    actual = tmp_path / "a.png"
    Image.new("RGB", (40, 40)).save(baseline)
    Image.new("RGB", (40, 41)).save(actual)
    result = compare_png(baseline, actual, tmp_path / "diff.png")
    assert not result.passed and not result.size_match


@pytest.mark.unit
def test_subthreshold_rgb_noise_ignored(tmp_path):
    baseline = tmp_path / "b.png"
    actual = tmp_path / "a.png"
    Image.new("RGB", (40, 40), (100, 100, 100)).save(baseline)
    Image.new("RGB", (40, 40), (108, 100, 100)).save(actual)
    result = compare_png(baseline, actual, tmp_path / "diff.png")
    assert result.passed and result.changed_pixels == 0
