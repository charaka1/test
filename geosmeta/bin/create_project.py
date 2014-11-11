#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
import argparse
from geosmeta import api
import sys

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Add a project to the GeosMeta system")
    parser.add_argument('--title',
                        '-t',
                        required=True,
                        help='Name of the Project')
    parser.add_argument('--description',
                        '-d',
                        required=False,
                        help='A short description of the Project')
    parser.add_argument('--comment',
                        '-c',
                        required=False,
                        help='Additional comments')
    parser.add_argument('--researchgroup',
                        '-r',
                        required=True,
                        help='Research Group this project belongs to')
    args = parser.parse_args()

    title = args.title
    description = args.description
    comment = args.comment
    researchGroup = args.researchgroup

    # Only proceed if title, username and research group is provided
    if (title and researchGroup):
        # Create a Research Group
        try:
            result = api.addProject(title, researchGroup, description, comment)
        except Exception as err:
            sys.stderr.write('Error creating Project\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
        else:
            sys.stdout.write('Project was created successfully, Project ID:' + str(result) + '\n')
            sys.exit(0)
    else:
        sys.stdout.write('Not creating Project\n')
        sys.exit(0)