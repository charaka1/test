# Copyright (c) The University of Edinburgh, 2014.
#
import tool
import json
import util
import requests

def geosmetaTool():
    """Obtain a Tool object to talk to the GeosMeta server

    :returns: a new Tool
    """
    geosmetaTool = tool.Tool()
    return geosmetaTool


def processGetResponse(response):
    """Utility method to process the requests response
    for get methods.

    :param response: requests response object
    :returns: JSON from response if response contains it
    :raises Exception: if problem processing response
                       or error received from server
    """

    code = requests.codes.ok
    try:
        return processResponse(response, code)
    except Exception as e:
        raise e

def processPostResponse(response):
    """Utility method to process the requests response
    for post methods.

    :param response: requests response object
    :returns: JSON from response if response contains it
    :raises Exception: if problem processing response
                       or error received from server
    """

    code = requests.codes.created
    try:
        return processResponse(response, code)
    except Exception as e:
        raise e

def processResponse(response, statusCode):
    """Utility method to process the requests response.

    :param response: requests response object
    :param statusCode: HTTP status code to check response against
    :returns: JSON from response if response contains it
    :raises Exception: if problem processing response
                       or error received from server
    """

    if response.status_code == statusCode:
        try:
            responseJSON = response.json()
            return responseJSON
        except ValueError as e:
            responseJSON = None
            return responseJSON
        except Exception as e:
            raise e
    else:
        try:
            # Gets status codes 4XX and 5XX only
            response.raise_for_status()
        except Exception as e1:
            raise e1
        else:
            message = "Status code: %s" %(response.status_code)
            try:
                responseJSON = response.json()
            except Exception as e2:
                responseJSON = None
            if responseJSON is not None:
                reason = json.dumps(responseJSON['_issues'])
                message += "\nReason: " + reason
            raise Exception(message)

def getAccounts():
    """Get account details from system.

    :returns: JSON response
    :raises Exception: if problem getting accounts
    """
    message = ''
    resource = 'accounts'
    try:
        response = geosmetaTool().performGet(resource, message)
    except Exception as e:
        raise e

    try:
        return processGetResponse(response)
    except Exception as e:
        raise e

def getAccount(username):
    """Get account details from system for a user.

    :param username: username to lookup
    :returns: JSON response
    :raises Exception: if problem getting accounts
    """
    message = ''
    resource = 'accounts/' + username
    try:
        response = geosmetaTool().performGet(resource, message)
    except Exception as e:
        raise e

    try:
        return processGetResponse(response)
    except Exception as e:
        raise e

def postAccount(accountJSON):
    """Post user account to database.

    :param accountJSON: JSON containing account details
    :returns: requests response object
    """
    response = geosmetaTool().performPost('accounts', accountJSON)
    return response

def createUser(firstname, lastname, username, email, secret, roles):
    """Create a user in the Geosmeta system

    :param firstname: Firstname of the user
    :param lastname: Lastname of the user
    :param username: Username of the user
    :param email: Email of the user
    :param secret: Secret key
    :param roles: List of roles
    :returns: id of user if creation successful
    :raises Exception: if problem creating user
    """
    account = {'firstname': firstname,
               'lastname': lastname,
               'username': username,
               'email': email,
               'secret': secret,
               'roles': roles
               }
    try:
        response = postAccount(json.dumps(account))
    except Exception as e:
        raise e

    try:
        return processPostResponse(response)
    except Exception as e:
        raise e

    response_json = response.json()
    if response_json['_status'] == "OK":
        id = response_json['_id']
        return id
    else:
        raise Exception("Status not OK")

def getProjectRoles(projectName):
    """Get the roles for a project.
    :param projectName: project to get roles from
    :returns: JSON response
    :raises Exception: if problem getting the document
    """

    message = ''
    resource = 'project_roles'
    #+ projectName
    params = {'where': '{"project": "' +  projectName + '"}' }
    try:
        response = geosmetaTool().performGet(resource, message, params)
    except Exception as e:
        raise e

    try:
        return processGetResponse(response)
    except Exception as e:
        raise e

def getActivity(projectName, activityName):
    """Get an activity document.
    :param projectName: project to get activity from
    :param activityName: activity to retrieve
    :returns: JSON response
    :raises Exception: if problem getting the document
    """

    message = ''
    resource = 'activities/' + activityName
    params = {'where': '{"project": "' +  projectName + '"}' }
    try:
        response = geosmetaTool().performGet(resource, message, params)
    except Exception as e:
        raise e

    try:
        return processGetResponse(response)
    except Exception as e:
        raise e

def getActivities(projectName):
    """Get all activity documents for a given project.
    :param projectName: project to get activities from
    :returns: JSON response
    :raises Exception: if problem getting the document
    """

    message = ''
    resource = 'activities'
    params = {'where': '{"project": "' + projectName + '"}'}
    try:
        response = geosmetaTool().performGet(resource, message, params)
    except Exception as e:
        raise e

    try:
        return processGetResponse(response)
    except Exception as e:
        raise e

def findActivities(projectName, query):
    """Find/search activity documents in the project that satisfies the query .
    :param projectName: project to get activities from
    :param query: query parameters
    :returns: JSON response
    :raises Exception: if problem getting the documents
    """

    message = ''
    resource = 'activities'

    params = {'where': '{"$and":[{"project": "' + projectName + '"},{' + query + '}]}'}
    #print(params)

    try:
        response = geosmetaTool().performGet(resource, message, params)
        #response = geosmetaTool().performGetNoParams(resource, message, searchString)
    except Exception as e:
        raise e

    try:
        return processGetResponse(response)
    except Exception as e:
        raise e

