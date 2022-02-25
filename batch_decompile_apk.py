# -*- coding:utf-8 -*-
"""
@filename:
@Created : 2022.02.22
@author  :StackOF
@desc    :使用多进程池反编译apk文件

@modify  :
2022.02.25 优化logger打印
->
"""
import logging
import os
import sys
import time
from pathlib import Path

import pandas as pd
import fire
from pathos.multiprocessing import ProcessPool
from common_utils import *


def decompile_one_apk(pkg_name: str, local_path: str, decompile_root_path: str, seq):
    """

    :param pkg_name:
    :param local_path:
    :param decompile_root_path:
    :param seq:
    :return:
    """

    global gb_dc_src, gb_dc_res
    one_start_time = time.time()
    if gb_dc_in_one_path:
        apk_src_path = os.path.join(decompile_root_path, pkg_name, 'src')
        apk_res_path = os.path.join(decompile_root_path, pkg_name, 'res')
    else:
        apk_src_path = os.path.join(decompile_root_path, 'src', pkg_name)
        apk_res_path = os.path.join(decompile_root_path, 'res', pkg_name)

    if gb_dc_src and gb_dc_res:
        cmd = jadx_path + ' ' + local_path + ' ' + '-ds ' + apk_src_path + ' -dr ' + apk_res_path
    elif gb_dc_src:
        cmd = jadx_path + ' ' + local_path + ' -r ' + '-ds ' + apk_src_path
    elif gb_dc_res:
        cmd = jadx_path + ' ' + local_path + ' -s ' + ' -dr ' + apk_res_path
    ret, err = exec_cmd(cmd)
    if ret.find('not found') >=0:
        logger.error(ret)
    elif err.find('not found')>=0:
        logger.error(err)

    one_end_time = time.time()
    one_run_time = one_end_time - one_start_time

    logger.info(f'{seq} {pkg_name} {one_run_time} s')
    logger.debug(f'{seq} {pkg_name} {ret} {err} s')
    return [(seq, pkg_name, local_path, apk_src_path, apk_res_path, one_run_time)]


def decompile_by_pool(apk_file_lst: list, in_decompile_root_path: str):
    apk_count = len(apk_file_lst)
    apk_name_tup, apk_path_tup, apk_size_tup = zip(*apk_file_lst)
    decompile_root_path_lst = [in_decompile_root_path] * apk_count
    # pool
    cpu_count = os.cpu_count()
    pool_count = cpu_count // 2
    logger.info(f'cpu count is {cpu_count}, pool count is {pool_count}')

    start_time = time.time()
    de_pool = ProcessPool(pool_count)
    de_pool.restart()

    results = de_pool.uimap(decompile_one_apk, apk_name_tup, apk_path_tup, decompile_root_path_lst,
                            [i for i in range(apk_count)])
    de_pool.close()
    de_pool.join()

    total_result_lst = []
    for cur_result in results:
        total_result_lst += cur_result
    end_time = time.time()
    run_time = end_time - start_time
    out_df = pd.DataFrame(total_result_lst,
                          columns=['seq', 'apk_name', 'local_path', 'src_path', 'res_path', 'decompile_time'])
    return out_df, run_time


# jadx所在目录
if OS_TYPE == 'linux':
    jadx_path = os.path.join(TOOLS_PATH, 'jadx', 'bin', 'jadx')
else:
    jadx_path = os.path.join(TOOLS_PATH, 'jadx', 'bin', 'jadx.bat')
# 是否反编译代码文件，默认为True
gb_dc_src = True
# 是否反编译资源文件，默认为True
gb_dc_res = True
# 一个apk的src和res是否放在同一个目录内，默认为False
gb_dc_in_one_path = False


def decompile_by_path(apk_path:str, b_dc_res=True, b_dc_src=True, b_dc_in_one_path=False):
    """
    :param apk_path: 需要反编译的apk所在的路径
    :param b_dc_res: 是否反编译资源文件，默认为True
    :param b_dc_src: 是否反编译代码文件，默认为True
    :param b_dc_in_one_path: 一个apk的src和res是否放在同一个目录内，默认为False
    :return:
    反编译结果所在目录，为apk_path的父目录/decompile
    如果b_dc_in_one_path为False，则
        其中res所在目录为decomplie/res/{apkname}
        其中src所在目录为decomplie/src/{apkname}
    如果b_dc_in_one_path为True，则
        其中res所在目录为decomplie/{apkname}/res
        其中src所在目录为decomplie/{apkname}/src
    """
    logger.info(f'Start {decompile_by_path.__name__}, the apk file path is {apk_path}')
    global gb_dc_src, gb_dc_res, gb_dc_in_one_path
    gb_dc_src = b_dc_src
    gb_dc_res = b_dc_res
    gb_dc_in_one_path = b_dc_in_one_path
    apk_file_lst = get_apk_list(apk_path)
    logger.debug(apk_file_lst)

    decompile_root_path = os.path.join(Path(__file__).resolve().parent, 'decompile')
    src_path = os.path.join(decompile_root_path, 'src')
    res_path = os.path.join(decompile_root_path, 'res')
    mkdir(src_path)
    mkdir(res_path)
    output_path = decompile_root_path

    apk_count = len(apk_file_lst)
    logger.info(f'total {apk_count} apk to decompile')

    dc_result_df, run_time = decompile_by_pool(apk_file_lst, decompile_root_path)
    out_file = os.path.join(output_path, 'decompile_apk--' + get_second() + '_' + str(int(run_time)) + '.xlsx')
    write_df_lst_to_xlsx(out_file, [dc_result_df], ['decompile'])
    logger.info(f'Finish decompile {apk_path}, total {apk_count} apk,run {run_time} s')
    logger.info(f'decompile path is {decompile_root_path}')
    return decompile_root_path


if __name__ == "__main__":
    # 默认打印级别为INFO，可以改为DEBUG打印详细信息
    logger.setLevel(logging.INFO)

    fire.Fire(decompile_by_path)
    # for test
    # decompile_by_path(os.path.join(os.getcwd(),'test','apk'))

