import os
import platform
import threading
import time
import uuid
from copy import deepcopy
from time import sleep

import grpc
import psutil

from . import session_pb2_grpc, session_pb2


class Session:
    def __init__(self, address: str, token: str, token_id: str,
                 refresh_interval: float = 0.1, session_tag: str = ''):
        self._address = address
        self._token = token
        self._refresh_interval = refresh_interval
        self._track_annotations = []
        self.metrics = session_pb2.Session()
        self.metrics.start_time = time.time()
        self.metrics.start_date = int(time.time() * 1000)
        self.metrics.session_uuid = str(uuid.uuid4())
        self.metrics.session_tag = session_tag
        self.metrics.token_id = token_id
        self.collect_system_info()

        self._stop_event = threading.Event()  # Event to signal the thread to stop

        self.save_thread = threading.Thread(target=self.save_metrics, daemon=True)
        self.save_thread.start()

    def collect_system_info(self):
        self.metrics.pid = os.getpid()
        self.metrics.hostname = platform.node()
        self.metrics.os = platform.system()
        self.metrics.os_version = platform.version()
        self.metrics.kernel_version = platform.release()
        self.metrics.architecture = platform.machine()
        self.metrics.python_version = platform.python_version()
        self.metrics.processor = platform.processor()
        self.metrics.cpu_count = os.cpu_count()
        self.metrics.boot_time = psutil.boot_time()
        self.metrics.current_user = os.getlogin()

    def record_usage(self):
        current_time = time.time()

        # Record memory usage
        memory_usage = deepcopy(psutil.virtual_memory().percent)
        self.metrics.memory_usage.append(
            session_pb2.UsageAtTime(time=current_time, memory_usage=memory_usage))

        # Record CPU usage
        cpu_usage = deepcopy(psutil.cpu_percent(interval=None))
        self.metrics.cpu_usage.append(
            session_pb2.UsageAtTime(time=current_time, memory_usage=cpu_usage))

        # Record disk usage
        disk_usage = deepcopy(psutil.disk_usage('/').percent)
        self.metrics.disk_usage.append(
            session_pb2.UsageAtTime(time=current_time, memory_usage=disk_usage))

        # Record network usage
        net_io = deepcopy(psutil.net_io_counters())
        network_usage = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)  # Convert to MB
        self.metrics.network_usage.append(
            session_pb2.UsageAtTime(time=current_time, memory_usage=network_usage))

    def save_metrics(self):
        try:
            while not self._stop_event.is_set():
                self.record_usage()
                sleep(self._refresh_interval)  # Simulate time interval for metrics recording
        except KeyboardInterrupt:
            self.end_session()

    def end_session(self):
        self._stop_event.set()  # Signal the thread to stop
        self.save_thread.join()  # Wait for the thread to finish
        self.record_usage()
        self.metrics.end_time = time.time()
        self.metrics.end_date = int(time.time() * 1000)
        self.metrics.execution_time = (self.metrics.end_time - self.metrics.start_time) * 1000  # milliseconds
        self.metrics.track_annotations.extend(self._track_annotations)
        self.save_session()

    def save_session(self):
        with grpc.insecure_channel(self._address) as channel:
            stub = session_pb2_grpc.SessionServiceStub(channel)
            request = session_pb2.SaveSessionRequest(token=self._token, session=self.metrics)
            response = stub.SaveSession(request)
            return response

    def add_annotation(self, annotation: str, color: str = '#000000'):
        self._track_annotations.append(
            session_pb2.TrackAnnotation(time=time.time(), annotation=annotation, color=color))
