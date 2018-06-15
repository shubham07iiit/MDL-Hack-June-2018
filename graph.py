
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


def process(trans_list):
    scoredSequenceDict={}
    # // validation : transaction start should be yellow
    for trans in trans_list:
        if trans.events_arr[0].color!= EventColor.Yellow:
            print "Wrong transaction "
            return []
        sequence_str=""
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


if __name__ == "__main__":
    S= Event("Start", EventColor.Yellow)
    A= Event("A", EventColor.Green)
    B= Event("B", EventColor.Green)
    C= Event("C", EventColor.Green)

    X= Event("X", EventColor.Yellow)
    Y= Event("Y", EventColor.Green)

    t1= WebTransaction([S,A,C,X,Y], 1)
    t2 = WebTransaction([S, A, C], 1)
    t3 = WebTransaction([X, Y], 1)

    t4 = WebTransaction([S, B, A], 1)
    t5 = WebTransaction([S, B, A], 1)
    t6 = WebTransaction([S, B, A], 1)

    t7 = WebTransaction([S, A, A], 1)


    trans_list= [t1,t2,t3,t4,t5,t6,t7]

    scoredSequenceDict= process(trans_list)
    from operator import itemgetter

    import operator
    sorted_x = sorted(scoredSequenceDict.items(), key=operator.itemgetter(1))
    for key, value in sorted_x:
        print key+ " "+ str(value)
    # for key,value in sorted(scoredSequenceDict.iteritems(), key=itemgetter(1), reverse=True):
    #     print key+ " "+ str(value)


