"""
uses selenium and phantomjs (phantomjs bin is in the project folder)

    pip install -U selenium


You will need to modify this file by adding your username and password for bluechip

To run:

    >>python bluechip.py

You can pass days -days<number of days to go back from today> or overtime -overtime<number of hours above or below the regular 7/day>

Examples:

    >>python bluechip.py -d1 -o1

This will log 8 hours in bluechip for yesterday.

"""

import datetime
from datetime import timedelta
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.support.select import Select
import sys

USERNAME = ''
PASSWORD = ''

def nine_to_five(username, password, day_offset=0, overtime=0):

    browser = webdriver.PhantomJS('./phantomjs')
    browser.get('https://prodnetapp01.pimedia.com/lago/Default.aspx')

    browser.find_element_by_id('ctl00_ContentPlaceHolder1_LogIn').click()

    #login here
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_tName').send_keys(username)
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_tPassword').send_keys(password)
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_bSubmit').click()
    print 'logged in...'

    browser.find_element_by_id('ctl00_ContentPlaceHolder1_UserTrans_FormView1_tJob').send_keys('59950')
    select = browser.find_element_by_id('ctl00_ContentPlaceHolder1_UserTrans_FormView1_ddTask')
    Select(select).select_by_value('2777')

    day = datetime.date.today() - timedelta(days=int(day_offset))
    start = '{} {}'.format(day.strftime('%x'), '09:00')
    # overtime only added in hour blocks
    out = 16 + int(overtime)
    stop = '{} {}'.format(day.strftime('%x'), '{}:30'.format(out))

    # enter start date/time
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_UserTrans_FormView1_pStart').clear()
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_UserTrans_FormView1_pStart').send_keys(start)
    # enter stop date/time
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_UserTrans_FormView1_pStop').clear()
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_UserTrans_FormView1_pStop').send_keys(stop)
    # insert
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_UserTrans_FormView1_bAddTrans').click()
    print 'inserted time block...'
    # done
    browser.quit()
    print 'Done.'

def run():
    parser = OptionParser(usage="Usage: python %prog --days=<days to go back> --overtime=<hours above or below the regualar 7>")
    parser.add_option(
        '-d', '--days',
        action='store',
        default= 0,
        type='int',
        dest='day_offset',
        help='If you forgot to clock yesterday pass 1, two days ago pass 2 etc.'
    )
    parser.add_option(
        '-o', '--overtime',
        action='store',
        default= 0,
        type='int',
        dest='overtime',
        help='add overtime in hour blocks pass 1, or subtract time in hour blocks pass -1',
    )
    options, args = parser.parse_args(args=sys.argv)
    nine_to_five(USERNAME, PASSWORD, day_offset=options.day_offset, overtime=options.overtime)

if __name__ == '__main__':
    run()
