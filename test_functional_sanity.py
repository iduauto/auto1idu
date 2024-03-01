import  pytest

import setup
from functional_sanity import FunctionalSanity

driver = setup.get_driver()
functional_sanity = FunctionalSanity(driver)

def test_functional_sanity_06():
    assert functional_sanity.functional_sanity_06()

def test_functional_sanity_11():
    assert functional_sanity.functional_sanity_11()

def test_functional_sanity_12():
    assert functional_sanity.functional_sanity_12()

def test_functional_sanity_14():
    assert functional_sanity.functional_sanity_14()

def test_functional_sanity_28():
    assert functional_sanity.functional_sanity_28()

def test_functional_sanity_29():
    assert functional_sanity.functional_sanity_29()

def test_functional_sanity_31():
    assert functional_sanity.functional_sanity_31()

def test_functional_sanity_32():
    assert functional_sanity.functional_sanity_32()

def test_functional_sanity_33():
    assert functional_sanity.functional_sanity_33()

def test_functional_sanity_34():
    assert functional_sanity.functional_sanity_34()

def test_functional_sanity_35():
    assert functional_sanity.functional_sanity_35()

def test_functional_sanity_37():
    assert functional_sanity.functional_sanity_37()

def test_functional_sanity_38():
    assert functional_sanity.functional_sanity_38()

def test_functional_sanity_39():
    assert functional_sanity.functional_sanity_39()

def test_functional_sanity_41():
    assert functional_sanity.functional_sanity_41()

def test_functional_sanity_43():
    assert functional_sanity.functional_sanity_43()

def test_functional_sanity_47():
    assert functional_sanity.functional_sanity_47()

def test_functional_sanity_49():
    assert functional_sanity.functional_sanity_49()

def test_functional_sanity_50():
    assert functional_sanity.functional_sanity_50()

def test_functional_sanity_57():
    assert functional_sanity.functional_sanity_57()

def test_functional_sanity_58():
    assert functional_sanity.functional_sanity_58()