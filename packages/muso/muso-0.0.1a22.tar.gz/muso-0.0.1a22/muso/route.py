# -*- coding: UTF-8 -*-

import asyncio
import functools
import inspect
from typing import Callable, List

from marshmallow import Schema, fields
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response as StarletteResponse

from muso.auth import AuthBase
from muso.request import MusoRequest
from muso.response import ORJSONResponse
from muso.schema import BaseSchema, EmptyResponseSchema


class RouteGroup:

    def __init__(self, *, prefix: str, tag: str, description: str = ''):
        self.prefix: str = prefix
        self.tag: str = tag
        self.description: str = description
        self.route_list: List[Route] = []

    def _register(
            self, *, uri: str, method: str, headers: Schema | None,
            query_args: Schema | None, form_data: Schema | None,
            json_body: Schema | None, response: Schema | None,
            auth: AuthBase | None, is_streaming_response: bool, summary: str,
    ) -> Callable:

        def decorator(endpoint_function):
            if auth:
                auth.fill_uri_and_method(uri=uri, method=method)
            _parameters = inspect.signature(obj=endpoint_function).parameters
            _contains_request = bool('request' in _parameters.keys())
            _contains_current_user = bool('current_user' in _parameters.keys())
            _is_coroutine_function = asyncio.iscoroutinefunction(
                endpoint_function)
            if response:
                _wrapped_response_schema_cls = BaseSchema.from_dict(
                    fields=dict(
                        code=fields.Integer(required=True),
                        msg=fields.String(required=True, allow_none=True),
                        data=fields.Nested(nested=response, allow_none=True),
                    ),
                    name=f'Wrapped{response.__class__.__name__}',
                )
                _wrapped_response = _wrapped_response_schema_cls()
            else:
                _wrapped_response = EmptyResponseSchema()

            @functools.wraps(endpoint_function)
            async def wrapper(request: StarletteRequest):
                muso_request = MusoRequest(
                    starlette_request=request,
                    query_args_schema=query_args,
                    form_data_schema=form_data,
                    json_body_schema=json_body,
                )
                arguments = dict()
                if _contains_request:
                    arguments['request'] = muso_request

                auth_to_current_user = None
                if auth:
                    auth_to_current_user = auth(request=muso_request)
                    if asyncio.iscoroutine(auth_to_current_user):
                        auth_to_current_user = await auth_to_current_user
                if _contains_current_user:
                    arguments['current_user'] = auth_to_current_user

                if _is_coroutine_function:
                    result = await endpoint_function(**arguments)
                else:
                    result = await run_in_threadpool(
                        func=endpoint_function, **arguments)
                if isinstance(result, StarletteResponse):
                    return result
                return ORJSONResponse(
                    content=_wrapped_response.dump(
                        dict(code=0, msg='', data=result)))

            self.route_list.append(Route(
                path=f'{self.prefix}{uri}', method=method, endpoint=wrapper,
                headers_schema=headers, query_args_schema=query_args,
                form_data_schema=form_data, json_body_schema=json_body,
                response_schema=_wrapped_response,
                auth=auth,
                is_streaming_response=is_streaming_response,
                summary=summary))
            return wrapper

        return decorator

    def get(self, *, uri: str,
            headers: Schema | None = None,
            query_args: Schema | None = None,
            response: Schema | None = None,
            auth: AuthBase | None = None,
            is_streaming_response: bool = False,
            summary: str = '') -> Callable:
        return self._register(
            uri=uri, method='GET', headers=headers, query_args=query_args,
            form_data=None, json_body=None, response=response, auth=auth,
            is_streaming_response=is_streaming_response, summary=summary)

    def post(self, *, uri: str,
             headers: Schema | None = None,
             query_args: Schema | None = None,
             form_data: Schema | None = None,
             json_body: Schema | None = None,
             response: Schema | None = None,
             auth: AuthBase | None = None,
             is_streaming_response: bool = False,
             summary: str = '') -> Callable:
        if form_data and json_body:
            raise SyntaxError(
                'form_data and json_body cannot be used together')
        return self._register(
            uri=uri, method='POST', headers=headers, query_args=query_args,
            form_data=form_data, json_body=json_body, response=response,
            auth=auth, is_streaming_response=is_streaming_response,
            summary=summary)

    def put(self, *, uri: str,
            headers: Schema | None = None,
            query_args: Schema | None = None,
            form_data: Schema | None = None,
            json_body: Schema | None = None,
            response: Schema | None = None,
            auth: AuthBase | None = None,
            is_streaming_response: bool = False,
            summary: str = '') -> Callable:
        if form_data and json_body:
            raise SyntaxError(
                'form_data and json_body cannot be used together')
        return self._register(
            uri=uri, method='PUT', headers=headers, query_args=query_args,
            form_data=form_data, json_body=json_body, response=response,
            auth=auth, is_streaming_response=is_streaming_response,
            summary=summary)

    def delete(self, *, uri: str,
               headers: Schema | None = None,
               query_args: Schema | None = None,
               response: Schema | None = None,
               auth: AuthBase | None = None,
               is_streaming_response: bool = False,
               summary: str = '') -> Callable:
        return self._register(
            uri=uri, method='DELETE', headers=headers, query_args=query_args,
            form_data=None, json_body=None, response=response, auth=auth,
            is_streaming_response=is_streaming_response, summary=summary)


class Route:

    def __init__(self, *, path: str, method: str, endpoint: Callable,
                 headers_schema: Schema,
                 query_args_schema: Schema | None,
                 form_data_schema: Schema | None,
                 json_body_schema: Schema | None,
                 response_schema: Schema | None,
                 auth: AuthBase | None,
                 is_streaming_response: bool = False,
                 summary: str):
        self.path = path
        self.method = method
        self.endpoint = endpoint
        self.headers_schema = headers_schema
        self.query_args_schema = query_args_schema
        self.form_data_schema = form_data_schema
        self.json_body_schema = json_body_schema
        self.response_schema = response_schema
        self.auth = auth
        self.is_streaming_response = is_streaming_response
        self.summary = summary
