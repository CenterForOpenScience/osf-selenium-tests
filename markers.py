import pytest

import settings


two_minute_drill = pytest.mark.two_minute_drill
smoke_test = pytest.mark.smoke_test
core_functionality = pytest.mark.core_functionality
dont_run_on_prod = pytest.mark.skipif(
    settings.PRODUCTION, reason='Test should not run on production'
)
dont_run_on_preferred_node = pytest.mark.skipif(
    bool(settings.PREFERRED_NODE),
    reason='Test makes breaking changes to preferred node',
)
