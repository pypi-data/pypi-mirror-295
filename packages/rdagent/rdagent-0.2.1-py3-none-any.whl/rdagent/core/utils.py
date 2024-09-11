from __future__ import annotations

import importlib
import json
import multiprocessing as mp
import pickle
from collections.abc import Callable
from typing import Any, ClassVar, NoReturn, cast

from fuzzywuzzy import fuzz  # type: ignore[import-untyped]


class RDAgentException(Exception):  # noqa: N818
    pass


class SingletonBaseClass:
    """
    Because we try to support defining Singleton with `class A(SingletonBaseClass)`
    instead of `A(metaclass=SingletonMeta)` this class becomes necessary.
    """

    _instance_dict: ClassVar[dict] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        # Since it's hard to align the difference call using args and kwargs, we strictly ask to use kwargs in Singleton
        if args:
            # TODO: this restriction can be solved.
            exception_message = "Please only use kwargs in Singleton to avoid misunderstanding."
            raise RDAgentException(exception_message)
        class_name = [(-1, f"{cls.__module__}.{cls.__name__}")]
        args_l = [(i, args[i]) for i in args]
        kwargs_l = list(sorted(kwargs.items()))
        all_args = class_name + args_l + kwargs_l
        kwargs_hash = hash(tuple(all_args))
        if kwargs_hash not in cls._instance_dict:
            cls._instance_dict[kwargs_hash] = super().__new__(cls)  # Corrected call
        return cls._instance_dict[kwargs_hash]

    def __reduce__(self) -> NoReturn:
        """
        NOTE:
        When loading an object from a pickle, the __new__ method does not receive the `kwargs`
        it was initialized with. This makes it difficult to retrieve the correct singleton object.
        Therefore, we have made it unpickable.
        """
        msg = f"Instances of {self.__class__.__name__} cannot be pickled"
        raise pickle.PicklingError(msg)


def parse_json(response: str) -> Any:
    try:
        return json.loads(response)
    except json.decoder.JSONDecodeError:
        pass
    error_message = f"Failed to parse response: {response}, please report it or help us to fix it."
    raise ValueError(error_message)


def similarity(text1: str, text2: str) -> int:
    text1 = text1 if isinstance(text1, str) else ""
    text2 = text2 if isinstance(text2, str) else ""

    # Maybe we can use other similarity algorithm such as tfidf
    return cast(int, fuzz.ratio(text1, text2))  # mypy does not reguard it as int


def import_class(class_path: str) -> Any:
    """
    Parameters
    ----------
    class_path : str
        class path like"scripts.factor_implementation.baselines.naive.one_shot.OneshotFactorGen"

    Returns
    -------
        class of `class_path`
    """
    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def multiprocessing_wrapper(func_calls: list[tuple[Callable, tuple]], n: int) -> list:
    """It will use multiprocessing to call the functions in func_calls with the given parameters.
    The results equals to `return  [f(*args) for f, args in func_calls]`
    It will not call multiprocessing if `n=1`

    Parameters
    ----------
    func_calls : List[Tuple[Callable, Tuple]]
        the list of functions and their parameters
    n : int
        the number of subprocesses

    Returns
    -------
    list

    """
    if n == 1:
        return [f(*args) for f, args in func_calls]
    with mp.Pool(processes=n) as pool:
        results = [pool.apply_async(f, args) for f, args in func_calls]
        return [result.get() for result in results]
