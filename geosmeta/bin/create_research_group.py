#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
import argparse
from pymongo import MongoClient
import sys

#Note that this script speaks directly to MongoDB. Therefore, change the following line to the correct Mongo DB
#instance.
MONGO_DB_URI = 'mongodb://cha:g3osm3ta@localhost:27017/apitest'

def DB():
    mongoClient = MongoClient(MONGO_DB_URI)
    db = mongoClient.apitest
    return db

if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Add a user to the GeosMeta system")
    parser.add_argument('--title',
                        '-t',
                        required=True,
                        help='Name of the Research Group')
    parser.add_argument('--description',
                        '-d',
                        required=False,
                        help='A short description of the Research Group')
    parser.add_argument('--comment',
                        '-c',
                        required=False,
                        help='Additional comments')
    parser.add_argument('--username',
                        '-u',
                        required=True,
                        help='User name of the creator')
    args = parser.parse_args()

    title = args.title
    description = args.description
    comment = args.comment
    username = args.username

    #Only proceed if title and username is provided
    if(title and username):
        #Create a Research Group
        try:
            document = { 'title': title,
                         'shortDescription': description,
                         'comment': comment,
                         'creator': username}
            DB().research_groups.insert(document)
        except Exception as err:
            sys.stderr.write('Error creating Research Group\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
    else:
        sys.stdout.write('Not creating Research Group\n')
        sys.exit(0)