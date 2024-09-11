"""
Tests for diagnostic middleware.
"""

import re
from unittest.mock import Mock, patch

import ddt
import ddtrace
from django.test import TestCase, override_settings

from ..middleware import DETECT_ANOMALOUS_TRACE, LOG_ROOT_SPAN, DatadogDiagnosticMiddleware


def fake_view(_request):
    """Fake get_response for middleware."""


@ddt.ddt
class TestDatadogDiagnosticMiddleware(TestCase):
    """Tests for DatadogDiagnosticMiddleware."""

    def make_middleware(self):
        """Make an instance of the middleware with current settings."""
        return DatadogDiagnosticMiddleware(fake_view)

    def run_middleware(self, middleware=None):
        """Run the middleware using a fake request."""
        if middleware is None:
            middleware = self.make_middleware()

        resolver = Mock()
        resolver.route = "/some/path"
        request = Mock()
        request.resolver_match = resolver

        middleware.process_view(request, None, None, None)

    @patch('edx_arch_experiments.datadog_diagnostics.middleware.log.error')
    def test_log_diagnostics_error_only_once(self, mock_log_error):
        """
        If the log_diagnostics function is broken, only log the error once.
        The method should still be called every time in case it is still doing
        useful work before the error, though.
        """
        middleware = self.make_middleware()

        bad_method = Mock(side_effect=lambda request: 1/0)
        middleware.log_diagnostics = bad_method

        self.run_middleware(middleware)
        self.run_middleware(middleware)

        # Called twice
        assert len(bad_method.call_args_list) == 2

        # But only log once
        mock_log_error.assert_called_once_with(
            "Encountered error in DatadogDiagnosticMiddleware (suppressing further errors): "
            "ZeroDivisionError('division by zero')"
        )

    @ddt.data(
        # Feature disabled
        (False, False),
        (False, True),
        # Enabled, but nothing anomalous
        (True, False),
        # Enabled and anomaly detected
        (True, True),
    )
    @ddt.unpack
    @patch('edx_arch_experiments.datadog_diagnostics.middleware.log.warning')
    def test_anomalous_trace(self, enabled, cause_anomaly, mock_log_warning):
        with (
                patch.object(DETECT_ANOMALOUS_TRACE, 'is_enabled', return_value=enabled),
                patch.object(LOG_ROOT_SPAN, 'is_enabled', return_value=False),
                # Need at least two levels of spans in order to fake
                # an anomaly. (Otherwise current_root_span returns None.)
                ddtrace.tracer.trace("local_root"),
                ddtrace.tracer.trace("intermediary_span"),
                ddtrace.tracer.trace("inner_span"),
        ):
            if cause_anomaly:
                ddtrace.tracer.current_root_span().finish()
            self.run_middleware()

        if enabled and cause_anomaly:
            mock_log_warning.assert_called_once()
            log_msg = mock_log_warning.call_args_list[0][0][0]  # first arg of first call

            assert re.fullmatch(
                r"Anomalous Datadog local root span: "
                r"trace_id=[0-9A-Fa-f]+; duration=[0-9]\.[0-9]{3}; worker_age=[0-9]\.[0-9]{3}; span ancestry:\n"
                r"name='local_root'.*duration=[0-9]+.*\n"
                r"name='intermediary_span'.*duration=None.*\n"
                r"name='inner_span'.*duration=None.*",
                log_msg
            )
        else:
            mock_log_warning.assert_not_called()

    @override_settings(DATADOG_DIAGNOSTICS_LOG_SPAN_DEPTH=2)
    @patch('edx_arch_experiments.datadog_diagnostics.middleware.log.warning')
    def test_anomalous_trace_truncation(self, mock_log_warning):
        """
        Test that truncation works, returning N most proximal spans.
        """
        with (
                patch.object(DETECT_ANOMALOUS_TRACE, 'is_enabled', return_value=True),
                patch.object(LOG_ROOT_SPAN, 'is_enabled', return_value=False),
                # Need at least two levels of spans in order to fake
                # an anomaly. (Otherwise current_root_span returns None.)
                ddtrace.tracer.trace("local_root"),
                ddtrace.tracer.trace("intermediary_span"),
                ddtrace.tracer.trace("inner_span"),
        ):
            ddtrace.tracer.current_root_span().finish()  # cause anomaly
            self.run_middleware()

        mock_log_warning.assert_called_once()
        log_msg = mock_log_warning.call_args_list[0][0][0]  # first arg of first call

        assert re.fullmatch(
            r"Anomalous Datadog local root span: "
            r"trace_id=[0-9A-Fa-f]+; duration=[0-9]\.[0-9]{3}; worker_age=[0-9]\.[0-9]{3}; span ancestry:\n"
            r"\(ancestors truncated\)\n"  # difference here
            r"name='intermediary_span'.*duration=None.*\n"
            r"name='inner_span'.*duration=None.*",
            log_msg
        )

    @patch('edx_arch_experiments.datadog_diagnostics.middleware.log.info')
    def test_log_root_span(self, mock_log_info):
        with (
                patch.object(DETECT_ANOMALOUS_TRACE, 'is_enabled', return_value=False),
                patch.object(LOG_ROOT_SPAN, 'is_enabled', return_value=True),
                # Need at least two levels of spans for interesting logging
                ddtrace.tracer.trace("local_root"),
                ddtrace.tracer.trace("inner_span"),
        ):
            self.run_middleware()

        mock_log_info.assert_called_once()
        log_msg = mock_log_info.call_args_list[0][0][0]  # first arg of first call
        assert re.fullmatch(
            r"Datadog span diagnostics: Route = /some/path; "
            r"local root span = name='local_root' .*; "
            r"current span = name='inner_span' .*",
            log_msg
        )
