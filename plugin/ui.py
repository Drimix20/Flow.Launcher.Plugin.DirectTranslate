# -*- coding: utf-8 -*-

import copy
from typing import List

from flowlauncher import FlowLauncher

from googletrans import Translator
from googletrans.constants import LANGUAGES, SPECIAL_CASES
from plugin.templates import *
from plugin.extensions import _
import locale


class Main(FlowLauncher):
    messages_queue = []

    @staticmethod
    def system_lang():
        lang = locale.getdefaultlocale()
        return lang[0][:2] if lang else "en"

    def sendNormalMess(self, title: str, subtitle: str):
        message = copy.deepcopy(RESULT_TEMPLATE)
        message["Title"] = title
        message["SubTitle"] = subtitle

        self.messages_queue.append(message)

    def sendActionMess(self, title: str, subtitle: str, method: str, value: List):
        # information
        message = copy.deepcopy(RESULT_TEMPLATE)
        message["Title"] = title
        message["SubTitle"] = subtitle

        # action
        action = copy.deepcopy(ACTION_TEMPLATE)
        action["JsonRPCAction"]["method"] = method
        action["JsonRPCAction"]["parameters"] = value
        message.update(action)

        self.messages_queue.append(message)

    @staticmethod
    def valid_lang(lang: str) -> bool:
        return lang in LANGUAGES or lang in SPECIAL_CASES

    def translate(self, src: str, dest: str, query: str):
        try:
            translator = Translator()
            if src == "auto":
                src = translator.detect(query).lang

            translation = translator.translate(query, src=src, dest=dest)
            self.sendNormalMess(_(str(translation.text)), f"{query}   [{src} → {dest}]")
        except ValueError as error:
            self.sendNormalMess(_(str(error)), f"{query}   [{src} → {dest}]")
        return self.messages_queue

    def query(self, param: str) -> List[dict]:
        query = param.strip().lower()
        params = query.split(" ")

        if len(params) <= 1:
            self.sendNormalMess("direct translate", _("<hotkey> <from language> <to language> <text>"))
            return self.messages_queue

        # no lang_code: <auto> -> <system language>
        if not self.valid_lang(params[0]): return self.translate("auto", self.system_lang(), query)
        # one lang_code: <auto> -> lang_code
        if not self.valid_lang(params[1]): return self.translate("auto", params[0], " ".join(params[1:]))
        # 2 lang_codes: lang1 -> lang2
        return self.translate(params[0], params[1], " ".join(params[2:]))
