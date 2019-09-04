import json


class JsonParser(object):

    def __init__(self, json_str) -> None:
        super().__init__()
        self.__result = json.loads(json_str)
        self.i = 0

    def parse(self):
        result = self.__result
        # self.__parse_dict("", result, {})
        # return json_dict
        return result

    def __parse_dict(self, key, result, json_dict):
        if not isinstance(result, dict):
            json_dict[result] = key
        else:
            for k in result:
                self.__parse_dict(
                    k if (len(key) == 0) else "%s_%s" % (key, k),
                    result[k],
                    json_dict
                )
