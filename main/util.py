import os
import re


class Util(object):
    """
    创建文件夹
    """

    @staticmethod
    def mkdir(path):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    @staticmethod
    def rmdir(path):
        folder = os.path.exists(path)
        if folder:
            os.remove(path)

    @staticmethod
    def rm_file(path):
        file = os.path.exists(path)
        if file:
            os.remove(path)

    @staticmethod
    def parse_template_lines_from_path(path):
        with open(path, "r") as file:
            return file.readlines()

    @staticmethod
    def parse_template_content_from_path(path):
        with open(path, "r") as file:
            return file.read()

    @staticmethod
    def re_search(re_str, content_str):
        return re.search(re_str, content_str, re.S)

    @staticmethod
    def re_sub(re_str, rep, content_str):
        return re.sub(re_str, rep, content_str, flags=re.S)

    @staticmethod
    def text_first_letter_upper(text):
        """
        首字母大写
        :param text:  fileName
        :return:   FileName
        """
        if text and len(text) > 0 and text[0].islower():
            text = "%s%s" % (text[0].upper(), text[1:])
            return text
        return text

    @staticmethod
    def text_first_letter_lower(text):
        """
        首字母小写
        :param text:  FileName
        :return:   fileName
        """
        if text and len(text) > 0 and text[0].isupper():
            text = "%s%s" % (text[0].lower(), text[1:])
            return text
        return text

    @staticmethod
    def text_underline_mode(text):
        """
        转化成全大写下划线分隔命名，以大写字母识别分隔
        :param text:  AbcDef
        :return: ABC_DEF
        """
        lst = []
        for index, char in enumerate(text):
            if char.isupper() and index != 0:
                lst.append("_")
            lst.append(char)
        return "".join(lst).upper()

    @staticmethod
    def get_append_config():
        with open("./append.config", "r") as f:
            return f.read()

    @staticmethod
    def get_transform_config():
        with open("./transform.config", "r") as f:
            return f.read()
