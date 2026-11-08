from unittest.mock import Mock

import pytest

from visualqa.components.breaking_banner import BreakingBanner


@pytest.mark.unit
def test_banner_capture_rejects_clipped_title():
    banner = Mock(rect={"x": 10, "y": 20, "width": 100, "height": 60})
    title = Mock(rect={"x": 15, "y": 25, "width": 110, "height": 30})
    driver = Mock()
    driver.get_window_size.return_value = {"width": 300, "height": 500}
    driver.find_element.side_effect = [banner, title]
    with pytest.raises(AssertionError, match="does not contain"):
        BreakingBanner(driver).capture_screenshot()
