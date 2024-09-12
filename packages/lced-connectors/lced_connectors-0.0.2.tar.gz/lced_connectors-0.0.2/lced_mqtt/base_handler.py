import inspect
import json
import traceback

from lced_exceptions.frame_exception import FrameException
from lced_exceptions.status_code import FrameStatusCode
from lced_utils.buffer_utils import get_handler_mapping_info
from lced_utils.data_utils import parse_val
from lced_utils.logger_utils import logger


class BaseHandler:
    @staticmethod
    def base_func(client, userdata, message):
        try:
            BaseHandler.base_func_core(client, userdata, message)
        except Exception as e:
            tb_string = traceback.format_exc()
            logger.error(f"{e}\n{'#' * 100}\n{tb_string}{'#' * 100}")

    @staticmethod
    def base_func_core(client, userdata, message):
        res = [item for item in get_handler_mapping_info() if item[0] == message.topic]
        if res:
            func_name = res[0][1]
            func_handler = res[0][2]
            class_handler = res[0][3]
            params_list = []
            arguments = {}
            if message.payload:
                query_arguments = json.loads(message.payload.decode("utf-8"))
                arguments.update(query_arguments)
            signature = inspect.signature(func_handler)
            for parameter_name, parameter in signature.parameters.items():
                if parameter_name == "self":
                    pass
                else:
                    argument_value = arguments.get(parameter_name)
                    if argument_value is None:
                        if parameter.default is not inspect.Parameter.empty:
                            params_list.append(parameter.default)
                            continue
                        else:
                            raise FrameException(
                                *FrameStatusCode.MISSING_NECESSARY_PARAMETERS(
                                    parameter_name
                                )
                            )
                    parameter_type = parameter.annotation
                    if parameter_type is inspect.Parameter.empty:
                        parameter_type = type(parameter.default)
                    if isinstance(argument_value, list):
                        params_list.append(
                            [parse_val(v, parameter_type) for v in argument_value]
                        )
                    else:
                        params_list.append(parse_val(argument_value, parameter_type))
            logger().info(
                f"Mqtt receiving info include <topic:{message.topic}, payload:{arguments}, qos:{message.qos}, retain:{message.retain}>"
            )
            exec_func = getattr(class_handler(), func_name)
            data = exec_func(*params_list)
            if data:
                qos = 2
                retain = False
                p_topic = data.get("topic")
                p_payload = json.dumps(data.get("payload", {}), ensure_ascii=False)
                client.publish(p_topic, p_payload, qos=qos, retain=retain)
                logger().info(
                    f"Mqtt sending info include <system_code:{FrameStatusCode.SUCCESS[0]}, topic:{p_topic}, payload:{p_payload}, qos:{qos}, retain:{retain}>"
                )
        else:
            raise FrameException(*FrameStatusCode.UNABLE_MATCH_ROUTE)
