Punch Card
=========

Automated bluechip transaction inserting.

IMPORTANT:
This code makes the assumption you are always 'clocked in'

uses selenium and phantomjs.

Install selenium:

    > pip install selenium==2.37.2


You will need to modify `bluechip.py` by adding your username and password.

To run:

    > python bluechip.py

You can also pass days or overtime.

days -days<number of days to go back from today>
overtime -overtime<number of hours above or below the regular 7/day>

Examples:

    > python bluechip.py

This will log 7.5 hours for today.

    > python bluechip.py -d1 -o1

This will log 8.5 hours in bluechip for yesterday.
