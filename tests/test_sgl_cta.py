"""Port of rsgl's test-sgl_cta.R (the SglCta base class).

rsgl's construction tests assert S3 internals (class attribute chain, empty-list
base object); the Pythonic equivalents are class/instance identity and the
value-equality semantics that replace R's ``identical()`` / ``%in%``.
"""

from pysgl.cta import SglCta, SglCtaIdentity


def test_base_is_instantiable():
    assert isinstance(SglCta(), SglCta)


def test_subclass_is_an_sgl_cta():
    assert isinstance(SglCtaIdentity(), SglCta)


def test_same_class_instances_are_equal_and_hash_alike():
    assert SglCta() == SglCta()
    assert hash(SglCta()) == hash(SglCta())


def test_different_classes_are_not_equal():
    assert SglCta() != SglCtaIdentity()
