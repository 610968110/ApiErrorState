#! ./envs/bin/python3.7
# -*- coding: UTF-8 -*-

from main.basis.http_state import State
from main.basis.parser import JsonParser
from main.basis.file_maker import SingleFileMaker, FileMaker
from main.util import Util


class AndroidFileMaker(SingleFileMaker):
    def state_enum_name(self, enum_name):
        return Util.text_first_letter_upper(enum_name)

    def state_key_name(self, key_name):
        return Util.text_underline_mode(key_name)

    def file_name(self, file_name):
        # return "%s.kt" % Util.text_first_letter_upper(file_name)
        return "ApiErrorState.kt"


class IosFileMaker(SingleFileMaker):
    def state_enum_name(self, enum_name):
        return Util.text_first_letter_lower(enum_name)

    def state_key_name(self, key_name):
        return Util.text_first_letter_lower(key_name)

    def file_name(self, file_name):
        # return "%s.swift" % Util.text_first_letter_upper(file_name)
        return "ApiErrorState.swift"


def run():
    #  从网络获取错误码的json字符串
    req_str = State().get_state_json()
    #  将json解析成dict
    err_dict = JsonParser(req_str).parse()

    AndroidFileMaker(
        state_dict=err_dict,
        save_path="./output/android",  # 设置输出路径
        template_file="./template/temp_android.temp"  # 设置模板，不符合需求可以袭击修改
    ).make_file(root_name="global")

    IosFileMaker(
        state_dict=err_dict,
        save_path="./output/ios",
        template_file="./template/temp_ios.temp"
    ).make_file(root_name="global")


if __name__ == '__main__':
    run()
    print("complete")
