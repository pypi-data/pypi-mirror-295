from lced_exceptions.frame_exception import FrameException
from lced_exceptions.status_code import FrameStatusCode
from lced_variables.dict_var import RouterSingletonDict, ConfigSingletonDict


def Handler(url: str, desc: str = None):
    route_prefix = ConfigSingletonDict()["config_info"]["BIND"]["route_prefix"]

    def wrapper(cls):
        tag = "base_func"
        if not (tag in dir(cls)):
            raise FrameException(
                *FrameStatusCode.NEED_INHERIT_BASE_CLASS("BaseHandler")
            )
        res = [
            item
            for item in RouterSingletonDict().get("dynamic_methods", [])
            if item[0] == cls.__name__
        ]

        for item in res:
            func_name = item[1]
            func_handler = item[2]
            func_full_url = route_prefix + url + item[3]
            for router in RouterSingletonDict().get("register_route", []):
                if func_full_url == router[0]:
                    raise FrameException(
                        *FrameStatusCode.ROUTE_REGISTERED(func_full_url)
                    )
            RouterSingletonDict().setdefault("register_route", []).append(
                (func_full_url, getattr(cls, tag))
            )
            RouterSingletonDict().setdefault("handler_mapping", []).append(
                (func_full_url, func_name, func_handler, cls)
            )
        cls.desc = desc
        return cls

    return wrapper


def HandlerMapping(url: str = "", title: str = None, client_name: str = None):
    def wrapper(func):
        path = url
        if not path:
            path = f"/{func.__name__}"
        RouterSingletonDict().setdefault("dynamic_methods", []).append(
            (
                func.__qualname__.replace("." + func.__name__, ""),
                func.__name__,
                func,
                path,
                title,
                client_name,
            )
        )
        return func

    return wrapper
