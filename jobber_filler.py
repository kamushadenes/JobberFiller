#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import base64
from time import sleep
from datetime import datetime, timedelta, date
from random import randint
import traceback
import os
from workalendar.america import BrazilSaoPauloCity, BrazilSaoPauloState, Brazil



# Jobber email
email="EMAIL"

# Use echo PASSWORD | base64 and put the result here
password="BASE64_PASSWD"

# Date is in YYYY/mm/dd format
first_date = '2015/07/01'

# Date is in YYYY/mm/dd format
last_date = '2015/07/31'

# Daily deviation in minutes, minimum and maximum
daily_deviation = (5,15)

# Use custom default?
use_custom_default = True

# Beggining of the first category
custom_default_category = '#80 -'
custom_default_text = 'This is my custom default text'

# Check https://pypi.python.org/pypi/workalendar/0.1 for possible values
cal = BrazilSaoPauloCity()


# Days of vacancy, you should't work on this days (I know, I know...)
vacancy = [
'2015/07/01',
'2015/07/02',
'2015/07/03',
'2015/07/04',
'2015/07/05',
]

# Fill weekends? Note that days on exceptional_dates will ALWAYS be filled
fill_weekends = False

# Fill holidays? Note that days on exceptional_dates will ALWAYS be filled
fill_holidays = False

# Fill only exceptional_dates
exceptional_only = False

# Add exceptional dates (e.g. dates where you trully want to specify the times) in the following format:
# 'YYYY/mm/dd': [('CATEGORY', 'NOTES', 'START_TIME', 'END_TIME')]

# On CATEGORY, you just need to specify the first distinguishable part of the string, as in '#9 -', or 'General'
# Hours need to follow the format HH.MM, as in 9.00, or HH only.

# If you add an hour without minutes (e.g. 9), get_deviated_time will be called, using daily_deviation to randomly choose a minute

# '2015/07/31': [('#80 -', 'Did something', '6.00', '9.00'), ('#9 -', 'Did something else', '10.00', '13.00')]

# Just add one per line and you should be ok, you can add more than one entry per day as normal, just dont expect me to check if you are overlapping things

# Dont use accents
exceptional_dates = {
    '2015/07/01': [('#80 -', 'Did everyday chores', '9.23', '12'), ('#5 -', 'Nothing', '13', '18')],
    '2015/07/06': [('#80 -', 'Did something cool', '9', '12'), ('#77 -', 'Did something boring', '13', '18.23')],

}


# Possible values: chrome, phantomjs, firefox (firefox is REALLY slow, don't recommend using it)
engine = 'chrome'

