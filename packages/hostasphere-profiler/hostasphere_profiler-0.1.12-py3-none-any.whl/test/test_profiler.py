import unittest

from profiler.core import Profiler

profiler = Profiler(
    address='localhost:50051',
    token='hsp_012e03f598f302a750ba14b09a41b7871693dc11c2efa8bc6405b3083a2cdb41',
    session_tag='test_session_2'
)


class TestProfiler(unittest.TestCase):
    @profiler.track()
    def sample_function(self, start, end):
        return sum(range(start, end))

    def test_sample_function(self):
        result = self.sample_function(1, 1000)
        self.assertEqual(result, sum(range(1000)))

        try:
            Profiler(address='localhost:50051', token='invalid_token')
        except Exception as e:
            self.assertEqual(str(e), 'Invalid token')
        try:
            Profiler(address='localhost:50052', token='dummy_token')
        except Exception as e:
            self.assertEqual(str(e), 'Invalid address, target is not a hostaspere server')


if __name__ == '__main__':
    unittest.main()
