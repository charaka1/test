# Copyright (c) The University of Edinburgh, 2014.
#
import unittest
from geosmeta import tool
import json
from datetime import datetime
from pymongo import MongoClient
import uuid

EVE_ENTRY_POINT = 'http://localhost:5000'
MONGO_DB_URI = 'mongodb://cha:g3osm3ta@localhost:27017/apitest'
ADMIN_USERNAME = 'adminuser'
ADMIN_SECRET = 'letmein'
USER_USERNAME = 'user'
USER_SECRET = 'secret'
READUSER_USERNAME = 'readuser'
READUSER_SECRET = 'readsecret'
WRITEUSER_USERNAME = 'writeuser'
WRITEUSER_SECRET = 'writesecret'

def DB():
    mongoClient = MongoClient(MONGO_DB_URI)
    db = mongoClient.apitest
    return db

def deleteAccountsInDB():
    DB().accounts.drop()

def deleteGeosmetaCollectionInDB():
    DB().geosmetatest.drop()

def deleteResearchGroupCollectionInDB():
    DB().research_groups.drop()

def deleteProjectCollectionInDB():
    DB().projects.drop()

def deleteProjectRolesCollectionInDB():
    DB().project_roles.drop()

def deleteActivityCollectionInDB():
    DB().activities.drop()

def account():
    account = {'firstname': 'New',
               'lastname': 'User',
               'username': 'newuser',
               'email': 'newuser@example.com',
               'secret': 'letmein',
               'roles': ['user']}
    return account

def projectAccessDocument():
    document = {'project': 'Project Name #4',
                'read_access': [USER_USERNAME]}
    return document

def document(ownerID):
    now = datetime.utcnow().replace(microsecond=0).strftime('%a, %d %b %Y %H:%M:%S GMT')
    num = uuid.uuid4()
    document = {'name': 'Test Experiment Name %s' %num,
                'description': 'Test Description',
                'date': now,
                'owner': ownerID}
    return document

def researchGroup():
    num = uuid.uuid4()
    document = {'title': 'Test Research Group %s' %num,
                'shortDescription': 'Test description',
                'comment': 'Test comment',
                'creator': USER_USERNAME}
    return document

def project():
    num = uuid.uuid4()
    document = {'title': 'Test Project %s' %num,
                'shortDescription': 'Test description',
                'comment': 'Test comment',
                'creator': USER_USERNAME,
                'research_group': 'Research Group Name #1'}
    return document

def activity():
    num = uuid.uuid4()
    document = {'title': 'Test Activity %s' %num,
                'shortDescription': 'Test description',
                'comment': 'Test comment',
                'creator': USER_USERNAME,
                'project': 'Project Name #1'}
    return document

def createAdminUser():
    admin_account = {'firstname': 'User',
                     'lastname': 'Admin',
                     'username': ADMIN_USERNAME,
                     'email': 'admin@example.com',
                     'secret': ADMIN_SECRET,
                     'roles': ['admin', 'user']}
    accountID = DB().accounts.insert(admin_account)
    return accountID

def createUser():
    account = {'firstname': 'User',
               'lastname': 'Test',
               'username': USER_USERNAME,
               'email': 'user@example.com',
               'secret': USER_SECRET,
               'roles': ['user']}
    accountID = DB().accounts.insert(account)
    return accountID

def createReadUser():
    account = {'firstname': 'Readuser',
               'lastname': 'Test',
               'username': READUSER_USERNAME,
               'email': 'readuser@example.com',
               'secret': READUSER_SECRET,
               'roles': ['user']}
    accountID = DB().accounts.insert(account)
    return accountID

def createWriteUser():
    account = {'firstname': 'Writeiser',
               'lastname': 'Test',
               'username': WRITEUSER_USERNAME,
               'email': 'writeuser@example.com',
               'secret': WRITEUSER_SECRET,
               'roles': ['user']}
    accountID = DB().accounts.insert(account)
    return accountID

def createGeosmetaCollectionInDB(ownerID):
    for i in range(5):
        now = datetime.utcnow().replace(microsecond=0).strftime('%a, %d %b %Y %H:%M:%S GMT')
        document = {'name': 'Experiment Name #%d' %i,
                    'description': 'Description #%d' %i,
                    'date': now,
                    'owner': ownerID}
        DB().geosmetatest.insert(document)

def createResearchGroupCollectionInDB():
    for i in range(5):
        document = {'title': 'Research Group Name #%d' %i,
                    'shortDescription': 'Description #%d' %i,
                    'comment': 'Comment #%d' %i,
                    'creator': USER_USERNAME}
        DB().research_groups.insert(document)

def createProjectCollectionInDB():
    for i in range(5):
        document = {'title': 'Project Name #%d' %i,
                    'shortDescription': 'Description #%d' %i,
                    'comment': 'Comment #%d' %i,
                    'creator': USER_USERNAME,
                    'research_group': 'Research Group Name #%d' %i}
        DB().projects.insert(document)

