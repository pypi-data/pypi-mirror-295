import honeyhive
import os
from honeyhive.models import components, operations
from honeyhive.utils.telemetry import Telemetry
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter
from traceloop.sdk import Traceloop
from traceloop.sdk.tracing.tracing import TracerWrapper
from traceback import print_exc


class HoneyHiveTracer:
    _is_traceloop_initialized = False
    session_id = None
    api_key = None

    @staticmethod
    def init(
        api_key,
        project,
        session_name,
        source,
        server_url="https://api.honeyhive.ai",
        disable_batch=False,
        verbose=False,
    ):
        try:
            HoneyHiveTracer.verbose = verbose
            session_id = HoneyHiveTracer.__start_session(
                api_key, project, session_name, source, server_url
            )
            Telemetry().capture("tracer_init", {"hhai_session_id": session_id})
            if not HoneyHiveTracer._is_traceloop_initialized:
                Traceloop.init(
                    api_endpoint=f"{server_url}/opentelemetry",
                    api_key=api_key,
                    metrics_exporter=ConsoleMetricExporter(out=open(os.devnull, "w")),
                    disable_batch=disable_batch,
                )
                HoneyHiveTracer._is_traceloop_initialized = True
            Traceloop.set_association_properties({"session_id": session_id})
            HoneyHiveTracer.session_id = session_id
            HoneyHiveTracer.api_key = api_key
        except:
            if HoneyHiveTracer.verbose:
                print_exc()
            else:
                pass

    @staticmethod
    def init_from_session_id(
        api_key,
        session_id,
        server_url="https://api.honeyhive.ai",
    ):
        try:
            if not HoneyHiveTracer._is_traceloop_initialized:
                Traceloop.init(
                    api_endpoint=f"{server_url}/opentelemetry",
                    api_key=api_key,
                    metrics_exporter=ConsoleMetricExporter(out=open(os.devnull, "w")),
                )
                HoneyHiveTracer._is_traceloop_initialized = True
            Traceloop.set_association_properties({"session_id": session_id})
            HoneyHiveTracer.session_id = session_id
            HoneyHiveTracer.api_key = api_key
        except:
            if HoneyHiveTracer.verbose:
                print_exc()
            else:
                pass

    @staticmethod
    def __start_session(api_key, project, session_name, source, server_url):
        sdk = honeyhive.HoneyHive(bearer_auth=api_key, server_url=server_url)
        res = sdk.session.start_session(
            request=operations.StartSessionRequestBody(
                session=components.SessionStartRequest(
                    project=project,
                    session_name=session_name,
                    source=source,
                )
            )
        )
        assert res.object.session_id is not None
        return res.object.session_id

    @staticmethod
    def set_feedback(feedback):
        if HoneyHiveTracer.session_id is None:
            raise Exception("HoneyHiveTracer is not initialized")
        session_id = HoneyHiveTracer.session_id
        try:
            sdk = honeyhive.HoneyHive(HoneyHiveTracer.api_key)
            sdk.events.update_event(
                request=operations.UpdateEventRequestBody(
                    event_id=session_id, feedback=feedback
                )
            )
        except:
            if HoneyHiveTracer.verbose:
                print_exc()
            else:
                pass

    @staticmethod
    def set_metric(metrics):
        if HoneyHiveTracer.session_id is None:
            raise Exception("HoneyHiveTracer is not initialized")
        session_id = HoneyHiveTracer.session_id
        try:
            sdk = honeyhive.HoneyHive(HoneyHiveTracer.api_key)
            sdk.events.update_event(
                request=operations.UpdateEventRequestBody(
                    event_id=session_id,
                    metrics=metrics,
                )
            )
        except:
            if HoneyHiveTracer.verbose:
                print_exc()
            else:
                pass

    @staticmethod
    def set_metadata(metadata):
        if HoneyHiveTracer.session_id is None:
            raise Exception("HoneyHiveTracer is not initialized")
        session_id = HoneyHiveTracer.session_id
        try:
            sdk = honeyhive.HoneyHive(HoneyHiveTracer.api_key)
            sdk.events.update_event(
                request=operations.UpdateEventRequestBody(
                    event_id=session_id, metadata=metadata
                )
            )
        except:
            if HoneyHiveTracer.verbose:
                print_exc()
            else:
                pass

    @staticmethod
    def flush():
        TracerWrapper().flush()
