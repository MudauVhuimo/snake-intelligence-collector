"""Scheduled redundant runs must skip if the previous archive is fresh."""
from datetime import datetime,timedelta,timezone
import unittest
from research.schedule_guard import parse_generated,should_collect

class ScheduleGuardTests(unittest.TestCase):
    def test_old_archive_needs_collection_and_recent_does_not(self):
        now=datetime(2026,11,2,6,30,tzinfo=timezone.utc)
        self.assertTrue(should_collect(now-timedelta(minutes=60),now))
        self.assertFalse(should_collect(now-timedelta(minutes=25),now))
        self.assertFalse(should_collect(now-timedelta(minutes=49),now))
        self.assertTrue(should_collect(now-timedelta(minutes=50),now))
        self.assertTrue(should_collect(None,now))
    def test_manual_override_and_clock_drift(self):
        now=datetime(2026,11,2,6,30,tzinfo=timezone.utc)
        self.assertTrue(should_collect(now,now,force=True))
        self.assertTrue(should_collect(now+timedelta(hours=2),now))
    def test_require_timezone_aware_generated_header(self):
        text="# Collection\nGenerated (UTC): 2026-11-02T00:42:14+00:00\n"
        self.assertEqual(parse_generated(text),datetime(2026,11,2,0,42,14,tzinfo=timezone.utc))
        self.assertIsNone(parse_generated("Generated (UTC): 2026-11-02T00:42:14"))
        self.assertIsNone(parse_generated("garbled report"))
if __name__=="__main__":
    unittest.main()
