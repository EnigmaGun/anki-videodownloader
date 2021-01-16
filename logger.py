import os


class Logger():

    @staticmethod
    def init(filename='log.txt'):

        LOG_PATH = os.path.dirname(os.path.abspath(__file__)) + "/logs"

        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)

        Logger.logger = open(f"{LOG_PATH}/{filename}", "w+")

    @staticmethod
    def info(message):
        Logger.logger.write(f'[INFO] {message}\n')

    @staticmethod
    def warn(message):
        Logger.logger.write(f'[WARN] {message}\n')

    @staticmethod
    def error(message):
        Logger.logger.write(f'[ERROR] {message}\n')

    @staticmethod
    def close():
        Logger.logger.close()
