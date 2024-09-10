# -*- coding: UTF-8 -*-

import abc
from muso.request import MusoRequest


class AuthBase(abc.ABC):

    def __init__(self):
        self.uri = None
        self.method = None

    def fill_uri_and_method(self, *, uri: str, method: str):
        self.uri = uri
        self.method = method

    @property
    @abc.abstractmethod
    def auth_name(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def auth_type(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, *, request: MusoRequest):
        raise NotImplementedError
