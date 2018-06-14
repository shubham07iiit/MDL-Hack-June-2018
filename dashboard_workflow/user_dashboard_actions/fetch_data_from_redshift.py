import psycopg2, psycopg2.extras
import json
from .constants import *
import os
import shutil


class Event(object):

    name = None
    color = None
    time_stamp = None


class Transition(object):

    events = []
    user_id = None


class FetchDataFromRedhsift(object):

    events = {
        'web_date': [],
        'web_drives': ['option', 'Classification'],
        'web_visualization': ['Chart_type', 'Classification'],
        'web_search': ['param', 'auto_suggest'],
        'web_add': ['IsBusiness', 'IsStartNamedLocation', 'IsEndNamedLocation'],
        'web_reported_drives': ['IsShown'],
        'web_driveList_Select': ['Select_type', 'NumSelected', 'Search'],
        'web_sort': ['Option'],
        'web_edit': ['Edit_type'],
        'web_editPane_done': [],
        'web_delete': [],
        'web_report': ['expenseService'],
        'web_duplicate': [],
        'web_join': [],
        'web_reports_date': [],
        'web_reports_drives': ['Option'],
        'web_reports_vehicles': ['Selection'],
        'web_reports_create': ['Service', 'Source', 'Action', 'Product'],
        'web_reports_archived': ['Option', 'Action', 'Service', 'Product']
    }

    def __init__(self, payload):
        self.num_users = payload.get('num_users')
        self.start_date = payload.get('start_date')
        self.end_date = payload.get('end_date')
        self.user_id = payload.get('user_id')
        self.r_cur = ''

    def connect_to_redshift(self):
        r_conn = psycopg2.connect(database="mileiq", user="mileiq", password="aYTaRx7LdcCMRDf8", port=5439,
                                  host="miq-redshit-test.cuumkgtcwrly.us-east-1.redshift.amazonaws.com",
                                  connect_timeout=0)
        self.r_cur = r_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def store_user_sessions(self, user, curr_user_events):
        all_events = []
        i = 0
        for event in curr_user_events:
            if event[NAME] == 'web_login':
                if all_events:
                    transition = Transition
                    transition.events = all_events
                    transition.user_id = user
                    i += 1
                all_events = []
                continue

            new_event = Event
            new_event.name = event[NAME]
            new_event.color = 'GREEN'
            new_event.time_stamp = event[TIME]

            properties = event[PROPERTIES]
            properties = json.loads(properties)
            for property in self.events[event[NAME]]:
                if property in properties:
                    all_actions[str(action[TIME])] = action[NAME] + '-' + property + '-' + str(properties[property])
            else:
                all_actions[str(action[TIME])] = action[NAME]
                all_events.append(new_event)

        if all_events:
            transition = Transition()
            transition.events = all_events
            transition.user_id = user

    def query_redshift(self):
        query = None
        if self.num_users is not None:
            query = ("""SELECT mixpanel_user_id
                        FROM sec_user
                        WHERE is_premium = '1'
                        LIMIT {0};""".format(self.num_users))
        else:
            query = ("""SELECT mixpanel_user_id
                        FROM sec_user
                        WHERE upgraded = '1';""")

        result = self.r_cur.execute(query)
        all_users = self.r_cur.fetchall()
        self.num_users = len(all_users)
        active_users = 0
        for i in range(0, int(self.num_users)):
            user = all_users[i]['distinct_id']
            print(user)
            query = ("""SELECT * from  mp.event
                        WHERE distinct_id = '{0}' AND 
                        NAME LIKE 'web_%' AND NAME LIKE 'app_%'
                        AND TIME >= '{1}' AND TIME <= '{2}';""".format(user, self.start_date, self.end_date));
            result = self.r_cur.execute(query)
            curr_user_events= self.r_cur.fetchall()

            if curr_user_events:
                active_users += 1
                self.store_user_sessions(user, curr_user_events)
            print('Hello')
        print(active_users)






