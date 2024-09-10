import unittest
from unittest.mock import patch
from datetime import datetime
import pytz

from ruwanvm.misc.timestamp import Timestamp


class TestTimestampLibrary(unittest.TestCase):

    @patch('ruwanvm.misc.timestamp.datetime')
    def test_current_timestamp(self, mock_datetime):
        expected_results = 1725148800  # timestamp for 2024/9/1 00:00:00 UTC time

        mock_now = datetime(2024, 9, 1, 0, 0, 0, tzinfo=pytz.utc)
        mock_datetime.now.return_value = mock_now
        results = Timestamp.current_timestamp()

        self.assertEqual(results, expected_results)

    @patch('ruwanvm.misc.timestamp.datetime')
    def test_current_timestamp_for_timezone(self, mock_datetime):
        expected_results = 1725166800  # timestamp for 2024/9/1 00:00:00 EST time

        mock_now = datetime(2024, 9, 1, 0, 0, 0, tzinfo=pytz.timezone('EST'))
        mock_datetime.now.return_value = mock_now
        results = Timestamp.current_timestamp(timezone='EST')

        self.assertEqual(results, expected_results)

    def test_timestamp_to_datetime(self):
        expected_results = "2024/09/01 00:00:00"

        result = Timestamp.timestamp_to_datetime(1725148800)

        self.assertEqual(result, expected_results)

    def test_timestamp_to_datetime_with_timezone(self):
        expected_results = "2024/09/01 00:00:00"

        result = Timestamp.timestamp_to_datetime(1725105600, timezone='Pacific/Auckland')

        self.assertEqual(result, expected_results)

    def test_timestamp_to_datetime_with_timezone_format(self):
        expected_results = "2024-09-01 00:00:00"

        result = Timestamp.timestamp_to_datetime(1725166800, timezone='EST', time_format='%Y-%m-%d %H:%M:%S')

        self.assertEqual(result, expected_results)

    def test_datetime_to_timestamp(self):
        expected_results = 1725148800

        result = Timestamp.datetime_to_timestamp("2024/09/01 00:00:00")

        self.assertEqual(result, expected_results)

    def test_datetime_to_timestamp_with_timezone(self):
        expected_results = 1725105600

        result = Timestamp.datetime_to_timestamp("2024/09/01 00:00:00", timezone='Pacific/Auckland')

        self.assertEqual(result, expected_results)

    def test_datetime_to_timestamp_with_timezone_format(self):
        expected_results = 1725166800

        result = Timestamp.datetime_to_timestamp(
            "2024-09-01 00:00:00",
            timezone='EST',
            time_format='%Y-%m-%d %H:%M:%S'
        )

        self.assertEqual(result, expected_results)


if __name__ == '__main__':
    unittest.main()
