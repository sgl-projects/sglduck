"""Tests for the SglCta base class.

These cover class/instance identity and the value-equality semantics used to
compare and de-duplicate CTAs.
"""

from sglduck.cta import SglCta, SglCtaIdentity


def test_base_is_instantiable():
    assert isinstance(SglCta(), SglCta)


def test_subclass_is_an_sgl_cta():
    assert isinstance(SglCtaIdentity(), SglCta)


def test_same_class_instances_are_equal_and_hash_alike():
    assert SglCta() == SglCta()
    assert hash(SglCta()) == hash(SglCta())


def test_different_classes_are_not_equal():
    assert SglCta() != SglCtaIdentity()
