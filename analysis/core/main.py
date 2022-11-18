import pickle
from analysis.core.analysisWindows.bruteForce import id4624,id4625
from analysis.core.analysisWindows.hostSecureDetect import hostSecureDetect

f = open('../../pklFile/test_all.pkl', 'rb')
df = pickle.load(f)
f.close()

def generatIPList():
    for data in df.values:
        # print(data[1]) #2022-04-18 20:11:53
        '''
        4624.4625都是29
        '''

        id4625(data)
        id4624(data)

if __name__ == '__main__':
    # generatIPList()
    for data in df.values:
        hostSecureDetect(data)