class JobberFiller(object):

    def get_deviated_time(self, base):
      return '{}.{:02}'.format(base, randint(self.daily_deviation[0], self.daily_deviation[1]))

    def generate_entry(self, entry_number, previous):
      sleep(0.1)
      text = ''
      try:
        el = self.driver.find_elements_by_css_selector('optgroup[label="Today"]')[entry_number]
      except IndexError:
        sleep(0.5)
        try:
          el = self.driver.find_element_by_css_selector('optgroup[label="Today"]')
        except:
          el = 'General'
      if el != 'General':
        for option in el.find_elements_by_tag_name('option'):
            text = option.text
            category = '{} -'.format(text.split('-')[0].strip())
            if use_custom_default:
              if category == custom_default_category:
                text = custom_default_text
            else:
              try:
                text = text.split('-')[2].strip()
              except:
                try:
                  text = text.split('-')[1].strip()
                except:
                  text = text
            break
      else:
        if previous == None:
          if use_custom_default:
            category = custom_default_category
            text = custom_default_text
          else:
            category = 'General'
            text = '.'
        else:
          category = previous[0]
          text = previous[1]
      if entry_number == 0:
        hour_start = self.get_deviated_time('9')
        hour_end = self.get_deviated_time('12')
      elif entry_number == 1:
        hour_start = self.get_deviated_time('13')
        hour_end = self.get_deviated_time('18')

      return (category, text, hour_start, hour_end)


    def daterange(self, start_date, end_date):
        for n in range(int ((end_date - start_date).days + 1)):
            yield start_date + timedelta(n)

    def get_driver(self):
      if hasattr(self, 'driver'):
        if self.driver != None:
          return self.driver
        else:

          if engine == 'chrome':
            chromedriver = "/usr/local/bin/chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            return driver

          elif engine == 'firefox'
            # Firefox is SLOW AS HELL
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.folderList', 2)
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference('browser.download.dir', '/tmp')
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'img/png')
            profile.native_events_enabled = True
            return webdriver.Firefox(profile)

          elif engine == 'phantomjs':
            # PhantomJS is OK
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'pt-BR'
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Connection'] = 'keep-alive'
            driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any', '--ignore-ssl-errors=yes'])
            return driver
          else:
            raise Exception('Invalid engine!')

    def __init__(self, email, password, first_date, last_date, exceptional_dates, daily_deviation, exceptional_only):
      self.email = email
      self.password = password
      fd = first_date.split('/')
      ld = last_date.split('/')
      self.first_date = date(int(fd[0]), int(fd[1]), int(fd[2]))
      self.last_date = date(int(ld[0]), int(ld[1]), int(ld[2]))
      self.exceptional_dates = exceptional_dates
      self.daily_deviation = daily_deviation
      self.exceptional_only = exceptional_only
      self.excel_location = excel_location
      self.driver = None
      self.driver = self.get_driver()
      self.driver.set_window_size(1120, 550)
      print('[*] JobberFiller is ready!')
      print('[*] First Date: {}'.format(self.first_date))
      print('[*] Last Date: {}'.format(self.last_date))
      print('[*] Work on weekends: {}'.format(fill_weekends))
      print('[*] Work on holidays: {}'.format(fill_holidays))



    def login(self):
      print('[*] Logging in...')
      self.driver.get("https://secure.getjobber.com/login")
      self.driver.find_element_by_id('email').send_keys(email)
      self.driver.find_element_by_id('user_session_password').send_keys(base64.b64decode(password))
      try:
        self.driver.find_element_by_id('submit').click()
      except:
        pass
      try:
        el = self.driver.find_element_by_class_name('flash--error')
        if 'Incorrect username or password' in el:
          print('[-] Invalid credentials, quitting...')
          self.quit()
      except:
        pass


    def fill_things_up(self):
      try:
        el = self.driver.find_element_by_class_name('flash--error')
        if 'Incorrect username or password' in el:
          print('[-] Invalid credentials, quitting...')
          self.quit()
      except:
        pass
      for single_date in self.daterange(self.first_date, self.last_date):
        date_str = single_date.strftime('%Y/%m/%d')
        if date_str in vacancy:
          print('[*] Skipping vacancy: {}'.format(date_str))
          continue
        self.driver.get('https://secure.getjobber.com/time_sheet/{}/day'.format(date_str))
        if self.exceptional_dates.get(date_str, False):
          print('[*] Filling date {}...'.format(date_str))
          entry_cnt = 0
          for entry in self.exceptional_dates[date_str]:
            print('[*] Inserting legit entry: {}'.format(entry))
            if entry_cnt != 0:
              self.driver.find_element_by_id('add_row').click()
            el = self.driver.find_elements_by_id('time_sheet_entry_work_order_id')[entry_cnt]
            for option in el.find_elements_by_tag_name('option'):
              if option.text.strip().startswith(entry[0]):
                option.click()
                break
            self.driver.find_elements_by_id('time_sheet_entry_note')[entry_cnt].send_keys(entry[1])
            sleep(0.5)
            if not '.' in entry[2]:
              self.driver.find_elements_by_id('time_sheet_entry_start_time')[entry_cnt].send_keys(self.get_deviated_time(entry[2]))
            else:
              self.driver.find_elements_by_id('time_sheet_entry_start_time')[entry_cnt].send_keys(entry[2])
            sleep(0.5)
            if not '.' in entry[3]:
              self.driver.find_elements_by_id('time_sheet_entry_end_time')[entry_cnt].send_keys(self.get_deviated_time(entry[3]))
            else:
              self.driver.find_elements_by_id('time_sheet_entry_end_time')[entry_cnt].send_keys(entry[3])
            sleep(0.5)
            self.driver.find_elements_by_name('commit')[entry_cnt].click()
            entry_cnt += 1
        else:
          if not exceptional_only:
            if single_date.weekday() in [5, 6]:
              if not fill_weekends:
                print('[*] Skipping weekend (lucky you!): {}'.format(date_str))
                continue
              else:
                print('[*] Filling weekend (sorry for you): {}'.format(date_str))

            if not cal.is_working_day(single_date):
              if not fill_holidays:
                print('[*] Skipping holiday (lucky you!): {}'.format(date_str))
                continue
              else:
                print('[*] Filling holiday (sorry for you): {}'.format(date_str))
            print('[*] Generating default entries...')
            entry_cnt = 0
            previous = None
            for entry_number in range(2):
              sleep(1)
              entry = self.generate_entry(entry_number, previous)
              previous = (entry[0], entry[1])
              print('[*] New generated entry: {}'.format(entry))
              if entry_cnt != 0:
                self.driver.find_element_by_id('add_row').click()
              el = self.driver.find_elements_by_id('time_sheet_entry_work_order_id')[entry_number]
              for option in el.find_elements_by_tag_name('option'):
                if option.text.strip().startswith(entry[0]):
                  option.click()
                  break
              self.driver.find_elements_by_id('time_sheet_entry_note')[entry_number].send_keys(entry[1])
              sleep(0.5)
              self.driver.find_elements_by_id('time_sheet_entry_start_time')[entry_number].send_keys(entry[2])
              sleep(0.5)
              self.driver.find_elements_by_id('time_sheet_entry_end_time')[entry_number].send_keys(entry[3])
              sleep(0.5)
              self.driver.find_elements_by_name('commit')[entry_number].click()
              entry_cnt += 1



    def quit(self):
      self.driver.quit()
      raise Exception('Driver quit!')

    def logout(self):
      print('[*] Logging out...')
      self.driver.get('https://secure.getjobber.com/logout')


if __name__ == '__main__':

    try:
        jf = JobberFIller(email, password, first_date, last_date, exceptional_dates, daily_deviation, exceptional_only)
        jf.login()
        # Don't ask
        sleep(5)
        jf.fill_things_up()
        jf.logout()
        jf.quit()
    except Exception as e:
        traceback.print_exc()
        try:
          jf.quit()
        except:
          pass
