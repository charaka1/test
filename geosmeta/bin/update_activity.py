#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import api
import argparse
import sys
import json

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Updates an Activity using the GeosMeta system")
    parser.add_argument('--activityname',
                        '-a',
                        required=True,
                        help='Activity name or the ID (required)')
    parser.add_argument('--projectName',
                        '-p',
                        required=True,
                        help='Name of project (required)')
    parser.add_argument('--field',
                        '-f',
                        required=True,
                        help='Name of the field - e.g., status (required)')
    parser.add_argument('--value',
                        '-v',
                        required=True,
                        help='Value for the field - e.g., OBSOLETE (required)')
    args = parser.parse_args()

    activityName = args.activityname
    projectName = args.projectName
    field = args.field
    value = args.value

    if (projectName and activityName):

        #first get the document and then extract the etag
        try:
            resultJSON = api.getActivity(projectName, activityName)
        except Exception as err:
            sys.stderr.write('Error retrieving the etag:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
        else:
            sys.stdout.write('Etag retrieved successfully: \n')
            activityID = resultJSON['_id']
            activityEtag = resultJSON['_etag']
            print 'Etag: ' + activityEtag
            print '_id:' + activityID


        # Now update the activity using its _id, _etag and the change to be made.
        try:
            result = api.updateActivity(activityID, activityEtag, field, value)
            print(result)
        except Exception as err:
            sys.stderr.write('Error updating the activity:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

        else:
            sys.stdout.write('Activity was updated successfully, Activity ID:' + str(result) + '\n')
            sys.exit(0)
    else:
        sys.stdout.write('Not updating the activity\n')
        sys.exit(0)

