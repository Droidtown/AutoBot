#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
from glob import glob
from requests import post

import csv
import json
import re
import string


try:
    accountDICT = json.load(open("account.info", encoding="utf-8"))
except:
    accountDICT = {"username":""}

articut = Articut(username=accountDICT["username"], apikey=accountDICT["apikey"])


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
    def __init__(self, PK, seedQ):
        """
        PK: 原始 json 檔中的 key 名稱，例如：「成立時間：」
        PKattribute: 原始 json 檔中的 key 的性質，例如：time

        """
        self.PK:str = PK
        self.PKattribute:str = type(self).__name__
        self.whenLIST:list = ["什麼時候", "甚麼時候", "哪時候", "哪時", "哪一年", "哪年", "啥時候", "啥時", "何年", "何時"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []
        self.qLIST.append(f"{seedQ.split('是')[0]}")

    def generateWhenQLIST(self, inputQ:str, seed="哪一年") -> list:
        """
        搭配 LLM 產生的 whenLIST，做出 WHEN 問句。
        """
        llmResultDICT = self._w2vLLM(username=accountDICT["username"], seed=seed)
        if llmResultDICT["status"] == True:
            self.whenLIST.extend(llmResultDICT["result"])
        self.whenLIST = [w for w in list(set(self.whenLIST)) if set(w).isdisjoint(string.ascii_lowercase+string.ascii_uppercase+"不無在某是")]

        for i in self.whenLIST:
            self.qLIST.append(inputQ.replace(seed, i))
        return self.qLIST

    def _w2vLLM(self, username:str="", seed:str=""):
        w2vLIST = []
        url = "https://api.droidtown.co/Loki/Call/" # 中文版
        if username != "":
            payload = {
              "username": username,
              "func": "call_llm",
              "data": {
                "model": "Gemma2-9B", # [Gemma2-9B, Gemma3-12B, Gemma3-27B, Gemma3-27B-QAT, Llama3-8B, Llama3-70B, Llama3-Taiwan-8B, Llama3.3-70B, Phi3-3B, Phi4-14B, Nemotron-4B]
                "system": "You are a Traditional Chinese word2vec model.", # optional
                "assistant": "You will reply in Mandarin Chinese used in Taiwan. Reply format will be a JSON list in the format [<word>, <word>...]. Use semi-width comma as seperator.", # optional
                "user": f"Return top 10 synonyms of {seed} as a word2vec model, ignore the confidence.", # required
              }
            }
            try:
                result = post(url, json=payload).json()
            except Exception as err:
                return f"Unexpected {err}, {type(err)}"

            try:
                llmResultSTR = self.listPAT.findall(str(result["result"][0]["message"]))[0]
                dialect = self.sniffer.sniff(llmResultSTR)
            except:
                try:
                    llmResultSTR = self.listPAT.findall(str(result["result"][0]["message"]))[0]
                    dialect = self.sniffer.sniff(llmResultSTR)
                except Exception as e:
                    return {"status":False, "result":[], "msg":f"{e}"}

            for i in llmResultSTR.split(dialect.delimiter):
                if "的" in i:
                    pass
                else:
                    w2vLIST.append(i.replace("\n", "").replace("\\n", "").replace("'", "").replace('"', "").strip().lstrip("是").rstrip("嗎"))
                    w2vLIST = list(set(w2vLIST))

            return {"status":True, "result":w2vLIST, "msg":"success"}
        else:
            return {"status":False, "result":[], "msg":f"需要卓騰語言科技網站帳號(email)才能使用。請至 {url.split('Loki')[0]} 完成註冊"}

    def TGgenerateWhenQLIST(self, inputQ:str) -> list:
        if self.PK == "":
            return None
        else:
            pass
        resultDICT = articut.parse(self.PK)
        verbLIST = articut.getVerbStemLIST(resultDICT)[0]
        if verbLIST == []:
            pass
        else:
            verb = verbLIST[0][-1]

        for i in self.whenLIST:
            self.qLIST.append(f"{inputQ.split(self.PK)[0].rstrip('的')}{i}{verb}")
            self.qLIST.append(f"{i}{inputQ.split(self.PK)[0].rstrip('的')}{verb}")
        return self.qLIST

class Person:
    def __init__(self, PK, seedQ):
        """
        PK: 原始 json 檔中的 key 名稱，例如：「成立時間：」
        PKattribute: 原始 json 檔中的 key 的性質，例如：time
        """
        self.PK:str = PK
        self.PKattribute:str = type(self).__name__
        self.whoLIST:list = ["誰", "什麼人", "甚麼人", "哪個人", "哪人", "哪一位", "哪位", "啥人", "何人"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []
        self.qLIST.append(f"{seedQ.split('是')[0]}")

    def generateWhoQLIST(self, inputQ:str, seed="哪位") -> list:
        """
        搭配 LLM 產生的 whoLIST，做出 WHO 問句。
        """
        llmResultDICT = self._w2vLLM(username=accountDICT["username"], seed=seed)
        if llmResultDICT["status"] == True:
            self.whoLIST.extend(llmResultDICT["result"])
        self.whoLIST = [w for w in list(set(self.whoLIST)) if set(w).isdisjoint(string.ascii_lowercase+string.ascii_uppercase+"不無在某是")]

        for i in self.whoLIST:
            self.qLIST.append(inputQ.replace(seed, i))
        return self.qLIST

    def _w2vLLM(self, username:str="", seed:str=""):
        w2vLIST = []
        url = "https://api.droidtown.co/Loki/Call/" # 中文版
        if username != "":
            payload = {
              "username": username,
              "func": "call_llm",
              "data": {
                "model": "Gemma2-9B", # [Gemma2-9B, Gemma3-12B, Gemma3-27B, Gemma3-27B-QAT, Llama3-8B, Llama3-70B, Llama3-Taiwan-8B, Llama3.3-70B, Phi3-3B, Phi4-14B, Nemotron-4B]
                "system": "You are a Traditional Chinese word2vec model.", # optional
                "assistant": "You will reply in Mandarin Chinese used in Taiwan. Reply format will be a JSON list in the format [<word>, <word>...]. Use semi-width comma as seperator.", # optional
                "user": f"Return top 10 synonyms of {seed} as a word2vec model, ignore the confidence.", # required
              }
            }
            try:
                result = post(url, json=payload).json()
            except Exception as err:
                return f"Unexpected {err}, {type(err)}"

            try:
                llmResultSTR = self.listPAT.findall(str(result["result"][0]["message"]))[0]
                dialect = self.sniffer.sniff(llmResultSTR)
            except:
                llmResultSTR = self.listPAT.findall(str(result["result"][0]["message"]))[0]
                dialect = self.sniffer.sniff(llmResultSTR)

            for i in llmResultSTR.split(dialect.delimiter):
                if "的" in i:
                    pass
                else:
                    w2vLIST.append(i.replace("\n", "").replace("\\n", "").replace("'", "").replace('"', "").strip().lstrip("是").rstrip("嗎"))
                    w2vLIST = list(set(w2vLIST))

            return {"status":True, "result":w2vLIST, "msg":"success"}
        else:
            return {"status":False, "result":[], "msg":f"需要卓騰語言科技網站帳號(email)才能使用。請至 {url.split('Loki')[0]} 完成註冊"}

    def TGgenerateWhoQLIST(self, inputQ:str) -> list:
        if self.PK == "":
            return None
        else:
            pass
        resultDICT = articut.parse(self.PK, level="lv1")
        verbLIST = articut.getVerbStemLIST(resultDICT)[0]
        if verbLIST == []:
            pass
        else:
            verb = verbLIST[0][-1]

        for i in self.whoLIST:
            self.qLIST.append(f"{inputQ.split(self.PK)[0].rstrip('的')}{i}{verb}")
            self.qLIST.append(f"{i}{verb}{inputQ.split(self.PK)[0].rstrip('的')}")
        return self.qLIST

class NumberString:
    def __init__(self, PK, seedQ):
        """
        PK: 原始 json 檔中的 key 名稱，例如：「成立時間：」
        PKattribute: 原始 json 檔中的 key 的性質，例如：time
        """
        self.PK:str = PK
        self.PKattribute:str = type(self).__name__
        self.howManyQLIST:list = ["多少", "什麼"]
        self.listPAT = re.compile("(?<=\[)[^\]]+(?=\])")
        self.sniffer = csv.Sniffer()
        self.qLIST:list = []
        self.qLIST.append(f"{seedQ.split('是')[0]}")

    def generateHowManyQLIST(self, inputQ:str, seed="多少") -> list:
        """
        搭配 LLM 產生的 howManyQLIST，做出 WHO 問句。
        """
        llmResultDICT = self._w2vLLM(username=accountDICT["username"], seed=seed)
        if llmResultDICT["status"] == True:
            self.howManyQLIST.extend(llmResultDICT["result"])
        self.howManyQLIST = [w for w in list(set(self.howManyQLIST)) if set(w).isdisjoint(string.ascii_lowercase+string.ascii_uppercase+"不無在某是")]

        for i in self.howManyQLIST:
            self.qLIST.append(inputQ.replace(seed, i))
        return self.qLIST

    def _w2vLLM(self, username:str="", seed:str=""):
        w2vLIST = []
        url = "https://api.droidtown.co/Loki/Call/" # 中文版
        if username != "":
            payload = {
              "username": username,
              "func": "call_llm",
              "data": {
                "model": "Gemma2-9B", # [Gemma2-9B, Gemma3-12B, Gemma3-27B, Gemma3-27B-QAT, Llama3-8B, Llama3-70B, Llama3-Taiwan-8B, Llama3.3-70B, Phi3-3B, Phi4-14B, Nemotron-4B]
                "system": "You are a Traditional Chinese word2vec model.", # optional
                "assistant": "You will reply in Mandarin Chinese used in Taiwan. Reply format will be a JSON list in the format [<word>, <word>...]. Use semi-width comma as seperator.", # optional
                "user": f"Return top 10 synonyms of {seed} as a word2vec model, ignore the confidence.", # required
              }
            }
            try:
                result = post(url, json=payload).json()
            except Exception as err:
                return f"Unexpected {err}, {type(err)}"

            try:
                llmResultSTR = self.listPAT.findall(str(result["result"][0]["message"]))[0]
                dialect = self.sniffer.sniff(llmResultSTR)
            except:
                llmResultSTR = self.listPAT.findall(str(result["result"][0]["message"]))[0]
                dialect = self.sniffer.sniff(llmResultSTR)

            for i in llmResultSTR.split(dialect.delimiter):
                if "的" in i:
                    pass
                else:
                    w2vLIST.append(i.replace("\n", "").replace("\\n", "").replace("'", "").replace('"', "").strip().lstrip("是").rstrip("嗎"))
                    w2vLIST = list(set(w2vLIST))

            return {"status":True, "result":w2vLIST, "msg":"success"}
        else:
            return {"status":False, "result":[], "msg":f"需要卓騰語言科技網站帳號(email)才能使用。請至 {url.split('Loki')[0]} 完成註冊"}

    def TGgenerateHowManyQLIST(self, inputQ:str="", ud:dict={}) -> list:
        if self.PK == "":
            return None
        else:
            pass
        resultDICT = articut.parse(self.PK, level="lv1", userDefinedDictFILE="./SkipKeyDICT.json")
        verbLIST = articut.getVerbStemLIST(resultDICT)[0]
        if verbLIST == []:
            verb = ""
        else:
            if self.PK.startswith(verbLIST[0][0]) and self.PK.endswith(verbLIST[0][-1]):
                verb = self.PK
            else:
                verb = verbLIST[0][-1]
        if self.PK.endswith(verb):
            verb = self.PK
        else:
            pass
        for i in self.howManyQLIST:
            if "什麼" in i:
                self.qLIST.append(f"{inputQ.split(self.PK)[0].rstrip('的')}{verb}是{i}")
                self.qLIST.append(f"{i}是{inputQ.split(self.PK)[0].rstrip('的')}{verb}")
                self.qLIST.append(f"{i}是{inputQ.split(self.PK)[0]}{verb}")
            else:
                self.qLIST.append(f"{inputQ.split(self.PK)[0].rstrip('的')}{verb}{i}")
                self.qLIST.append(f"{inputQ.split(self.PK)[0].rstrip('的')}{verb}是{i}")

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
        llmResultSTR = self._w2vLLM(username=accountDICT["username"], cue=cue)
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
        #"專利狀況": CompxDictionary,
        "產品/服務簡介": str,
        "公司簡介": str,
        "公司註冊地址": AddressTW,
        "公司英文名稱": str
    }

    #for f in glob("{}/*.json".format(sourceDIR)):
        #inputLIST.append(json.load(open(f, mode="r", encoding="utf-8")))
    #print(inputLIST)

    #t = Time("成立時間", "_Loki_Company_的成立時間是哪一年")
    #t.generateWhenQLIST("_Loki_Company_的成立時間是哪一年")
    #t.TGgenerateWhenQLIST("_Loki_Company_的成立時間是哪一年")
    #print(t.qLIST)

    #p = Person("負責人", "_Loki_Company_的負責人是哪位")
    #p.generateWhoQLIST("_Loki_Company_的負責人是哪位")
    #p.TGgenerateWhoQLIST("_Loki_Company_的負責人是哪位")
    #print(p.qLIST)

    ns = NumberString(PK="統一編號", seedQ="_Loki_Company_的統一編號是多少")
    #ns.generateHowManyQLIST("_Loki_CompanyOwner_的統一編號是多少")
    print(ns.qLIST)
    ns.TGgenerateHowManyQLIST("_Loki_Company_的統一編號是多少")
    print(ns.qLIST)