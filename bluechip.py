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

import datetime, subprocess, sys, os, glob, time
from datetime import timedelta
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.support.select import Select

# add a localsettings.py file and place your username and password in there
# USERNAME = 'username'
# PASSWORD = 'password'
#
# To use the -a -all you need to add a list of lists of usernames and passwords
# username_password = [ ['username1' , 'password1'] , ['username2' , 'password2'] ]


try:
    from localsettings import *
except ImportError:
    # go add these in a localsettings.py!
    USERNAME = ''
    PASSWORD = ''
    # username_password = [ ['username1' , 'password1'] , ['username2' , 'password2'] ]
    username_password = [['', ''],['', ''], ]
    pass


def nine_to_five(username, password, day_offset=0, overtime=0):

    # delete and old time sheets in the download folder
    map(os.unlink, glob.glob(os.path.expanduser('~/Downloads/EmployeeTime*.PDF')))

    # browser = webdriver.PhantomJS('./phantomjs')
    # browser = webdriver.Firefox()

    # currently chrome is the only one that we can download the file with
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    # go to bluechip login page
    browser.get('https://prodnetapp01.pimedia.com/lago/Default.aspx')
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_LogIn').click()

    #login here
    print 'logging in as {}...'.format(username)
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
    print 'inserted {} hours for {}'.format(out-8.5, day.strftime('%A %B %d'))

    # we want to now print the sheet
    # press the print button
    browser.find_element_by_id('ctl00_ContentPlaceHolder1_bPrint').click()
    # need to wait a second for it to download
    time.sleep(2)

    # grab the time sheet file
    file = glob.glob(os.path.expanduser('~/Downloads/EmployeeTime*.PDF'))
    subprocess.call(['lpr', '-#1', '-l', '-r', '{}'.format(file[0])])
    print '{}\'s time sheet printed.'.format(username)
    browser.quit()


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
    parser.add_option(
        '-a', '--all',
        action='store_true',
        dest='punch_all',
        default=False,
        help='will punch in all users.'
    )

    options, args = parser.parse_args(args=sys.argv)

    if options.punch_all:
        for user, pw in username_password:
            nine_to_five(user, pw, day_offset=options.day_offset, overtime=options.overtime)
    else:
        nine_to_five(USERNAME, PASSWORD, day_offset=options.day_offset, overtime=options.overtime)


if __name__ == '__main__':
    run()
