import os

import gevent
from locust.env import Environment
from locust.stats import stats_printer, stats_history

from continuous_performance_testing.tests.base_performance_test import BasePerformanceTest
from continuous_performance_testing.tests.runner import ExampleUser


class TestExampleUserPerformance(BasePerformanceTest):
    """
    Class for API Performance Test
    """
    NUM_USERS = 200  # This will give us ~160 fast calls per second.
    TEST_DURATION_IN_SECONDS = 120  # 2 minutes

    def test_should_get_capital_invoices_and_checkout(self):
        # setup Environment and Runner
        host = os.environ.get('API_URL', 'http://continuous-test-server:5000')

        env = Environment(user_classes=[ExampleUser], host=host)
        env.create_local_runner()
        # start a greenlet that periodically outputs the current stats
        gevent.spawn(stats_printer(env.stats))
        # start a greenlet that save current stats to history
        gevent.spawn(stats_history, env.runner)
        env.runner.start(self.NUM_USERS, spawn_rate=10)
        # Schedule the test to end.
        gevent.spawn_later(self.TEST_DURATION_IN_SECONDS, lambda: env.runner.quit())
        # join and wait for the test to end.
        env.runner.greenlet.join()
        stats = env.runner.stats.serialize_stats()
        self.assert_route_performance(route="/fast",
                                      stats=stats,
                                      min_avg_call_rate=125,
                                      max_error_rate=0.00001,
                                      max_avg_latency=7,
                                      max_90th_latency=10,
                                      max_95th_latency=15)
        self.assert_route_performance(route="/slow",
                                      stats=stats,
                                      min_avg_call_rate=2.5,
                                      max_error_rate=0.00001,
                                      max_avg_latency=805,
                                      max_90th_latency=810,
                                      max_95th_latency=850)
