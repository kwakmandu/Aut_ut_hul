import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import inspect

MAX_BYTE = 1024


class SingletonMeta(type):
    """
    싱글턴 메타클래스로, 인스턴스가 한 개만 존재하도록 보장합니다.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.init_logger()

    def init_logger(self):
        self.logger = logging.getLogger("DSLogger")
        self.logger.setLevel(logging.INFO)

        # 로그 파일 설정
        self.handler = RotatingFileHandler(
            "../log/latest.log", maxBytes=MAX_BYTE, backupCount=0
        )
        # %(name)s 부분을 30자 길이로 고정
        formatter = logging.Formatter("[%(asctime)s] %(class.func)-30s :%(message)s")
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False

    def rotate_logs(self):
        """
        로그 파일을 회전시키고, 필요한 경우 확장자만 변경합니다.
        """
        self.handler.close()
        self.logger.removeHandler(self.handler)

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"../log/until_{current_time}.log"
        os.rename("../log/latest.log", new_filename)

        # 이전 로그 파일 확장자 변경
        self.rename_old_logs()

        # 로거 다시 초기화
        self.init_logger()

    def rename_old_logs(self):
        """
        가장 최근 로그 파일을 제외하고 나머지 로그 파일의 확장자를 .zip으로 변경합니다.
        """
        log_files = sorted(
            [
                "../log/" + f
                for f in os.listdir("../log")
                if f.startswith("until_") and not f.endswith(".zip")
            ],
            key=lambda x: os.path.getmtime(x),
        )

        for log_file in log_files[:-1]:  # 가장 최근 파일을 제외한 모든 파일
            os.rename(log_file, f"{log_file}.zip")

    def get_caller_info(self):
        stack = inspect.stack()
        caller_frame = None
        for frame in stack[
            2:
        ]:  # 첫 두 프레임은 현재 메서드와 log 메서드이므로 건너뜁니다
            module = inspect.getmodule(frame[0])
            if (
                module and module.__name__ != __name__
            ):  # 현재 모듈이 아닌 경우를 찾습니다
                caller_frame = frame
                break

        if caller_frame:
            module = inspect.getmodule(caller_frame[0])
            module_name = module.__name__ if module else ""
            function_name = caller_frame.function

            # 클래스 이름 추출 (있는 경우)
            try:
                class_name = caller_frame[0].f_locals["self"].__class__.__name__
            except (KeyError, AttributeError):
                class_name = ""

            return module_name, function_name, class_name

        return "", "", ""

    def log(self, message):
        """
        로그 메시지를 파일에 기록합니다.
        파일 크기가 제한을 초과하면 회전합니다.
        호출한 모듈, 함수, 클래스 이름을 자동으로 포함시킵니다.
        """
        if self.handler.stream.tell() + len(message.encode("utf-8")) >= MAX_BYTE:
            self.rotate_logs()

        module_name, function_name, class_name = self.get_caller_info()

        extra = {"class.func": f"{class_name}.{function_name}"}

        self.logger.info(message, extra=extra)
        # print(f"[{module_name}] [{function_name}] [{class_name}] : {message}")


if __name__ == "__main__":
    # Logger 인스턴스 사용 예
    logger = Logger()
    logger.log("This is a test log message.")

    # 추가 테스트를 위한 함수와 클래스
    def test_function():
        logger.log("This is a log from test_function")

    class TestClass:
        def test_method(self):
            logger.log("This is a log from TestClass.test_method")

    test_function()
    TestClass().test_method()
