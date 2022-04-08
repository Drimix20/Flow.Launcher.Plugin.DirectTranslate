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

    def getSystemLanguage(self):
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

    def query(self, param: str) -> List[dict]:
        query = param.strip().lower()
        params = query.split(" ")
        cnt_words = len(params)

        if cnt_words <= 1:
            self.sendNormalMess("Direct Translate", _("<Hotkey> <From Language> <To Language> <Text>"))
        else:
            if not self.valid_lang(params[0]):
                # no lang_code provided: <auto> -> <system default language>
                lang1, lang2 = "auto", self.getSystemLanguage()
            else:
                if not self.valid_lang(params[1]):
                    # one lang_code provided: <auto> -> lang_code
                    lang1, lang2 = "auto", params[0]
                    query = " ".join(params[1:])
                else:
                    # 2 lang_codes provided: lang_code -> lang_code
                    lang1, lang2 = params[:2]
                    query = " ".join(params[2:])

            try:
                translator = Translator()
                if lang1 == "auto":
                    lang1 = translator.detect(query).lang

                translation = translator.translate(query, src=lang1, dest=lang2)
                self.sendNormalMess(_(str(translation.text)), f"{query}   [{lang1} → {lang2}]")
            except ValueError as error:
                self.sendNormalMess(_(str(error)), query)

        return self.messages_queue
