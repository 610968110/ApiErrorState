from abc import ABC

from main.util import Util
import abc


class FileMaker(object):
    """
    该类是将json解析到多个文件中
    """
    _root_name = "Global"
    _root_template = r"{{ROOT}}"
    _root_key = r"{{KEY}}"
    _root_value = r"{{VALUE}}"
    _root_header_start = r"{{HEADER_START}}"
    _root_header_end = r"{{HEADER_END}}"
    _root_content_start = r"{{CONTENT_START}}"
    _root_content_end = r"{{CONTENT_END}}"

    def __init__(self, state_dict, save_path, template_file) -> None:
        """
        :param state_dict: 错误码的字典
        :param save_path: 存储的文件路径
        :param template_file: 模板文件的路径
        """
        transform = eval(Util.get_transform_config())
        self._transform_config = transform if isinstance(transform, dict) else {}
        append = eval(Util.get_append_config())
        append_config = append if isinstance(append, dict) else {}
        if len(append_config):
            state_dict["other"] = append_config
        self._state_dict = state_dict
        self._path = save_path
        self._template_file_content = Util.parse_template_content_from_path(template_file)
        Util.mkdir(path=self._path)
        super().__init__()

    def make_file(self, root_name=_root_name, enum_name=_root_name, state_dict=None):
        self._make_root_file(root_name, enum_name, state_dict)

    def _make_root_file(self, root_name, enum_name, state_dict):
        """
        :param state_dict: 需要解析的json字典
        :param root_name: 储存的文件名
        :param enum_name: 文件中的枚举名
        :return:
        """
        if not state_dict:
            state_dict = self._state_dict
        sub_state_dict = {}
        for (k, v) in state_dict.items():
            if isinstance(v, dict):
                self._make_root_file(k, k, v)
            else:
                sub_state_dict[k] = v
        file_name = self.file_name(root_name)
        self._make_sub_file(sub_state_dict, file_name, enum_name)

    def _make_sub_file(self, sub_state_dict, file_name, enum_name):
        """
        :param sub_state_dict: 错误码的字典
        :param file_name: 存储的文件名
        :param enum_name: 存储文件中的的枚举名
        :return:
        """
        enum_name = self.state_enum_name(enum_name)
        file_path = self._path
        enum_content = ""
        # 枚举的名字
        template_file_content = self._template_file_content.replace(self._root_template, enum_name)
        # 枚举的头部
        re_header_rule = r"%s.*%s" % (FileMaker._root_header_start, FileMaker._root_header_end)
        h = Util.re_search(re_header_rule, template_file_content)
        if h:
            self._template_file_content = template_file_content \
                .replace(FileMaker._root_header_start, "") \
                .replace(FileMaker._root_header_end, "")
        # 枚举的内容体
        re_content_rule = r"%s(.*)%s" % (FileMaker._root_content_start, FileMaker._root_content_end)
        c = Util.re_search(re_content_rule, template_file_content)
        if c:
            for (k, v) in sub_state_dict.items():
                transform = self._transform_config.get(v)
                if transform:
                    k = transform
                content = c.group(1) \
                    .replace(FileMaker._root_key, self.state_key_name(k)) \
                    .replace(FileMaker._root_value, "%d" % v) \
                    .replace("\n", "", -1)
                enum_content = "%s%s\n" % (enum_content, content)
        template_file_content = Util.re_sub(re_content_rule, enum_content, template_file_content)
        self._write_to_file(template_file_content, "%s/%s" % (file_path, file_name), "w")

    def _write_to_file(self, content, file_path, mode):
        with open(file_path, mode) as file:
            file.write(content)

    @abc.abstractmethod
    def file_name(self, file_name):
        """
        文件名
        """
        return file_name

    @abc.abstractmethod
    def state_enum_name(self, enum_name):
        """
        枚举名
        """
        return enum_name

    @abc.abstractmethod
    def state_key_name(self, key_name):
        """
        枚举item名
        """
        return key_name


class SingleFileMaker(FileMaker, ABC):
    """
    该类是将json解析到一个文件中
    """

    def make_file(self, root_name=FileMaker._root_name,
                  enum_name=FileMaker._root_name, state_dict=None):
        Util.rm_file("%s/%s" % (self._path, self.file_name("")))
        template_file_content = self._template_file_content
        # 枚举的头部
        re_header_rule = r"%s(.*)%s" % (FileMaker._root_header_start, FileMaker._root_header_end)
        h = Util.re_search(re_header_rule, template_file_content)
        header = ""
        if h:
            self._template_file_content = template_file_content.replace(h.group(0), "")
            header = h.group(1).strip()
        super().make_file(root_name, enum_name, state_dict)
        with open("%s/%s" % (self._path, self.file_name("")), "r+") as f:
            old = f.read()
            f.seek(0)
            f.write("%s%s" % (header, old))

    def _make_sub_file(self, sub_state_dict, file_name, enum_name):
        super()._make_sub_file(sub_state_dict, self.file_name(file_name), enum_name)

    def _write_to_file(self, content, file_path, mode):
        super()._write_to_file(content, file_path, "a")
