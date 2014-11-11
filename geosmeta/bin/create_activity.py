#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import api
import argparse
import sys

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Uploads an Activity using the GeosMeta system")
    parser.add_argument('--activityname',
                        '-a',
                        required=True,
                        help='Name of the activity (required)')
    parser.add_argument('--project',
                        '-p',
                        required=True,
                        help='Name of the project (required)')
    parser.add_argument('--docSource',
                        '-d',
                        required=False,
                        help='Source of the activity - e.g., "fieldwork"')
    parser.add_argument('--status',
                        '-s',
                        required=False,
                        help='Status of the activity - e.g., "current"')
    parser.add_argument('--jsonFile',
                        '-j',
                        required=False,
                        help='json file containing additional data')
    args = parser.parse_args()

    activityname = args.activityname
    project = args.project
    docSource = args.docSource
    status = args.status
    jsonFile = args.jsonFile

    if (activityname and project):
        # Create an activity
        try:
            result = api.addActivity(activityname, project, docSource, status, jsonFile)
        except Exception as err:
            sys.stderr.write('Error creating activity:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

        else:
            sys.stdout.write('Activity was created successfully, Activity ID:' + str(result) + '\n')
            sys.exit(0)
    else:
        sys.stdout.write('Not creating activity\n')
        sys.exit(0)
