# -*- coding: utf-8 -*-
# @Author   : StackOF
# @Time     : 2022/2/24 
# @File     : common_utils.py
# @Project  : BatchDecompileApk
"""
Desc:
Modify:

"""
import subprocess
import time
from operator import itemgetter

import pandas as pd

from config import *
from tools.logger import init_logger

logger = init_logger(__name__)

def get_apk_list(apk_path: str):
    """

    :param apk_path:
    :return:
    """
    file_list = []
    if apk_path is None:
        raise Exception("folder_path is None")
    for dir_path, dir_names, filenames in os.walk(apk_path):
        for name in filenames:
            if os.path.splitext(name)[1] == '.apk':
                file_size = os.path.getsize(os.path.join(dir_path, name))
                file_list.append((name, os.path.join(dir_path, name), file_size))
    # name,file,size 降序
    file_lst_sorted = sorted(file_list, key=itemgetter(2), reverse=True)
    return file_lst_sorted


def exec_cmd(cmd):
    """

    :param cmd:
    :return:
    """

    if OS_TYPE == 'linux':
        cmd = path_remake(cmd)
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    stdout, stderr = res.communicate()
    if isinstance(stdout, str):
        str_stdout = stdout.encode('utf-8').decode("UTF-8")
        str_stderr = stderr.encode('utf-8').decode("UTF-8")
    else:
        try:
            str_stdout = stdout.decode("UTF-8")
            str_stderr = stderr.decode("UTF-8")
        except:
            str_stdout = stdout.decode("gb2312")
            str_stderr = stderr.decode("gb2312")
    return str_stdout, str_stderr


def path_remake(path):
    # return path.replace(' ', '\ ').replace('(','\(').replace(')','\)')
    return path.replace('(', '\(').replace(')', '\)')


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False


def get_second():
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def write_df_lst_to_xlsx(xlsx_file: str, df_lst: list, sheet_lst: list, index_int=0):
    try:
        xf = xlsx_file
        ew = pd.ExcelWriter(xlsx_file, engine='xlsxwriter')
    except Exception as e:
        logger.error("无法打开%s" % xlsx_file)
        pre, ext = os.path.splitext(xlsx_file)
        ts = get_second()
        xf = pre + '_' + ts + ext
        ew = pd.ExcelWriter(xf, engine='xlsxwriter')
    with ew as writer:
        for cur_pos in range(len(df_lst)):
            df_lst[cur_pos].to_excel(writer, sheet_name=sheet_lst[cur_pos], index=index_int, freeze_panes=(1, 0))
            column_widths = (
                df_lst[cur_pos].columns.to_series().apply(lambda x: len(x.encode('gbk')) + 5).values
            )
            writer.sheets[sheet_lst[cur_pos]].autofilter(0, 0, 0, len(df_lst[cur_pos].columns) - 1)
            for i, width in enumerate(column_widths):
                writer.sheets[sheet_lst[cur_pos]].set_column(i, i, width)
    logger.info('write the %s to %s' % (sheet_lst, xf))