import psutil
import time


def getBandwidth():
    net_io = psutil.net_io_counters()
    total_bandwidth = net_io.bytes_sent + net_io.bytes_recv
    return int(total_bandwidth)


def limit_bandwidth(max_bytes_per_second):
    def decorator(func):
        def wrapper(*args, **kwargs):
            bytes_per_second = len(args) + sum(len(v) for v in kwargs.values())
            delay = float(bytes_per_second) / max_bytes_per_second
            if delay > 0:
                time.sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator
