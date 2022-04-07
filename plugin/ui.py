# -*- coding: utf-8 -*-

import copy
from typing import List

from flowlauncher import FlowLauncher

from googletrans import Translator
from plugin.templates import *
from plugin.extensions import _


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

        if len(splitted_params) > 1 and len(splitted_params[0]) == 2 and len(splitted_params[1]) != 2:
            # There is only the destination lang: we can assume that the from lang is "auto"
            query_modified = f"auto {query_modified}"
            splitted_params = query_modified.split(' ')

        if len(splitted_params) < 3:
            self.sendNormalMess(
                "Direct Translate",
                _("<Hotkey> <From Language> <To Language> <Text>")
            )
        else:
            from_lang = splitted_params[0]
            to_lang = splitted_params[1]
            
            try:
                translator = Translator()
                translation = translator.translate(' '.join(splitted_params[2:]), src=from_lang, dest=to_lang)

                self.sendNormalMess(
                    _(str(translation.text)),
                    query
                )
            except ValueError as error:
                self.sendNormalMess(
                    _(str(error)),
                    query
                ) 

        return self.messages_queue
