#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import api
from geosmeta import util
import argparse
import sys
import uuid

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Add a user to the GeosMeta system")
    parser.add_argument('--firstname',
                        '-f',
                        required=True,
                        help='Firstname of the user')
    parser.add_argument('--lastname',
                        '-l',
                        required=True,
                        help='Surname of the user')
    parser.add_argument('--username',
                        '-u',
                        required=True,
                        help='EASE username of the user')
    parser.add_argument('--email',
                        '-e',
                        required=True,
                        help='Email of the user')
    # TODO: This should read choices from elsewhere?
    parser.add_argument('--roles',
                        '-r',
                        required=True,
                        help='Space separated list of roles',
                        nargs='+',
                        choices=['user', 'admin'])
    args = parser.parse_args()

    firstname = args.firstname
    lastname= args.lastname
    username = args.username
    email = args.email
    roles = args.roles

    # Prompt user for confirmation
    question = "Creating user account for %s %s\n"\
               "With username %s and email %s\n"\
               "and roles %s"\
               % (firstname, lastname, username, email, roles)

    response = util.queryYesNo(question)

    if (response):
        # Generate a random secret key
        secret = str(uuid.uuid4())
        # Create a user
        try:
            result = api.createUser(firstname,
                                    lastname,
                                    username,
                                    email,
                                    secret,
                                    roles)
        except Exception as err:
            sys.stderr.write('Error creating user:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

        else:
            sys.stdout.write('Created user OK with secret:\n%s\n' % secret)
            sys.stdout.write('Please ask the user to store this secret in their config file\n')
            sys.exit(0)
    else:
        sys.stdout.write('Not creating user\n')
        sys.exit(0)
