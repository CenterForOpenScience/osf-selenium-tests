import pytest
import settings

#TODO: Is there a better place to put these?
core_functionality = pytest.mark.core_functionality
dont_run_on_prod = pytest.mark.skipif(settings.PRODUCTION, reason='Test should not run on production')
