from enum import Enum


class ArticleStatus:
    UNREAD = 0
    READ = 1
    COLLECTED = 2
    DISLIKE = -1


class SubCode2SubText:
    EESS_SY = "Systems and Control (eess.SY)"
    CS_LG = "Machine Learning (cs.LG)"
    CS_IT = "Information Theory (cs.IT)"
    CS_CL = "Computation and Language (cs.CL)"
    CS_CV = "Computer Vision and Pattern Recognition (cs.CV)"
    CS_RO = "Robotics (cs.RO)"
    CS_AI = "Artificial Intelligence (cs.AI)"
    CS_ET = "Emerging Technologies (cs.ET)"
    CS_GT = "Computer Science and Game Theory (cs.GT)"
    CS_DB = "Databases (cs.DB)"
    CS_IR = "Information Retrieval (cs.IR)"
    MATH_NA = "Numerical Analysis (math.NA)"
    CS_NI = "Networking and Internet Architecture (cs.NI)"
    CS_CR = "Cryptography and Security (cs.CR)"
    CS_NE = "Neural and Evolutionary Computing (cs.NE)"
    CS_DS = "Data Structures and Algorithms (cs.DS)"
    CS_SE = "Software Engineering (cs.SE)"
    CS_CY = "Computers and Society (cs.CY)"
    CS_SD = "Sound (cs.SD)"
    CS_DM = "Discrete Mathematics (cs.DM)"
    CS_MA = "Multiagent Systems (cs.MA)"
    CS_HC = "Human-Computer Interaction (cs.HC)"
    CS_CC = "Computational Complexity (cs.CC)"
    CS_AR = "Hardware Architecture (cs.AR)"


class SubText2SubCode:
    @staticmethod
    def __getitem__(item):
        dic = {v: k for k, v in SubCode2SubText.__dict__.items()}
        return dic[item]


class ArticleOperateCode:
    READ = 1
    COLLECT = 2
    DISLIKE = 3
    DisCOLLECT = 4
    SHARE = 5
