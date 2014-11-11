#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import api
from geosmeta import util
import argparse
import sys
import json

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Get user details from the GeosMeta system")
    parser.add_argument('--username',
                        '-u',
                        required=False,
                        help='EASE username of the user (optional)')
    args = parser.parse_args()

    username = args.username

    # Prompt user for confirmation
    if (username):
        question = "Get user account for %s"\
               % (username)
    else:
        question = "Get all user accounts?"

    response = util.queryYesNo(question)

    if (response):
        # Get user details
            print "Getting user details"
            try:
                if (username):
                    resultJSON = api.getAccount(username)
                else:
                    resultJSON = api.getAccounts()
            except Exception as err:
                sys.stderr.write('Error getting users:\n')
                sys.stderr.write('%s\n' % str(err))
                sys.exit(1)
            else:
                sys.stdout.write('Got user details:\n\n')
                sys.stdout.write(json.dumps(resultJSON,
                                            indent=2,
                                            sort_keys=True))
                sys.exit(0)
    else:
        sys.stdout.write('Not getting user details\n')
        sys.exit(0)
