class FrameStatusCode:
    def __init__(self):
        pass

    SUCCESS = ("00000", "请求成功")
    UNABLE_MATCH_ROUTE = ("B0000", "无法匹配路由")

    @staticmethod
    def MISSING_NECESSARY_PARAMETERS(message):
        return "A0000", f"接口缺少必要参数:{message}"

    @staticmethod
    def ROUTE_REGISTERED(message):
        return "B0100", f"路由:{message}已经被注册"

    @staticmethod
    def NEED_INHERIT_BASE_CLASS(message):
        return "W0000", f"此方法类需要继承基础类:{message}"

    @staticmethod
    def REQUEST_METHOD_ERROR(message):
        return "A0200", f"请求方式错误，使用{message}方式再次尝试"

    @staticmethod
    def MESSAGE_JSON_DECODE_ERROR(message):
        return "A0001", f"接口参数序列化失败:{message}"

    @staticmethod
    def SERVER_UNDEFINED_ERROR(message):
        return "C0000", f"服务器未定义异常:{message}"
