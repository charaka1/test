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
    parser = argparse.ArgumentParser(description="Get project details from the GeosMeta system")
    parser.add_argument('--project',
                        '-p',
                        required=False,
                        help='Name of the project')
    parser.add_argument('--researchgroup',
                        '-r',
                        required=False,
                        help='Name of the research group to get projects for')
    args = parser.parse_args()

    projectName = args.project
    researchGroupName = args.researchgroup

    # Prompt user for confirmation
    if (researchGroupName):
        print "For Research Group %s" % (researchGroupName)
    if (projectName):
        question = "Get details of %s?"\
               % (projectName)
    else:
        question = "Get all projects?"

    response = util.queryYesNo(question)

    if (response):
        # Get user details
        print "Getting project details"
        try:
            resultJSON = api.getProjects(projectName=projectName,
                                         researchGroupName=researchGroupName)
        except Exception as err:
            sys.stderr.write('Error getting projects:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
        else:
            sys.stdout.write('Got project details:\n\n')
            sys.stdout.write(json.dumps(resultJSON,
                                        indent=2,
                                        sort_keys=True))

        if (projectName):
            print "\nGetting project roles"
            try:
                rolesJSON = api.getProjectRoles(projectName)
            except Exception as err:
                sys.stderr.write('\nError getting project roles:\n')
                sys.stderr.write('%s\n' % str(err))
                sys.exit(1)
            else:
                sys.stdout.write('\nGot project roles:\n\n')
                sys.stdout.write(json.dumps(rolesJSON,
                                            indent=2,
                                            sort_keys=True))

        sys.exit(0)
    else:
        sys.stdout.write('Not getting project details\n')
        sys.exit(0)
