Punch Card
=========

Automated bluechip transaction inserting.

IMPORTANT:
This code makes the assumption you are always 'clocked in'

Uses selenium, chromedriver and phantomjs.

Install selenium:

    > pip install selenium==2.37.2
    > brew install chromedriver

You will need to modify `bluechip.py` by adding your username and password.

Add a `localsettings.py` file and place your username and password in there

    USERNAME = 'username'
    PASSWORD = 'password'

To use the `-a` `-all` you need to add a list of lists of <usernames> and <passwords>

    username_password = [ ['username1' , 'password1'] , ['username2' , 'password2'] ]

To run:

    > python bluechip.py

You can also pass days or overtime.

days -days<number of days to go back from today>
overtime -overtime<number of hours above or below the regular 7/day>

Examples:

    > python bluechip.py

This will log 7.5 hours for today and print your timesheet.


    > python bluechip.py -d1 -o1

This will log 8.5 hours in bluechip for yesterday and print today's timesheet.


    > python bluechip.py -a

This will log 7.5 hours for all the users in `username_password` and print their time sheets.
