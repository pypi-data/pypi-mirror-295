from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Mapping, Union

if TYPE_CHECKING:
    import ddtrace.context

try:
    import ddtrace
    from datadog.dogstatsd.base import statsd

    def safe_set_gauge(gauge: str, value: int | float):
        statsd.gauge(gauge, value)

    def safe_incr(counter: str, value: int | float):
        statsd.increment(counter, value)

    @contextlib.contextmanager
    def safe_trace(span_id: str):
        with ddtrace.tracer.trace(name=span_id):
            yield

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):
        span = ddtrace.tracer.current_span()
        if span:
            span.set_metrics({k: v for (k, v) in metrics.items()})

    def safe_add_tags(tags: Mapping[str, str]):
        span = ddtrace.tracer.current_span()
        if span:
            span.set_tags({k: v for (k, v) in tags.items()})

    def safe_current_trace_context():  # pyright: ignore[reportRedeclaration]
        return ddtrace.tracer.current_trace_context()

    def safe_activate_trace_context(
        ctx: ddtrace.context.Context | ddtrace.Span | None,  # pyright: ignore[reportPrivateImportUsage]
    ) -> None:
        ddtrace.tracer.context_provider.activate(ctx)

except ImportError:

    def safe_set_gauge(gauge: str, value: int | float):
        pass

    def safe_incr(counter: str, value: int | float):
        pass

    @contextlib.contextmanager
    def safe_trace(span_id: str):
        yield

    def safe_add_metrics(metrics: Mapping[str, Union[int, float]]):
        pass

    def safe_add_tags(tags: Mapping[str, str]):
        pass

    def safe_current_trace_context():
        return

    def safe_activate_trace_context(
        ctx: ddtrace.context.Context | ddtrace.Span | None,  # pyright: ignore[reportPrivateImportUsage]
    ) -> None:
        pass
