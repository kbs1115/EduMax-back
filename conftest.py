import pytest

"""
fixture module을 pytest_plugins에 추가하면 fixture로 등록된다.
"""

pytest_plugins = [
    "community.tests.fixtures.api_fixtures",
    "community.tests.fixtures.instance_fixtures",
    "community.tests.fixtures.mock_fixtures",
    "community.tests.fixtures.data_fixtures",
]
