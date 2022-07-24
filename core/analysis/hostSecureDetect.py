from core.analysis.bruteForce import  findInBruteForce
from core.analysis.User import findInUser


#判断是否有受攻击成功的痕迹

def hostSecureDetect(data):
    findInBruteForce(data)
    findInUser(data)