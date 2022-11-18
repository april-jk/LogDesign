from analysis.core.analysisWindows.bruteForce import  findInBruteForce
from analysis.core.analysisWindows.User import findInUser


#判断是否有受攻击成功的痕迹

def hostSecureDetect(data):
    findInBruteForce(data)
    findInUser(data)