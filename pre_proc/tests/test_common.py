"""
test_common.py

Unit tests for pre_proc.common
"""
from abc import ABCMeta, abstractmethod
import unittest

from pre_proc.common import get_concrete_subclasses


class AbstractParent(object):
    """ Test parent abstract class """
    __metaclass__ = ABCMeta

    @abstractmethod
    def abstract_method(self):
        """ Dummy method """
        pass


class AbstractChild(AbstractParent):
    """ Test abstract child """
    __metaclass__ = ABCMeta

    @abstractmethod
    def abstract_method(self):
        """ Dummy method """
        pass


class ConcreteChild(AbstractParent):
    """ Test concrete child """
    def abstract_method(self):
        """ Concrete method """
        pass


class ConcreteSubChild(AbstractChild):
    """ Test concrete child of child """
    def abstract_method(self):
        """ Concrete method """
        pass


class TestGetConcreteSubclasses(unittest.TestCase):
    """ test pre_proc.common.get_concrete_subclasses """
    def test_all(self):
        """ Test that the whole hierarchy is returned """
        self.assertEqual(sorted([ConcreteChild, ConcreteSubChild]),
                         sorted(get_concrete_subclasses(AbstractParent)))

    def test_one(self):
        """ Test that a single child is returned """
        self.assertEqual([ConcreteSubChild],
                         get_concrete_subclasses(AbstractChild))

    def test_leaf(self):
        """ Test that nothing is returned if there are no children"""
        self.assertEqual([],
                         get_concrete_subclasses(ConcreteChild))
