#!/usr/bin/env python

"""Tests for `photoz_utils`."""

import pytest


from datalabutils import photoz_utils


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_delz(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert photoz_utils.delz(1,2) == (1-2.0) / (1+2.0)
