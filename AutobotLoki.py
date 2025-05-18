#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from glob import glob
from requests import post

import csv
import json
import re

try:
    accountDICT = json.load(open("account.info", encoding="utf-8"))
except:
    accountDICT = {"username":""}

def json2WhenQ():
    """"""
    return None

def json2WhatQ():
    """"""
    return None

def json2HowMuchQ():
    """"""
    return None

def json2HowManyQ():
    """"""
    return None

def json2Where():
    """"""
    return None

class PrimaryKey:
    def __init__(self):
        self.PKattribute:str = "" #e.g., _Loki_CompanyName_
    def setupAtt(self, att:str) -> str:
        self.PKattribute = att
        return self.PKattribute

class Time:
    def __init__(self, PK, PKattribute):
        self.PK:str = PK
        self.PKattribute:str = PKattribute
        self.whenLIST:list = ["什麼時候", "甚麼時候", "哪時候", "哪時", "哪一年", "哪年", "啥時候", "啥時", "何年", "何時"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []

    def generateWhenQLIST(self, inputQ:str, cue="哪一年") -> list:
        llmResultSTR = self._w2vLLM(username=accountDICT["username"], cue)
        dialect = self.sniffer.sniff(llmResultSTR)
        for i in llmResultSTR.split(dialect.delimiter):
            self.whenLIST.append(i.replace("\n", "").replace("\\n", "").replace("'", "").replace('"', "").strip().lstrip("是").rstrip("嗎"))
            self.whenLIST = list(set(self.whenLIST))
        for i in self.whenLIST:
            self.qLIST.append(inputQ.replace(cue, i))
        return self.qLIST

    def _w2vLLM(self, username:str, cue:str):
        url = "https://api.droidtown.co/Loki/Call/" # 中文版
        if username != "":
            payload = {
              "username": username,
              "func": "call_llm",
              "data": {
                "model": "Gemma2-9B", # [Gemma2-9B, Gemma3-12B, Gemma3-27B, Gemma3-27B-QAT, Llama3-8B, Llama3-70B, Llama3-Taiwan-8B, Llama3.3-70B, Phi3-3B, Phi4-14B, Nemotron-4B]
                "system": "You are a Traditional Chinese word2vec model.", # optional
                "assistant": "You will reply in Mandarin Chinese used in Taiwan. Reply format will be a JSON list in the format [<word>, <word>...]. Use semi-width comma as seperator.", # optional
                "user": f"Return at lease 10 synonyms of {cue} as a word2vec model, ignore the confidence.", # required
              }
            }
            try:
                result = post(url, json=payload).json()
            except Exception as err:
                return f"Unexpected {err}, {type(err)}"
            return self.listPAT.findall(str(result["result"][0]["message"]))[0]
        else:
            return f"需要卓騰語言科技網站帳號(email)才能使用。請至 {url.split('Loki')[0]} 完成註冊"

class Person:
    def __init__(self, PK, PKattribute):
        self.PK:str = PK
        self.PKattribute:str = PKattribute
        self.whoLIST:list = ["什麼名字", "什麼人", "哪一位", "哪位", "誰"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []

    def generateHowManyQLIST(self, inputQ:str, cue="誰") -> list:
        for i in self.whoLIST:
            self.qLIST.append(inputQ.replace(cue, i))
        return self.qLIST

class NumberString:
    def __init__(self, PK, PKattribute):
        self.PK:str = PK
        self.PKattribute:str = PKattribute
        self.howManyLIST:list = ["什麼", "多少"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []

    def generateHowManyQLIST(self, inputQ:str, cue="多少") -> list:
        for i in self.howManyLIST:
            self.qLIST.append(inputQ.replace(cue, i))
        return self.qLIST

class Money:
    def __init__(self, PK, PKattribute):
        self.PK:str = PK
        self.PKattribute:str = PKattribute
        self.howMuchMoneyLIST:list = ["多少金額", "多少錢", "多少"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []

    def generateHowMuchMoneyQLIST(self, inputQ:str, cue="多少錢") -> list:
        for i in self.howMuchMoneyLIST:
            self.qLIST.append(inputQ.replace(cue, i))
        return self.qLIST

class Url:
    def __init__(self, PK, PKattribute):
        self.PK:str = PK
        self.PKattribute:str = PKattribute
        self.whatUrlLIST:list = ["什麼"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []

    def generateWhatUrlQLIST(self, inputQ:str, cue="什麼") -> list:
        for i in self.whatUrlLIST:
            self.qLIST.append(inputQ.replace(cue, i))
        return self.qLIST

#class CompxDictionary:
    #先拆分 dict

class AddressTW:
    def __init__(self, PK, PKattribute):
        self.PK:str = PK
        self.PKattribute:str = PKattribute
        self.whereLIST:list = ["什麼地方", "哪裡", "何地"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []

    def _TGgenerateWhereQLIST(self, inputS:str, cue:str="") ->  list:
        self.qLIST.append(f"{self.PKattribute}的地址")
        self.qLIST.append(f"{self.PKattribute}在哪裡")
        for i in self.whereLIST:
            self.qLIST.append(f"{self.PKattribute}在{i}")
        return self.qLIST

    def generateWhereQLIST(self, inputQ:str, cue="哪裡") -> list:
        llmResultSTR = self._w2vLLM(username=accountDICT["username"], cue)
        dialect = self.sniffer.sniff(llmResultSTR)
        for i in llmResultSTR.split(dialect.delimiter):
            self.whereLIST.append(i.replace("\n", "").replace("\\n", "").replace("'", "").replace('"', "").strip().lstrip("是").rstrip("嗎"))
            self.whereLIST = list(set(self.whereLIST))
        for i in self.whereLIST:
            self.qLIST.append(inputQ.replace(cue, i))

    def _w2vLLM(self, username:str, cue:str):
        url = "https://api.droidtown.co/Loki/Call/" # 中文版
        if username != "":
            payload = {
              "username": username,
              "func": "call_llm",
              "data": {
                "model": "Gemma2-9B", # [Gemma2-9B, Gemma3-12B, Gemma3-27B, Gemma3-27B-QAT, Llama3-8B, Llama3-70B, Llama3-Taiwan-8B, Llama3.3-70B, Phi3-3B, Phi4-14B, Nemotron-4B]
                "system": "You are a Traditional Chinese word2vec model.", # optional
                "assistant": "You will reply in Mandarin Chinese used in Taiwan. Reply format will be a JSON list in the format [<word>, <word>...]. Use semi-width comma as seperator.", # optional
                "user": f"Return at lease 10 synonyms of {cue} as a word2vec model, ignore the confidence.", # required
              }
            }
            try:
                result = post(url, json=payload).json()
            except Exception as err:
                return f"Unexpected {err}, {type(err)}"
            return self.listPAT.findall(str(result["result"][0]["message"]))[0]
        else:
            return f"需要卓騰語言科技網站帳號(email)才能使用。請至 {url.split('Loki')[0]} 完成註冊"




if __name__ == "__main__":

#InputSTR
    inputLIST = []
    sourceDIR = "./dev_data"
    configDICT = {
        "公司名稱": PrimaryKey,
        "成立時間": Time,
        "統一編號": NumberString,
        "公司狀態": str,
        "團隊人數": int,
        "實收資本額(元/新台幣)": Money,
        "負責人": Person,
        "主分類": str,
        "官方網站": Url,
        "專利狀況": CompxDictionary,
        "產品/服務簡介": str,
        "公司簡介": str,
        "公司註冊地址": AddressTW,
        "公司英文名稱": str
    }

    for f in glob("{}/*.json".format(sourceDIR)):
        inputLIST.append(json.load(open(f, mode="r", encoding="utf-8")))
    print(inputLIST)