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
    parser = argparse.ArgumentParser(description="Get activity details from the GeosMeta system")
    parser.add_argument('--activityname',
                        '-a',
                        required=False,
                        help='Name of the activity')
    parser.add_argument('--project',
                        '-p',
                        required=True,
                        help='Name of the project (required)')
    args = parser.parse_args()

    activityName = args.activityname
    projectName = args.project

    # Prompt user for confirmation
    if (activityName):
        question = "Get details of %s"\
               % (activityName)
    else:
        question = "Get all activities?"

    response = util.queryYesNo(question)

    if (response):
        # Get user details
            print "Getting activity details from project: %s" % (projectName)
            try:
                if (activityName):
                    resultJSON = api.getActivity(projectName, activityName)
                else:
                    resultJSON = api.getActivities(projectName)
            except Exception as err:
                sys.stderr.write('Error getting activities:\n')
                sys.stderr.write('%s\n' % str(err))
                sys.exit(1)
            else:
                sys.stdout.write('Got activity details:\n\n')
                sys.stdout.write(json.dumps(resultJSON,
                                            indent=2,
                                            sort_keys=True))
                sys.exit(0)
    else:
        sys.stdout.write('Not getting activity details\n')
        sys.exit(0)
