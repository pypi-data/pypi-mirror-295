import threading


class ConfigSingletonDict(dict):
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(ConfigSingletonDict, cls).__new__(
                        cls, *args, **kwargs
                    )
        return cls._instance

    def __init__(self):
        super(ConfigSingletonDict, self).__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"


class RouterSingletonDict(dict):
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(RouterSingletonDict, cls).__new__(
                        cls, *args, **kwargs
                    )
        return cls._instance

    def __init__(self):
        super(RouterSingletonDict, self).__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"


class ConnectSingletonDict(dict):
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(ConnectSingletonDict, cls).__new__(
                        cls, *args, **kwargs
                    )
        return cls._instance

    def __init__(self):
        super(ConnectSingletonDict, self).__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"


if __name__ == "__main__":
    single_dict = ConnectSingletonDict()
    single_dict["name"] = "linwanlong"
    print(single_dict)
    single_dict_2 = ConnectSingletonDict()
    single_dict["age"] = "24"
    print(single_dict)
    print(single_dict["age"])
