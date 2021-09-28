# -*- coding: utf-8 -*-

import copy
from typing import List

from flowlauncher import FlowLauncher

from textblob import TextBlob, exceptions
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
        q = param.strip()

        query_modified = q.strip().lower()
        splitted_params = query_modified.split(' ')
 

        if len(splitted_params) < 3:
            self.sendNormalMess(
                "Direct Translate",
                "<Hotkey> <From Language> <To Language> <Text>"
            )
        else:
            from_lang = splitted_params[0]
            to_lang = splitted_params[1]
            
            if query_modified:
                try:
                    blob = TextBlob(' '.join(splitted_params[2:]))
                    translation = blob.translate(from_lang, to_lang)

                    self.sendNormalMess(
                        str(translation),
                        q
                    )
                except exceptions.NotTranslated:
                    self.sendNormalMess(
                        "Query not changed",
                        q
                    )
            # TODO not sure if required to handle it correctly
            # if not results:
            #     results.append({
            #             "Title": 'Not found',
            #             "SubTitle": query,
            #             "IcoPath":"Images/app.png"
            #         })

        return self.messages_queue
