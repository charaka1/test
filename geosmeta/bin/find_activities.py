#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import api
from geosmeta import util
import argparse
import json
import sys

if __name__ == '__main__':
        # Get command line arguments
    parser = argparse.ArgumentParser(description="Get activity details from the GeosMeta system")
    parser.add_argument('--query',
                        '-q',
                        required=False,
                        help='key-value search query (required)')
    parser.add_argument('--projectName',
                        '-p',
                        required=True,
                        help='Name of the project (required)')
    args = parser.parse_args()
    query = args.query
    projectName = args.projectName

    response = util.queryYesNo("Submit query: %s" % (query))

    if (response):
        # Submit the query
        try:
            if (query and projectName):
                resultJSON = api.findActivities(projectName, query)
                print(json.dumps(resultJSON,
                                indent=2,
                                sort_keys=True))
                sys.exit(0)
            else:
                sys.stdout.write('No query and project provided.\n')
        except Exception as err:
            sys.stderr.write('Error submitting the query:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
        else:
            sys.stdout.write('Received activities:\n\n')
            sys.exit(0)

    else:
        sys.stdout.write('Not submitting the query\n')
        sys.exit(0)
