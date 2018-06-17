from __future__ import print_function
YELLOW_EVENTS = {"app_loggedIn",
                 "app_bgtask_started",
                 "app_Launch",
                 "web_login",
                 "app_LogIn"}

class Test:
    def __init__(self, key):
        self.key = key
        self.scoredSequenceList = []


class EventColor:
    Yellow = "Yellow"
    Green = "Green"


class Event:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return self.name + self.color


class WebTransaction:
    def __init__(self, events_arr, identifier):
        self.events_arr = events_arr
        self.id = identifier

    def __repr__(self):
        event_str = ""
        for event in self.events_arr:
            event_str += event.__repr__() + " "

        return event_str + str(self.id)


# class ScoredSequence:
#     def __init__(self, events_arr, score):
#         self.events_arr= events_arr
#         self.score= score
#
#     def ___repr__(self):
#         event_str = ""
#         for event in self.events_arr:
#             event_str += event.__repr__() + " "
#         return event_str + self.score

APP_START_EVENT = "app_Launch"
WEB_START_EVENT = "web_login"


def process(trans_list):
    scoredSequenceDict = {}
    listSequenceDict = {}
    # // validation : transaction start should be yellow
    for trans in trans_list:

        sequence_list = []
        sequence_str = ""
        if trans.events_arr[0].name.startswith("app_"):
            sequence_list.append(Event(APP_START_EVENT, EventColor.Yellow))
            sequence_str = APP_START_EVENT
        elif trans.events_arr[0].name.startswith("web_"):
            sequence_list.append(Event(WEB_START_EVENT, EventColor.Yellow))
            sequence_str = APP_START_EVENT
        else:
            print("Wrong transaction ")
            return []

        for event in trans.events_arr:
            if event.color == EventColor.Yellow:
                sequence_str = event.name
                sequence_list = []
                sequence_list.append(event)

            else:
                sequence_list.append(event)
                sequence_str += event.name
                if sequence_str not in scoredSequenceDict:
                    scoredSequenceDict[sequence_str] = 0
                    listSequenceDict[sequence_str] = list(sequence_list)
                scoredSequenceDict[sequence_str] = scoredSequenceDict[sequence_str] + 1

        # print trans.__repr__()
        # for event in trans.events_arr:

    return scoredSequenceDict, listSequenceDict


def sortKey(eventList):
    for a in eventList:
        print(a)
    print(eventList)
    # sortedStr = eventList[0].name
    # xyz = sorted(eventList[1:])
    # for x in xyz:
    #     sortedStr += " " + x.name
    # return sortedStr


def mergeProcessedSeq(sortedScoredSequenceDict, listSequenceDict):
    try:
        dict = {}
        mergedList = []  # list of key, scoredsequnce list
        idx = 0



        for key, value in sortedScoredSequenceDict:
            sortedStr = sortKey(listSequenceDict(key))

            if sortedStr not in dict:
                dict[sortedStr] = idx
                mergedList.append(Test(sortedStr))
                idx += 1

            mergedList[dict[sortedStr]].scoredSequenceList.append(listSequenceDict(key))
            mergedList[dict[sortedStr]].scoredSequenceList.append(value)

        return mergedList

    except Exception as excp:
        import traceback
        print(traceback.print_exc())

    return mergedList





def getEventColor(eventName):
    if eventName in YELLOW_EVENTS:
        return EventColor.Yellow
    else:
        return EventColor.Green


def getTransList():
    # S = Event("app_Launch", EventColor.Yellow)
    A = Event("app_A", EventColor.Green)
    C = Event("app_C", EventColor.Green)

    B = Event("app_B", EventColor.Green)

    X = Event("app_LogIn", EventColor.Yellow)
    Y = Event("app_Y", EventColor.Green)

    t1 = WebTransaction([A, C, X, Y], 1)
    t2 = WebTransaction([A, C], 1)
    t3 = WebTransaction([X, Y], 1)

    t4 = WebTransaction([B, A], 1)
    t5 = WebTransaction([B, A], 1)
    t6 = WebTransaction([B, A], 1)

    t7 = WebTransaction([A, A], 1)

    trans_list = [t1]
    # trans_list = [t1, t2, t3, t4, t5, t6, t7]

    return trans_list


if __name__ == "__main__":

    transList = getTransList()

    # Calculate scores
    scoredSequenceDict, listSequenceDict = process(transList)

    # Sort Scored sequence
    import operator
    from operator import itemgetter

    sortedScoredSequenceDict = sorted(scoredSequenceDict.items(), key=operator.itemgetter(1), reverse=True)
    for key, value in sortedScoredSequenceDict:
        eventList = listSequenceDict[key]
        for e in eventList:
            print(e.name + "->", end="")
        print(str(value))
    print("\n")

    # Merge Sequence
    mergedList = mergeProcessedSeq(sortedScoredSequenceDict, listSequenceDict)
    print("Merged Sequence is")
    for item in mergedList:
        print(item.key)
        for subItems in item.scoredSequenceList:
            print(subItems)
        print("\n")
