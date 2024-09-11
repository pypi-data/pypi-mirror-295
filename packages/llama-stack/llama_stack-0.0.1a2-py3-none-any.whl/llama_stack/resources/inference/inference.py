# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...types import inference_completion_params, inference_chat_completion_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .embeddings import (
    EmbeddingsResource,
    AsyncEmbeddingsResource,
    EmbeddingsResourceWithRawResponse,
    AsyncEmbeddingsResourceWithRawResponse,
    EmbeddingsResourceWithStreamingResponse,
    AsyncEmbeddingsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.completion_stream_chunk import CompletionStreamChunk
from ...types.chat_completion_stream_chunk import ChatCompletionStreamChunk

__all__ = ["InferenceResource", "AsyncInferenceResource"]


class InferenceResource(SyncAPIResource):
    @cached_property
    def embeddings(self) -> EmbeddingsResource:
        return EmbeddingsResource(self._client)

    @cached_property
    def with_raw_response(self) -> InferenceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return InferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InferenceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return InferenceResourceWithStreamingResponse(self)

    def chat_completion(
        self,
        *,
        request: inference_chat_completion_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionStreamChunk:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "text/event-stream", **(extra_headers or {})}
        return self._post(
            "/inference/chat_completion",
            body=maybe_transform({"request": request}, inference_chat_completion_params.InferenceChatCompletionParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCompletionStreamChunk,
        )

    def completion(
        self,
        *,
        request: inference_completion_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionStreamChunk:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/inference/completion",
            body=maybe_transform({"request": request}, inference_completion_params.InferenceCompletionParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompletionStreamChunk,
        )


class AsyncInferenceResource(AsyncAPIResource):
    @cached_property
    def embeddings(self) -> AsyncEmbeddingsResource:
        return AsyncEmbeddingsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncInferenceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInferenceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return AsyncInferenceResourceWithStreamingResponse(self)

    async def chat_completion(
        self,
        *,
        request: inference_chat_completion_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionStreamChunk:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "text/event-stream", **(extra_headers or {})}
        return await self._post(
            "/inference/chat_completion",
            body=await async_maybe_transform(
                {"request": request}, inference_chat_completion_params.InferenceChatCompletionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCompletionStreamChunk,
        )

    async def completion(
        self,
        *,
        request: inference_completion_params.Request,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionStreamChunk:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/inference/completion",
            body=await async_maybe_transform(
                {"request": request}, inference_completion_params.InferenceCompletionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompletionStreamChunk,
        )


class InferenceResourceWithRawResponse:
    def __init__(self, inference: InferenceResource) -> None:
        self._inference = inference

        self.chat_completion = to_raw_response_wrapper(
            inference.chat_completion,
        )
        self.completion = to_raw_response_wrapper(
            inference.completion,
        )

    @cached_property
    def embeddings(self) -> EmbeddingsResourceWithRawResponse:
        return EmbeddingsResourceWithRawResponse(self._inference.embeddings)


class AsyncInferenceResourceWithRawResponse:
    def __init__(self, inference: AsyncInferenceResource) -> None:
        self._inference = inference

        self.chat_completion = async_to_raw_response_wrapper(
            inference.chat_completion,
        )
        self.completion = async_to_raw_response_wrapper(
            inference.completion,
        )

    @cached_property
    def embeddings(self) -> AsyncEmbeddingsResourceWithRawResponse:
        return AsyncEmbeddingsResourceWithRawResponse(self._inference.embeddings)


class InferenceResourceWithStreamingResponse:
    def __init__(self, inference: InferenceResource) -> None:
        self._inference = inference

        self.chat_completion = to_streamed_response_wrapper(
            inference.chat_completion,
        )
        self.completion = to_streamed_response_wrapper(
            inference.completion,
        )

    @cached_property
    def embeddings(self) -> EmbeddingsResourceWithStreamingResponse:
        return EmbeddingsResourceWithStreamingResponse(self._inference.embeddings)


class AsyncInferenceResourceWithStreamingResponse:
    def __init__(self, inference: AsyncInferenceResource) -> None:
        self._inference = inference

        self.chat_completion = async_to_streamed_response_wrapper(
            inference.chat_completion,
        )
        self.completion = async_to_streamed_response_wrapper(
            inference.completion,
        )

    @cached_property
    def embeddings(self) -> AsyncEmbeddingsResourceWithStreamingResponse:
        return AsyncEmbeddingsResourceWithStreamingResponse(self._inference.embeddings)
