import logging
import sys
import unittest
from functools import reduce
from typing import List, Dict

# pylint: disable=C0103
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


class BasePerformanceTest(unittest.TestCase):
    """
    The base class for performance tests that has some nice useful methods.
    """

    def assert_route_performance(self,
                                 route: str,
                                 stats: List[Dict],
                                 min_avg_call_rate: float,
                                 max_error_rate: float,
                                 max_avg_latency: float,
                                 max_90th_latency: float,
                                 max_95th_latency: float):
        """
        Asserts the performance of a route based on the statistics given by Locust (version ~1.2)
        @param route: The name of the route in the runner to verify.
        @param stats: The stats object from Locust after the test has been completed.
        @param min_avg_call_rate: The minimum call rate that the test should call on average (after a 30 second warmup)
        @param max_error_rate: The maximum total error rate for this route.
        @param max_avg_latency: The maximum allowed average latency for this route.
        @param max_90th_latency: The maximum allowed 90th percentile latency for this route.
        @param max_95th_latency: The maximum allowed 95th percentile latency for this route.
        """
        route_stats = next(filter(lambda stat: stat['name'] == route, stats))
        error_rate = self._get_error_rate(route_stats)
        print(f"Stats for: '{route}'")
        print(f"\tError rate: {error_rate}")
        avg_calls_per_second = self._get_averaged_calls_per_second(route_stats)
        print(f"\tAverages calls per second: {avg_calls_per_second}")
        avg_latency = self._get_percentage_latency(route_stats, 0.5)
        print(f"\tAverage latency: {avg_latency}")
        ninety_th_latency = self._get_percentage_latency(route_stats, 0.9)
        print(f"\t90th percentile latency: {ninety_th_latency}")
        ninety_fifth_latency = self._get_percentage_latency(route_stats, 0.95)
        print(f"\t95th percentile latency: {ninety_fifth_latency}")
        assert ninety_th_latency <= max_90th_latency, \
            f"90th percentile latency should be less than {max_90th_latency} milliseconds"
        assert avg_latency <= max_avg_latency, f"Average latency should be less than {avg_latency} milliseconds"
        assert error_rate <= max_error_rate, "Launch should have a very small number of errors"
        assert avg_calls_per_second > min_avg_call_rate, "Should call launch at least 1 per second"
        assert ninety_fifth_latency <= max_95th_latency, \
            f"95th percentile latency should be less than {max_95th_latency} milliseconds"

    @staticmethod
    def _get_percentage_latency(route_stats: Dict, percentage: float):
        latencies = sorted(BasePerformanceTest._get_stat_latencies_list(route_stats))
        return latencies[int(len(latencies) * percentage)]

    @staticmethod
    def _get_stat_latencies_list(route_stats):
        latencies = []
        for latency_group_time_ms in route_stats['response_times'].keys():
            for _ in range(route_stats['response_times'][latency_group_time_ms]):
                latencies.append(int(latency_group_time_ms))
        return latencies

    @staticmethod
    def _get_error_rate(route_stats: Dict) -> float:
        if route_stats['num_failures'] == 0:
            return 0
        return route_stats['num_failures'] / route_stats['num_requests']

    @staticmethod
    def _get_averaged_calls_per_second(route_stats: Dict, warm_up_period: int = 5) -> float:
        start_time = int(route_stats['start_time'])
        start_time_with_warmup = start_time + warm_up_period
        end_time = int(route_stats['last_request_timestamp'])
        req_bins = route_stats['num_reqs_per_sec']
        total_calls = reduce(lambda x, y: x + y,
                             [req_bins[key] for key in req_bins.keys() if key >= start_time_with_warmup])
        return total_calls / (end_time - start_time_with_warmup)
