"""Unit test file for nexthink_api."""
from pydantic import ValidationError
import pytest

from nexthink_api import NxtTokenRequest


class TestNxtTokenRequest():

    def testValidHeaderWIthModelDump(self) -> None:
        v1: NxtTokenRequest = NxtTokenRequest()
        d: dict = v1.get_request_header()
        assert d == {'grant_type': 'client_credentials'}

    def testModifyHeader(self) -> None:
        with pytest.raises(ValidationError):
            v1: NxtTokenRequest = NxtTokenRequest()
            v1.data = {'test': 'toto'}
