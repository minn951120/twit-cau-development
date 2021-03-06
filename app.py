import sys
import os
from IR.highlightAlgo import makeHighlightBystreamer
from IR.vectorizer import vectorize
from IR.query import get_query, similarity_ranks
from IR.evalfunc import distance_func, cosine_func
from downloading import intersect
import pickle


def getStreamerVectors():

    # <Prerequisite>
    # Make streamers vectors and save it as a binary file
    streamerVector = dict()
    chatters_in_streamer = dict()

    SVfilepath = os.path.join(os.getcwd(), "bin", "StreamerVector.dat")
    CISfilepath = os.path.join(os.getcwd(), "bin", "ChattersInStreamer.dat")

    print('Loding...', end=' ')
    if os.path.isfile(SVfilepath) and os.path.isfile(CISfilepath):
        file = open(SVfilepath, "rb")
        streamerVector = pickle.load(file)
        file.close()
        file = open(CISfilepath, "rb")
        chatters_in_streamer = pickle.load(file)
        file.close()

    # If it is the first time making streamer vector
    else:
        if not os.path.exists(os.path.join(os.getcwd(), "bin")):
            os.mkdir(os.path.join(os.getcwd(), "bin"))
        streamerVector, chatters_in_streamer = vectorize()
        file = open(SVfilepath, "wb")
        pickle.dump(streamerVector, file)
        file.close()
        file = open(CISfilepath, "wb")
        pickle.dump(chatters_in_streamer, file)
        file.close()


    if not streamerVector:
        raise FileNotFoundError

    print('Complete.')
    # print(streamerVector)
    return streamerVector, chatters_in_streamer


def main():
    # example) python main.py <streamer's name>
    #               (argv[0])   (argv[1])
    try:

        # <Prerequisite>
        # Make streamers vectors and save it as a binary file

        SV,CIS = getStreamerVectors()

        # 1. Read streamer's vectors from a binary file
        # 2. Check if the input streamer is one of them
        #  2.1 If not, return error
        # 3. Get a closest vector to the input streamer
        # 4. Evaluate the closest vector by followers.
        # 5. Print out the result

        keyword = checkArgument(sys.argv)
        if keyword is None:
            print(
                '\n===============  We provide various streamers below  ===============\n')
            for key in SV.keys():
                print(key)
            print(
                '\n====================================================================')
            keyword = input(
                'Please input one streamer and we will give you the most similar streamer : ')

        print('Your input is ', keyword)

        if keyword not in SV.keys():
            print('Please check your input')
            quit()


        royal = intersect(CIS, mode=1)

        print("\n\n- rank of cosine similarity")
        for rank in cosine_func(SV, keyword):
            print(rank)
            print("royal: ", royal[rank], "%")


        print("\n\n- rank of euclidian distance")
        for rank in distance_func(SV, keyword):
            print(rank)
            print("royal: ", royal[rank], "%")

        # for key, val in CIS.items():
        #     print(key)
        #     print(len(val))

        # Chatlog Analyze
        print(" ====================== ")
        print(" Chat log Analyze START ")
        print(" ====================== ")

        print('[numOfHighlights] the number of expected highlights for each chatlog')
        numOfHighlights = input('Your numOfHighlights is ')

        print(
            '[cummulative_sec] how many next seconds you want to consider for chat analyzing')
        cummulative_sec = input('Your cummulative_sec is ')

        print('[delay] how long each highlight section is suppposed to be')
        delay = input('Your delay is ')

        print(" ====================== ")
        
        makeHighlightBystreamer(
            keyword, int(numOfHighlights), int(cummulative_sec), int(delay))


    except(FileNotFoundError):
        print('Error occurred making streamer as a vector.')


def checkArgument(argv):
    # If there is no argument
    if len(argv) != 2:
        return None
    # elif len(argv) > 2:
    #     print('There are more than 2 arguments')
    #     quit()
    else:
        return argv[1]


if __name__ == "__main__":
    main()
