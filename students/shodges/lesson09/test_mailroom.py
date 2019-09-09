#!/usr/bin/env python3

import pytest
from donor_models import *

def test_donor_structure():
    honest_abe = Donor('Abraham Lincoln', 87.00, 18.65)
    teddy = Donor('Theodore Roosevelt')

    assert honest_abe.count == 2
    assert honest_abe.donations == 105.65

    assert teddy.count == 0
    assert teddy.donations == 0

    with pytest.raises(AttributeError):
        teddy.count = 1

    with pytest.raises(AttributeError):
        teddy.donations = 1000000.00


def test_process_donation():
    honest_abe = Donor('Abraham Lincoln')

    assert honest_abe.count == 0
    assert honest_abe.donations == 0.0

    honest_abe.process(307.65)

    assert honest_abe.count == 1
    assert honest_abe.donations == 307.65


def test_donor_collection():
    """
    Test DonorCollection class and persistence (since it's using shelve as a db)
    """
    simplecharity = DonorCollection('unit_tests')

    # Since this DB will persist, we want to start with a blank slate, but the del_donor
    # method will raise a KeyError if we try to delete a donor that doesn't exist.  That's
    # ok -- we'll just pass through it.
    try:
        simplecharity.del_donor('Test McTesterson')
    except KeyError:
        pass

    # Validate that the donor doesn't exist
    with pytest.raises(KeyError):
        simplecharity.donor('Test McTesterson')

    # Validate that we can add the donor
    assert simplecharity.add_donor('Test McTesterson') is True

    # Validate that we can process a donation and that its values will persist a DB close/
    # reopen
    assert simplecharity.donor('Test McTesterson').process(101.01) is True
    assert simplecharity.donor('Test McTesterson').count == 1
    assert simplecharity.donor('Test McTesterson').donations == 101.01

    # Close the DB and verify that it truly is closed
    simplecharity.db_close()
    with pytest.raises(ValueError):
        simplecharity.donor('Test McTesterson').count

    simplecharity = DonorCollection('unit_tests')
    assert simplecharity.donor('Test McTesterson').count == 1
    assert simplecharity.donor('Test McTesterson').donations == 101.01