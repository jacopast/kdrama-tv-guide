import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('guide', Path(__file__).parents[1] / 'fetch_kdrama_schedule.py')
guide = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guide)


class PlatformScheduleTests(unittest.TestCase):
    def test_unknown_platform_date_does_not_inherit_korean_broadcast(self):
        drama = {'schedule': {'2026-11-16': 'EP 01'}, 'isBatch': False}
        self.assertEqual(guide.effective_for_channel(drama, {'schedule': {}})['schedule'], {})
        self.assertEqual(guide.effective_for_channel(drama, {})['schedule'], drama['schedule'])

    def test_disney_plus_appears_in_shared_channel(self):
        platform = {'name': 'Disney+', 'regions': ['KR'], 'url': 'https://www.disneyplus.com/'}
        self.assertIs(guide.drama_platform_for({'platforms': [platform]}, 'Hulu'), platform)


if __name__ == '__main__':
    unittest.main()
