import os
import logging
import datetime
from functools import wraps
import pyshorteners


def logger(old_function):
    path = 'main.log'
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        logging.basicConfig(
            level=logging.INFO,
            filename=path,
            format="%(asctime)s - %(message)s"
        )
        logging.info(f"Функция: {old_function.__name__} с аргументами {args}{kwargs} и результатом {result}!")
        return result

    return new_function


def logger_1(path):

    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f'{datetime.datetime.now()} функция {old_function.__name__} с аргументами {args}{kwargs}'
                             f' и результатом {result}!\n')
            return result

        return new_function

    return __logger


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def summator(a, b=0):
        return a + b

    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'



def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_1(path)
        def summator(a, b=0):
            return a + b

        @logger_1(path)
        def div(a, b):
            return a / b

        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        div(4, 2)
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

@logger
def reduction_url(full_url):
    '''Простая библиотека API-оболочки для сокращения URL-адресов'''
    s = pyshorteners.Shortener()
    return s.tinyurl.short(full_url)



if __name__ == '__main__':
    test_1()
    test_2()
    reduction_url('https://netology.ru/profile/8079631')