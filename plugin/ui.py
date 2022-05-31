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
    items = []

    @staticmethod
    def system_lang():
        lang = locale.getdefaultlocale()
        return lang[0][:2] if lang else "en"

    def add_item(self, title: str, subtitle: str):
        self.items.append({'Title': title, 'SubTitle': subtitle, 'IcoPath': ICON_PATH})

    @staticmethod
    def valid_lang(lang: str) -> bool:
        return lang in LANGUAGES or lang in SPECIAL_CASES

    def translate(self, src: str, dest: str, query: str):
        try:
            translator = Translator()
            if src == "auto":
                src = translator.detect(query).lang
                sources = src if isinstance(src, list) else [src]
            else: sources = [src]

            for src in sources:
                translation = translator.translate(query, src=src, dest=dest)
                self.add_item(_(str(translation.text)), f"{src} → {dest}   {query}")
        except Exception as error:
            self.add_item(_(str(error)), f"{src} → {dest}   {query}")
        return self.items

    def help_action(self):
        self.add_item("direct translate", _("<hotkey> <from language> <to language> <text>"))
        return self.items

    def query(self, param: str='') -> List[dict]:
        query = param.strip().lower()
        params = query.split(" ")

        try:
            if len(params) < 1 or len(params[0]) < 2 or not params[1]: return self.help_action()
            # no lang_code: <auto> -> <system language>
            if not self.valid_lang(params[0]): return self.translate("auto", self.system_lang(), query)
            # one lang_code: <auto> -> lang_code
            if not self.valid_lang(params[1]): return self.translate("auto", params[0], " ".join(params[1:]))
            # 2 lang_codes: lang1 -> lang2
            return self.translate(params[0], params[1], " ".join(params[2:]))
        except IndexError:
            return self.help_action()