def getProjects(projectName=None, researchGroupName=None):
    """Get projects from the database.
    :param projectName: project to get details for (optional)
    :param researchGroupName: research group to get details for (optional)
    :returns: JSON response
    :raises Exception: if problem getting the project
    """

    message = ''
    resource = 'projects'
    if projectName is None:
        if researchGroupName is None:
            params = None
        else:
            params = {'where': '{"research_group": "' + researchGroupName +'"}'}
    else:
        if researchGroupName is None:
            params = {'where': '{"title": "' + projectName +'"}'}
        else:
            params = {'where': '{"research_group": "' + researchGroupName
                        + '", "title": "' + projectName + '"}'}

    try:
        response = geosmetaTool().performGet(resource, message, params)
    except Exception as e:
        raise e

    try:
        return processGetResponse(response)
    except Exception as e:
        raise e

def getResearchGroups(researchGroupName=None):
    """Get Research Groups from the database.
    :param researchGroupName: research group to get details for (optional)
    :returns: JSON response
    :raises Exception: if problem getting the project
    """

    message = ''
    resource = 'research_groups'
    if researchGroupName is None:
        params = None
    else:
        params = {'where': '{"title": "' + researchGroupName +'"}'}

    try:
        response = geosmetaTool().performGet(resource, message, params)
    except Exception as e:
        raise e

    try:
        return processGetResponse(response)
    except Exception as e:
        raise e

def postResearchGroup(researchGroupJSON):
    response = geosmetaTool().performPost('research_groups', researchGroupJSON)
    return response

def addResearchGroup(title, description, comment):
    """ Adds a new research group

    :param title: Unique (required) title of the research group
    :param description: Description of research group
    :param comment: Comment
    :return: id of the research group if created successfully
    """
    config = util.GeosMetaConfig()
    creator = config.username

    research_group = {'title': title,
                      'creator': creator}

    if description is not None:
        research_group['shortDescription'] = description

    if comment is not None:
        research_group['comment'] = comment

    try:
        response = postResearchGroup(json.dumps(research_group))
    except Exception as e:
        raise e

    try:
        return processPostResponse(response)
    except Exception as e2:
        raise e2

    response_json = response.json()
    if response_json['_status'] == "OK":
        id = response_json['_id']
        return id
    else:
        raise Exception("Status not OK")

def postProject(projectJSON):
    response = geosmetaTool().performPost('projects', projectJSON)
    return response

def postProjectRoles(projectRolesJSON):
    response = geosmetaTool().performPost('project_roles', projectRolesJSON)
    return response

def addProject(title, researchGroup, description, comment):
    """ Adds a new project

    :param title: Unique (required) title of the project
    :param researchGroup: Name of research group to add project to
    :param description: Description of project
    :param comment: Comment
    :return: id of the project if created successfully
    """
    config = util.GeosMetaConfig()
    creator = config.username

    project = {'title': title,
               'research_group': researchGroup,
               'creator': creator}

    if description is not None:
        project['shortDescription'] = description

    if comment is not None:
        project['comment'] = comment

    try:
        response = postProject(json.dumps(project))
    except Exception as e1:
        raise e1

    try:
        processPostResponse(response)
    except Exception as e2:
        raise e2

    project_roles = {'project': title,
                     'read_access': [],
                     'write_access': []}

    try:
        responseRoles = postProjectRoles(json.dumps(project_roles))
    except Exception as e3:
        raise e3

    try:
        processPostResponse(responseRoles)
    except Exception as e4:
        raise e4

    response_json = response.json()
    if response_json['_status'] == "OK":
        id = response_json['_id']
        return id
    else:
        raise Exception("Status not OK")

def postActivity(activityJSON):
    response = geosmetaTool().performPost('activities', activityJSON)
    return response

def patchActivity(resource, changesJSON, etag):
    response = geosmetaTool().performPatch(resource, changesJSON, etag)
    return response

def updateActivity(activityID, etag, field, value):
    """ Updates an activity field with a value provided.
    :param activityID: _id of the activity document to be changed
    :param etag: correct _etag of the current document
    :param field: field to be changed
    :param value: new value for the field
    :return: id of the activity if update successful
    """

    resource = 'activities/' + activityID
    changes = {field: value}
    changesJSON = json.dumps(changes)

    try:
        response = patchActivity(resource, changesJSON, etag)
        return response
        #response = patchWithPostOveride(resource, json.dumps(changes))
    except Exception as e:
        raise e

    #try:
    #    return processPostResponse(response)
    #except Exception as e:
    #    raise e

    #response_json = response.json()
    #if response_json['_status'] == "OK":
    #    id = response_json['_id']
    #    return id
    #else:
    #    raise Exception("Status not OK")

def addActivity(title, project, activitySource, status, jsonFile):
    """ Adds a new activity

    :param title: Unique (required) title of the activity
    :param project: Project the activity is associated with
    :param activitySource: Activity Source; e.g., experiment, fieldwork, etc.
    :param status: Status of the activity document; e.g., current, error, etc.
    :param jsonFile: A valid JSON file containing additional metadata
    :return: id of the activity document if created successfully
    """
    config = util.GeosMetaConfig()
    creator = config.username

    with open(jsonFile) as theFile:
        theContent = json.load(theFile)

    activity = {'title': title,
                'project': project,
                'creator': creator,
                'source': activitySource,
                'status': status,
                'metadata': json.dumps(theContent)}
    try:
        response = postActivity(json.dumps(activity))
    except Exception as e:
        raise e

    try:
        return processPostResponse(response)
    except Exception as e:
        raise e

    response_json = response.json()
    if response_json['_status'] == "OK":
        id = response_json['_id']
        return id
    else:
        raise Exception("Status not OK")
