import datetime
import sys
import argparse

from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest

import datetime
import time
from utilita import misc

import pendulum

class TestEverything(unittest.TestCase):

  def test__ymd_arg(self):

    self.assertEqual(misc.ymd_arg('2021-01-11'), datetime.date(2021,1,11))
    self.assertEqual(misc.ymd_arg('2021-1-11'), datetime.date(2021,1,11))

    with self.assertRaises(argparse.ArgumentTypeError):
      misc.ymd_arg('1-11-2021')

    with self.assertRaises(argparse.ArgumentTypeError):
      misc.ymd_arg('2021/01/11')

    with self.assertRaises(argparse.ArgumentTypeError):
      misc.ymd_arg('2021.01.11')

    self.assertEqual(misc.ymd_arg(None), None)

  def test__parse_templated(self):

    templated_greetings = {
      'keywords': {
        'thing': 'world'
      },
      'templates': {
        'hi': 'hello {thing}',
        'bye': 'laters {thing}'
      }
    }

    parsed_greetings = misc.parse_templated(templated_greetings)

    expected_greetings = {
      'hi': 'hello world',
      'bye': 'laters world'
    }

    self.assertEqual(parsed_greetings, expected_greetings)

    with self.assertRaises(TypeError):
      misc.parse_templated(None)

    with self.assertRaises(AssertionError):
      misc.parse_templated({})

    templated_dates = {
      'keywords': {
        'year': '2021'
      },
      'templates': {
        'start_date': '{year}-01-01',
        'end_date': '{year}-02-01'
      }
    }

    parsed_dates = misc.parse_templated(templated_dates, map_value=misc.ymd_arg)

    expected_dates = {
      'start_date': datetime.date(2021,1,1),
      'end_date': datetime.date(2021,2,1)
    }

    self.assertEqual(parsed_dates, expected_dates)


    # old name should yield a deprecation warning
    templated_compat = {
      'template_dict': { # old name
        'year': '2021'
      },
      'templates': {
        'start_date': '{year}-01-01',
      }
    }

    with self.assertWarns(PendingDeprecationWarning):
      misc.parse_templated(templated_compat, map_value=misc.ymd_arg)

  def test__parse_templated__w_formatted_keywords(self):

    templated_schematable_urls = {
      'keywords': {
        'dw':'postgresql://{user}:{pass}@localhost:5432/dw',
        'user': 'sysadmin', 
        'pass': 'password123'
      },
      'templates': {
        'product': '{dw}#product',
        'producer': '{dw}#producer',
      }
    }

    parsed_schematable_urls = misc.parse_templated(templated_schematable_urls)

    expected_schematable_urls = {
      'product': 'postgresql://sysadmin:password123@localhost:5432/dw#product',
      'producer': 'postgresql://sysadmin:password123@localhost:5432/dw#producer',
    }

    self.assertEqual(parsed_schematable_urls, expected_schematable_urls)

  def test__parse_templated__w_deep_recursive_formatted_keywords(self):

    templated_schematable_urls = {
      'keywords': {
        'dw_schema_url': '{dw_db_url}/dw',
        'dw_db_url':'postgresql://{user}:{pass}@localhost:5432',
        'user': 'sysadmin', 
        'pass': 'password123'
      },
      'templates': {
        'product': '{dw_schema_url}#product',
        'producer': '{dw_schema_url}#producer',
      }
    }

    parsed_schematable_urls = misc.parse_templated(templated_schematable_urls)

    expected_schematable_urls = {
      'product': 'postgresql://sysadmin:password123@localhost:5432/dw#product',
      'producer': 'postgresql://sysadmin:password123@localhost:5432/dw#producer',
    }

    self.assertEqual(parsed_schematable_urls, expected_schematable_urls)

  def test__parse_templated__w_extra_keywords(self):

    templated_db_urls = {
      'keywords': {
        'port':'5432'
      },
      'templates': {
        'dw_db_url': 'postgresql://{user}:{pass}@localhost:{port}/postgres',
      }
    }

    creds = {'user': 'sysadmin', 'pass': 'password123'}

    parsed_db_urls = misc.parse_templated(templated_db_urls, extra_keywords=creds)

    expected_db_urls = {
      'dw_db_url': "postgresql://sysadmin:password123@localhost:5432/postgres"
    }

    self.assertEqual(parsed_db_urls, expected_db_urls)

    templated_schematable_urls = {
      'keywords': {
        'dw':'postgresql://{user}:{pass}@localhost:5432/dw'
      },
      'templates': {
        'product': '{dw}#product',
        'producer': '{dw}#producer',
      }
    }

    creds = {'user': 'sysadmin', 'pass': 'password123'}

    parsed_schematable_urls = misc.parse_templated(templated_schematable_urls, extra_keywords=creds)

    expected_schematable_urls = {
      'product': 'postgresql://sysadmin:password123@localhost:5432/dw#product',
      'producer': 'postgresql://sysadmin:password123@localhost:5432/dw#producer',
    }

    self.assertEqual(parsed_schematable_urls, expected_schematable_urls)

  def test__pen2dt(self):

    pen = pendulum.create(2021,1,11)
    dt = misc.pen2dt(pen)
    self.assertEqual(type(dt), datetime.datetime)


  def test__timeit(self):
    sleeper = lambda duration: time.sleep(duration)

    try:
      timed_sleeper = misc.timeit(sleeper)
      timed_sleeper(1)
    except:
      self.fail('timeit decorated method raised an expection')

  def test__sql_arr_lit(self):

      self.assertEqual(
          misc.sql_arr_lit(['hello', 'world']), 
          "('hello', 'world')"
      )

      self.assertEqual(
          misc.sql_arr_lit([1, 2]), 
          "(1, 2)"
      )

      self.assertEqual(
          misc.sql_arr_lit(['hello']), 
          "('hello')"
      )

      self.assertRaises(
          AssertionError,
          lambda: misc.sql_arr_lit([])
      )


unittest.main()