def createProjectRolesCollectionInDB():
    for i in range(2):
        document = {'project': 'Project Name #%d' %i,
                    'read_access': [USER_USERNAME, READUSER_USERNAME],
                    'write_access': [USER_USERNAME, WRITEUSER_USERNAME]}
        DB().project_roles.insert(document)

def createActivityCollectionInDB():
    for i in range(5):
        document = {'title': 'Activity Name #%d' %i,
                    'shortDescription': 'Description #%d' %i,
                    'comment': 'Comment #%d' %i,
                    'creator': USER_USERNAME,
                    'project': 'Project Name #%d' %i}
        DB().activities.insert(document)

class TestTool(unittest.TestCase):

    def setUp(self):
        self.adminTool = tool.Tool('geosmeta-admin.cfg')
        self.tool = tool.Tool('geosmeta-normal.cfg')
        self.readTool = tool.Tool('geosmeta-readuser.cfg')
        self.writeTool = tool.Tool('geosmeta-writeuser.cfg')
        self.unauthTool = tool.Tool('geosmeta-unauth.cfg')
        deleteAccountsInDB()
        deleteGeosmetaCollectionInDB()
        deleteResearchGroupCollectionInDB()
        deleteProjectCollectionInDB()
        deleteProjectRolesCollectionInDB()
        deleteActivityCollectionInDB()
        self.adminID = createAdminUser()
        self.userID = createUser()
        self.readUserID = createReadUser()
        self.writeUserID = createWriteUser()
        createGeosmetaCollectionInDB(self.adminID)
        createResearchGroupCollectionInDB()
        createProjectCollectionInDB()
        createProjectRolesCollectionInDB()
        createActivityCollectionInDB()

    def testPerformGetAccountsAsAdmin(self):
        # Should work OK as admin user
        message = ''
        resource = 'accounts'
        response = self.adminTool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetAccountsAsUser(self):
        # Should fail as normal user
        message = ''
        resource = 'accounts'
        response = self.tool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetAccountsAsUnauthUser(self):
        # Should fail as unauthenticated user
        message = ''
        resource = 'accounts'
        response = self.unauthTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetProjectRolesAsAdmin(self):
        # Should work OK as admin user
        message = ''
        resource = 'project_roles'
        response = self.adminTool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetProjectRolesAsUser(self):
        # Should fail as normal user
        message = ''
        resource = 'project_roles'
        response = self.tool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetProjectRolesAsUnauthUser(self):
        # Should fail as unauthenticated user
        message = ''
        resource = 'project_roles'
        response = self.unauthTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetDocumentsAsAdmin(self):
        message = ''
        resource = 'geosmetatest'
        response = self.adminTool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetDocumentsAsUser(self):
        message = ''
        resource = 'geosmetatest'
        response = self.tool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetDocumentsAsUnauthUser(self):
        message = ''
        resource = 'geosmetatest'
        response = self.unauthTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetResearchGroupsAsAdmin(self):
        message = ''
        resource = 'research_groups'
        response = self.adminTool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetResearchGroupsAsUser(self):
        message = ''
        resource = 'research_groups'
        response = self.tool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetResearchGroupsAsUnauthUser(self):
        message = ''
        resource = 'research_groups'
        response = self.unauthTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetProjectsAsAdmin(self):
        message = ''
        resource = 'projects'
        response = self.adminTool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetProjectsAsUser(self):
        message = ''
        resource = 'projects'
        response = self.tool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetProjectsAsUnauthUser(self):
        message = ''
        resource = 'projects'
        response = self.unauthTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    # Getting all activities is unauthorised - must specify
    # project
    def testPerformGetAllActivitiesAsAdmin(self):
        message = ''
        resource = 'activities'
        response = self.adminTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetAllActivitiesAsUser(self):
        message = ''
        resource = 'activities'
        response = self.tool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetAllActivitiesAsReadUser(self):
        message = ''
        resource = 'activities'
        response = self.readTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetAllActivitiesAsWriteUser(self):
        message = ''
        resource = 'activities'
        response = self.writeTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetAllActivitiesAsUnauthUser(self):
        message = ''
        resource = 'activities'
        response = self.unauthTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetActivitiesForProjectAsAdmin(self):
        message = ''
        resource = 'activities'
        params = {'where': '{"project": "Project Name #1"}'}
        response = self.adminTool.performGet(resource, message, params)
        # Admin does not have read access to project
        self.assertEqual(response.status_code, 401)

    def testPerformGetActivitiesForProjectAsUser(self):
        message = ''
        resource = 'activities'
        params = {'where': '{"project": "Project Name #1"}'}
        response = self.tool.performGet(resource, message, params)
        self.assertEqual(response.status_code, 200)

    def testPerformGetActivitiesForProjectAsReadUser(self):
        message = ''
        resource = 'activities'
        params = {'where': '{"project": "Project Name #1"}'}
        response = self.readTool.performGet(resource, message, params)
        self.assertEqual(response.status_code, 200)

    def testPerformGetActivitiesForProjectAsWriteUser(self):
        message = ''
        resource = 'activities'
        params = {'where': '{"project": "Project Name #1"}'}
        response = self.writeTool.performGet(resource, message, params)
        self.assertEqual(response.status_code, 401)

    def testPerformGetActivitiesForProjectAsUnauthUser(self):
        message = ''
        resource = 'activities'
        params = {'where': '{"project": "Project Name #1"}'}
        response = self.unauthTool.performGet(resource, message, params)
        self.assertEqual(response.status_code, 401)

    def testPerformGetEventsAsAdmin(self):
        message = ''
        resource = 'events'
        response = self.adminTool.performGet(resource, message)
        self.assertEqual(response.status_code, 200)

    def testPerformGetEventsAsUser(self):
        message = ''
        resource = 'events'
        response = self.tool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformGetEventsAsUnauthUser(self):
        message = ''
        resource = 'events'
        response = self.unauthTool.performGet(resource, message)
        self.assertEqual(response.status_code, 401)

    def testPerformPostAccountAsAdmin(self):
        response = self.adminTool.performPost('accounts', json.dumps(account()))
        self.assertEqual(response.status_code, 201)

    def testPerformPostAccountAsUser(self):
        response = self.tool.performPost('accounts', json.dumps(account()))
        self.assertEqual(response.status_code, 401)

    def testPerformPostAccountAsUnauthUser(self):
        response = self.unauthTool.performPost('accounts', json.dumps(account()))
        self.assertEqual(response.status_code, 401)

    def testPerformPostProjectRolesAsAdmin(self):
        response = self.adminTool.performPost('project_roles', json.dumps(projectAccessDocument()))
        self.assertEqual(response.status_code, 201)

    def testPerformPostProjectRolesAsUser(self):
        response = self.tool.performPost('project_roles', json.dumps(projectAccessDocument()))
        self.assertEqual(response.status_code, 401)

    def testPerformPostProjectRolesAsUnauthUser(self):
        response = self.unauthTool.performPost('project_roles', json.dumps(projectAccessDocument()))
        self.assertEqual(response.status_code, 401)

    def testPerformPostDocumentAsAdmin(self):
        ownerID = str(self.adminID)
        response = self.adminTool.performPost('geosmetatest', json.dumps(document(ownerID)))
        self.assertEqual(response.status_code, 201)

    def testPerformPostDocumentAsUser(self):
        ownerID = str(self.adminID)
        response = self.tool.performPost('geosmetatest', json.dumps(document(ownerID)))
        self.assertEqual(response.status_code, 201)

    def testPerformPostDocumentAsUnauthUser(self):
        ownerID = str(self.adminID)
        response = self.unauthTool.performPost('geosmetatest', json.dumps(document(ownerID)))
        self.assertEqual(response.status_code, 401)

    def testPerformPostResearchGroupAsAdmin(self):
        response = self.adminTool.performPost('research_groups', json.dumps(researchGroup()))
        self.assertEqual(response.status_code, 201)

    def testPerformPostResearchGroupAsUser(self):
        response = self.tool.performPost('research_groups', json.dumps(researchGroup()))
        self.assertEqual(response.status_code, 201)

    def testPerformPostResearchGroupAsUnauthUser(self):
        response = self.unauthTool.performPost('research_groups', json.dumps(researchGroup()))
        self.assertEqual(response.status_code, 401)

    def testPerformPostProjectAsAdmin(self):
        response = self.adminTool.performPost('projects', json.dumps(project()))
        self.assertEqual(response.status_code, 201)

    def testPerformPostProjectAsUser(self):
        response = self.tool.performPost('projects', json.dumps(project()))
        self.assertEqual(response.status_code, 201)

    def testPerformPostProjectAsUnauthUser(self):
        response = self.unauthTool.performPost('projects', json.dumps(project()))
        self.assertEqual(response.status_code, 401)

    def testPerformPostActivityAsAdmin(self):
        response = self.adminTool.performPost('activities', json.dumps(activity()))
        self.assertEqual(response.status_code, 401)

    def testPerformPostActivityAsUser(self):
        response = self.tool.performPost('activities', json.dumps(activity()))
        self.assertEqual(response.status_code, 201)

    def testPerformPostActivityAsReadUser(self):
        response = self.readTool.performPost('activities', json.dumps(activity()))
        self.assertEqual(response.status_code, 401)

    def testPerformPostActivityAsWriteUser(self):
        response = self.writeTool.performPost('activities', json.dumps(activity()))
        self.assertEqual(response.status_code, 201)

    def testPerformPostActivityAsUnauthUser(self):
        response = self.unauthTool.performPost('activities', json.dumps(activity()))
        self.assertEqual(response.status_code, 401)
