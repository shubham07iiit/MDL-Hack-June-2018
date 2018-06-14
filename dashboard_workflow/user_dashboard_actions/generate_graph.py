import matplotlib.pyplot as plt
import plotly.plotly as py
from .constants import *
import os
import shutil
from collections import defaultdict

class Graphgenerator(object):

    def __init__(self, data):
        self.x = data[0]
        self.y = data[1]

    def plot_and_save_graph(self, user, session):
        plt.rcParams.update({'font.size': 5})
        plt.plot(self.x, self.y, linestyle='--', marker='o', color='b')
        plt.xticks(rotation=90)
        plt.yticks(rotation=5)
        plt.ylabel('time')
        plt.xlabel('user_actions')
        plt.title(user+'-'+session)
        # plt.show()
        # plt.figure(figsize=(10, 10))
        if not os.path.exists(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user):
            os.makedirs(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user)
        plt.savefig(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user + '/'+ session + '.png', dpi = 300)
        plt.close()

    def generate_aggregated_plot(self, user, session, aggregated_x, aggregated_y, file_num):
        if file_num == 0:
            plt.close()
            if not os.path.exists(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user):
                os.makedirs(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user)
            plt.savefig(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user + '/aggregated.png', dpi=300)
        plt.rcParams.update({'font.size': 5})
        plt.plot(aggregated_x, aggregated_y, linestyle='--', marker='o', color='b')
        plt.xticks(rotation=90)
        plt.yticks(rotation=5)
        plt.ylabel('time')
        plt.xlabel('user_actions')
        plt.title(user + '-' + session)
        # plt.show()
        # plt.figure(figsize=(10, 10))


    def plot_and_save_bar_graph(self, user, user_event_count):
        plt.bar(list(user_event_count.keys()), list(user_event_count.values()))
        plt.rcParams.update({'font.size': 5})
        plt.xticks(rotation=90)
        plt.yticks(rotation=5)
        plt.ylabel('Count')
        plt.xlabel('user_actions')
        plt.title(user)
        # plt.show()
        if not os.path.exists(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user):
            os.makedirs(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user)
        plt.savefig(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY + '/' + user + '/' + 'bar_graph.png', dpi = 300)
        plt.close()

    def fetch_data_from_workflow(self):
        if os.path.exists(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY):
            shutil.rmtree(DASHBOARD_WORKFLOW_GRAPH_DIRECTORY)
        all_folders = os.listdir(DASHBOARD_WORKFLOW_DIRECTORY)

        for folder in all_folders:
            all_files = os.listdir(DASHBOARD_WORKFLOW_DIRECTORY + '/' + folder)
            user_actions_count = defaultdict(int)
            file_num = 0
            for file in all_files:

                num = 0
                aggregated_x = []
                aggregated_y = []
                with open(DASHBOARD_WORKFLOW_DIRECTORY + '/' + folder + '/' + file) as f:
                    X = []
                    Y = []
                    for line in f:
                        x,y = line.split('    ')
                        X.append(x)
                        y = y[:-1]
                        Y.append(y)
                        aggregated_x.append(num)
                        aggregated_y.append(y)
                        user_actions_count[y] = user_actions_count[y] + 1
                        num += 1

                self.x = X
                self.y = Y
                self.plot_and_save_graph(user = folder, session = file)
                self.generate_aggregated_plot(folder, file, aggregated_x=aggregated_x, aggregated_y=aggregated_y, file_num = file_num)
                file_num += 1
            self.plot_and_save_bar_graph(user = folder, user_event_count = user_actions_count)


