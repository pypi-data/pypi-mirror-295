import sys
from os import path
from typing import Type
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest

import datetime
from utilita import date_fns

class TestEverything(unittest.TestCase):

  def test_base(self):

    y2020w52d7 = datetime.date(2020,12,27)
    y2020w53d1 = datetime.date(2020,12,28)

    self.assertFalse(date_fns.is_in_leap_week(y2020w52d7)) # => False
    self.assertTrue(date_fns.is_in_leap_week(y2020w53d1)) # => True

    self.assertTrue(date_fns.is_in_week_prior_leap_week(y2020w52d7)) # => True
    self.assertFalse(date_fns.is_in_week_prior_leap_week(y2020w53d1)) # => False


    self.assertEqual(date_fns.days_since_same_date_last_year(y2020w52d7), 364) # => 364 (days in non-leep-week years)
    
    y2020w53 = [y2020w53d1 + datetime.timedelta(days=x) for x in range(7)]

    for date in y2020w53:
      self.assertEqual(date_fns.days_since_same_date_last_year(date), 371) # => 371 (days in leep-week years)


    y2021w1d1 = datetime.date(2021,1,4)
    y2021w52d7 = datetime.date(2022,1,2)
    y2022w1d1 = datetime.date(2022,1,3)

    self.assertFalse(date_fns.is_in_leap_week(y2021w1d1)) # => False
    self.assertEqual(date_fns.days_since_same_date_last_year(y2021w1d1), 371)
    self.assertEqual(date_fns.days_since_same_date_last_year(y2021w52d7), 371)
    self.assertEqual(date_fns.days_since_same_date_last_year(y2022w1d1), 364)


  def test__comp_yearwise__non_leapyear_non_leapweek_1y(self):
    run_dt = datetime.datetime(2019, 6, 6)
    expected_dt = datetime.datetime(2018, 6, 7)

    comp_dt = date_fns.comp_yearwise(run_dt, n_years = 1)

    self.assertEqual(comp_dt, expected_dt, f"expected {expected_dt}, got {comp_dt} instead")


  def test__comp_days_yearwise__non_leapyear_non_leapweek_2y(self):
    run_date = datetime.datetime(2019, 6, 6)
    expected_dt = datetime.datetime(2017, 6, 8)

    comp_dt = date_fns.comp_yearwise(run_date, n_years = 2)

    self.assertEqual(comp_dt, expected_dt, f"expected {expected_dt}, got {comp_dt} instead")


  def test__comp_days_yearwise__into_leapyear_from_normal(self):
    run_date = datetime.datetime(2021, 6, 6) # 2021 is after 2020 (leap week year!)
    expected_date = datetime.datetime(2020,6,7)

    comp_dt = date_fns.comp_yearwise(run_date, n_years = 1)

    self.assertEqual(comp_dt, expected_date, f"Leap year not handled: expected {expected_date}, got {comp_dt} instead")
      
  def test__days_between(self):
    a = datetime.date.today() 
    b = datetime.date.today() - datetime.timedelta(days=1)
    days = date_fns.days_between(a, b)
    expected_days = 1

    self.assertEqual(days, expected_days, f"expected days between {a} and {b} to be {expected_days} not {days}")

    days_flip = date_fns.days_between(b, a)
    expected_days_flip = -1

    self.assertEqual(days_flip, expected_days_flip, f"expected days between {b} and {a} to be {expected_days_flip} not {days_flip}")

  def test__safe_datetime(self):
    dt = datetime.datetime(2021, 1, 1)
    safe_dt = date_fns.safe_datetime(dt)
    self.assertEqual(type(safe_dt), datetime.datetime, f"{safe_dt} is not a datetime object")

    d = datetime.date(2021, 1, 1)
    safe_dt2 = date_fns.safe_datetime(d)
    self.assertEqual(type(safe_dt2), datetime.datetime, f"{safe_dt2} is not a datetime object")

    num = 1 
    self.assertRaises(TypeError, date_fns.safe_datetime, num)

unittest.main()