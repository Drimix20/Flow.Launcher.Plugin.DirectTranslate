# -*- coding: utf-8 -*-

import copy
from typing import List

from flowlauncher import FlowLauncher

from googletrans import Translator, constants
from plugin.templates import *


class Main(FlowLauncher):
    messages_queue = []

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

    def query(self, param: str) -> List[dict]:
        query = param.strip()

        query_modified = query.strip().lower()
        splitted_params = query_modified.split(' ')


        if len(splitted_params) < 3:
            self.sendNormalMess(
                "Direct Translate",
                "<Hotkey> <From Language> <To Language> <Text>"
            )
        else:
            from_lang = splitted_params[0]
            to_lang = splitted_params[1]
            
            try:
                translator = Translator()
                translation = translator.translate(' '.join(splitted_params[2:]), src=from_lang, dest=to_lang)

                self.sendNormalMess(
                    str(translation.text),
                    query
                )
            except ValueError as error:
                self.sendNormalMess(
                    str(error),
                    query
                ) 

        return self.messages_queue
