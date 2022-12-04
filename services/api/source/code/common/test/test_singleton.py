from common.singleton import Singleton
from random import randint


def test_singleton_class_always_return_same_instance():
    class TestClassNoInit(metaclass=Singleton):
        ...

    first = TestClassNoInit()

    second = TestClassNoInit()

    assert hex(id(first)) == hex(id(second))


def test_singleton_class_accepts_arguments_on_the_first_creation():
    class TestClass(metaclass=Singleton):
        state: int
        def __init__(self, state: int) -> None:
            self.state = state
    expected_value = randint(1, 100)

    TestClass(state=expected_value)

    no_args = TestClass()

    assert no_args.state == expected_value


def test_singleton_class_do_not_accept_arguments_after_first_creation():
    class TestClass(metaclass=Singleton):
        state: int
        def __init__(self, state: int) -> None:
            self.state = state
    expected_value = randint(1, 100)

    TestClass(state=expected_value)

    not_really_a_new_instance = TestClass(state=expected_value + 1)

    assert not_really_a_new_instance.state == expected_value


def test_singleton_clear_method_should_reset_singleton():
    class TestClass(metaclass=Singleton):
        state: int
        def __init__(self, state: int) -> None:
            self.state = state

    val = randint(1, 100)
    cls = TestClass(state=val)
    Singleton.clear(cls.__class__)

    val = val + 1
    cls = TestClass(state=val)
    
    assert cls.state == val


def test_singleton_clear_method_should_not_raise_exception_if_not_exist():
    Singleton.clear(None)
    assert 1 == 1