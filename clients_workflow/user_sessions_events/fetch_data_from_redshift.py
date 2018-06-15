import psycopg2, psycopg2.extras
import pyodbc
import json
from .constants import *
import os
import shutil
import csv
from datetime import datetime
import operator
import bisect


class Event(object):
    name = None
    color = None
    time_stamp = None


class Transition(object):
    events = []
    user_id = None


class FetchDataFromRedhsift(object):

    events = {
        'web_date': ['IsQuickFilter', 'Range'],
        'web_drives': ['option', 'Classification'],
        'web_visualization': ['Chart_type', 'Classification', 'Purpose'],
        'web_search': ['param', 'auto_suggest'],
        'web_search_select': ['auto_suggest', 'auto_complete'],
        'web_add': ['IsBusiness', 'IsStartNamedLocation', 'IsEndNamedLocation'],
        'web_location_suggested': ['isNamedLocation', 'isProfileSuggestion', 'isOtherLocation'],
        'web_location_clicked': ['isNamedLocation', 'isNamedLocation', 'isOtherLocation'],
        'web_reported_drives': ['IsShown'],
        'web_driveList_Select': ['Select_type', 'NumSelected', 'Search'],
        'web_sort': ['Option'],
        'web_classify': ['Classification', 'Purpose', 'Source', 'editMode', 'nDrives'],
        'web_edit': ['Edit_type', 'Bulk_confirmation', 'didClassify', 'nDrives', 'Classification', 'Purpose', 'Source', 'editMode', 'nDrives', 'NamedLoc'],
        'web_unsubscribe_view': [],
        'web_bulksessions_edit': ['Total', 'Yes', 'Cancel'],
        'web_editPane_done': [],
        'web_delete': ['NumDeleted'],
        'web_report': ['NumSelected', 'expenseService'],
        'web_duplicate': [],
        'web_join': ['NumSelected'],
        'web_undo': ['Page', 'Action'],
        'web_update_card_details': ['action'],
        'web_reports_date': ['IsQuickFilter', 'Range'],
        'web_reports_drives': ['Option'],
        'web_reports_vehicles': ['Selection'],
        'web_reports_view_drives': [],
        'web_reports_create': ['nDays', 'expenseService', 'Product'],
        'web_reports_created': ['Service', 'Source', 'Action', 'Product'],
        'web_xero_selected': ['Type'],
        'web_xero_reimbursement': ['Action'],
        'web_reports_archived': ['Option', 'Action', 'Service', 'Product', 'IsPreview'],
        'web_welcome_seen': [],
        'web_welcome_skipped': ['step', 'location'],
        'web_welcome_onDemand': [],
        'web_welcome_completed': []
    }

    session_transitions = []
    user_sessions_dict = {}

    def __init__(self, payload):
        self.num_users = payload.get('num_users')
        self.start_date = payload.get('start_date')
        self.end_date = payload.get('end_date')
        self.user_id = payload.get('user_id')
        self.r_cur = ''

    def connect_to_redshift(self):
        # r_conn = psycopg2.connect(database="mileiq", user="mileiq", password="aYTaRx7LdcCMRDf8", port=5439,
        #                           host="miq-redshit-test.cuumkgtcwrly.us-east-1.redshift.amazonaws.com",
        #                           connect_timeout=0)

        # server = 'mdlazureeastus.database.windows.net'
        # database = 'MileIQTest'
        # username = 'shusing@microsoft.com'
        # password = 'MsSeventh@123'
        # driver = '{ODBC Driver 13 for SQL Server}'
        r_conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:mdlazureeastus.database.windows.net,'
                                '1433;Database=MileIQTest;Uid=shusing@microsoft.com;Pwd=MsSeventh@123;'
                                'Encrypt=yes;''TrustServerCertificate=no;Connection Timeout=300;'
                                'Authentication=ActiveDirectoryPassword')


        self.r_cur = r_conn.cursor()

    def store_user_sessions(self, user, curr_user_events):
        all_events = []
        i = 0
        for event in curr_user_events:
            if event[NAME] == 'web_login' or event[NAME] == 'app_LogIn' or event[NAME] == 'app_LogIn' or event[NAME] == 'app_Launch':
                if all_events:
                    transition = Transition
                    transition.events = all_events
                    transition.user_id = user
                    self.session_transitions.append(transition)
                    i += 1
                all_events = []
                continue

            new_event = Event
            new_event.color = 'GREEN'
            new_event.time_stamp = event[TIME]

            properties = event[PROPERTIES]
            properties = json.loads(properties)

            if properties:
                for key, value in properties:
                    new_event.name = event[NAME] + '-' + str(key) + '-' + str(value)
            else:
                new_event.name = event[NAME]

            # if event[NAME] not in self.events or not self.events[event[NAME]]:
            #     new_event.name = event[NAME]
            # else:
            #     for property in self.events[event[NAME]]:
            #         if property in properties:
            #             new_event.name = event[NAME] + '-' + property + '-' + str(properties[property])
            #         else:
            #             new_event.name = event[NAME]
            all_events.append(new_event)
        if all_events:
            transition = Transition()
            transition.events = all_events
            transition.user_id = user
            self.session_transitions.append(transition)



    def query_database(self):
        filename = "events_data.csv"
        fields = []
        rows = []
        with open(r'D:\MDL_Codebase\MDLHack-June-2018\dashboard_workflow\clients_workflow\user_sessions_events\events_data.csv', 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
                datetime_object = datetime.strptime(row[1][:-8], '%Y-%m-%d %H:%M:%S')
                tuple = (datetime_object, row[2], row[3])
                if row[0] in self.user_sessions_dict:
                    # (self.user_sessions_dict[row[0]]).append(tuple)
                    bisect.insort(self.user_sessions_dict[row[0]], tuple)
                else:
                    tuple_list = []
                    tuple_list.append(tuple)
                    self.user_sessions_dict[row[0]] = tuple_list

            # for key in self.user_sessions_dict:
            #     self.user_sessions_dict[key] = (self.user_sessions_dict[key]).sort(key=lambda x: x[0])




        # query = None
        # if self.num_users is not None:
        #     query = ("""SELECT TOP {0} mixpanel_distinct_id
        #                 FROM sec_user
        #                 WHERE is_premium = '1';""".format(self.num_users))
        # else:
        #     query = ("""SELECT mixpanel_distinct_id
        #                 FROM sec_user
        #                 WHERE is_premium = '1';""")

        # result = self.r_cur.execute(query)
        # all_users = self.r_cur.fetchall()
        # self.num_users = len(all_users)
        # active_users = 0
        # for i in range(0, int(self.num_users)):
        #     user = all_users[i][0]
        #     print(user)
        #     query = ("""SELECT * from  mp.event
        #                 WHERE distinct_id = '{0}' AND
        #                 NAME LIKE 'web%' OR NAME LIKE 'app%'
        #                 AND TIME >= '{1}' AND TIME <= '{2}'
        #                 ORDER BY time ASC;""".format(user, self.start_date, self.end_date));
        #     result = self.r_cur.execute(query)
        #     curr_user_events= self.r_cur.fetchall()
        #
        #     if curr_user_events:
        #         active_users += 1
        #         self.store_user_sessions(user, curr_user_events)
        #     print('Hello')
        # print(active_users)






