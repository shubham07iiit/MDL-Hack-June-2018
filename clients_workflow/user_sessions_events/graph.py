class Test:
    def __init__(self, key):
        self.key = key
        self.scoredSequenceList = []

class EventColor:
    Yellow= "Yellow"
    Green= "Green"

class Event:
    def __init__(self, name, color):
        self.name= name
        self.color= color

    def __repr__(self):
        return self.name +self.color

class WebTransaction:
    def __init__(self, events_arr, identifier):
        self.events_arr = events_arr
        self.id = identifier

    def __repr__(self):
        event_str= ""
        for event in self.events_arr:
            event_str+= event.__repr__()+" "

        return event_str + str(self.id)

class ScoredSequence:
    def __init__(self, events_arr, score):
        self.events_arr= events_arr
        self.score= score

    def ___repr__(self):
        event_str = ""
        for event in self.events_arr:
            event_str += event.__repr__() + " "
        return event_str + self.score

APP_START_EVENT= "app_Launch"
WEB_START_EVENT= "web_login"

def process(trans_list):
    scoredSequenceDict={}
    # // validation : transaction start should be yellow
    for trans in trans_list:
        sequence_str = ""
        if trans.events_arr[0].name.startswith("app_"):
            sequence_str=APP_START_EVENT
        elif trans.events_arr[0].name.startswith("web_"):
            sequence_str=APP_START_EVENT
        else:
            print("Wrong transaction ")
            return []



        for event in trans.events_arr:
            if event.color == EventColor.Yellow:
                sequence_str=event.name
            else:
                sequence_str+=event.name
                if not sequence_str in scoredSequenceDict:
                    scoredSequenceDict[sequence_str]=0
                scoredSequenceDict[sequence_str]= scoredSequenceDict[sequence_str]+1


        # print trans.__repr__()
        # for event in trans.events_arr:


    return scoredSequenceDict

def sortKey(key):
    return key[0]+''.join(sorted(key[1:]))

def mergeProcessedSeq(sorted_x):
    try:
        dict={}
        mergedList=[]  # list of key, scoredsequnce list
        idx=0
        for key,value in sorted_x:
            sortedKey= sortKey(key)

            if sortedKey not in dict:
                dict[sortedKey]=idx
                mergedList.append(Test(sortedKey))
                idx += 1

            mergedList[dict[sortedKey]].scoredSequenceList.append(key)
            mergedList[dict[sortedKey]].scoredSequenceList.append(value)

            return mergedList

    except Exception as excp:
        print "Exception is :" +excp.message

    return mergedList


YELLOW_EVENTS= {"app_loggedIn",
                "app_bgtask_started",
                "app_Launch",
                "web_login",
                "app_LogIn",
                "S",
                "X"}

def getEventColor(eventName):
    if eventName in YELLOW_EVENTS:
        return EventColor.Yellow
    else:
        return EventColor.Green

def getTransList():
    S = Event("app_Launch", EventColor.Yellow)
    A = Event("add_Drive", EventColor.Green)
    C = Event("named_Location", EventColor.Green)

    B = Event("edit_Drive", EventColor.Green)

    X = Event("app_LogIn", EventColor.Yellow)
    Y = Event("delete_Drive", EventColor.Green)

    t1 = WebTransaction([S, A, C, X, Y], 1)
    t2 = WebTransaction([S, A, C], 1)
    t3 = WebTransaction([X, Y], 1)

    t4 = WebTransaction([S, B, A], 1)
    t5 = WebTransaction([S, B, A], 1)
    t6 = WebTransaction([S, B, A], 1)

    t7 = WebTransaction([S, A, A], 1)

    trans_list = [t1, t2, t3, t4, t5, t6, t7]

    return trans_list

if __name__ == "__main__":

    transList= getTransList()
    scoredSequenceDict= process(transList)

    import operator
    from operator import itemgetter
    sorted_x = sorted(scoredSequenceDict.items(), key=operator.itemgetter(1), reverse=True)

    #Print sorted sequence
    for key, value in sorted_x:
        print key+ " "+ str(value)
    print "\n"

    #Print Merged Sequence
    print "Merged Sequence is"
    mergedList= mergeProcessedSeq(sorted_x)
    for item in mergedList:
        print item.key
        for subItems in item.scoredSequenceList:
            print subItems
        print "\n"







