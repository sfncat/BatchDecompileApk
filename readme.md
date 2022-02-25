# Batch Decompile Apk
```commandline
INSTALL
    linux:
        python3 -m venv venv
        source venv/bin/activate
        pip3 install -r requirements.txt
    windows:
        python -m venv venv
        venv\Scripts\activate.bat
        pip install -r requirements.txt
HELP
    python batch_decompile_apk.py --help
         
NAME
    batch_decompile_apk.py

SYNOPSIS
    batch_decompile_apk.py APK_PATH <flags>

POSITIONAL ARGUMENTS
    APK_PATH
        Type: str
        需要反编译的apk所在的路径

FLAGS
    --b_dc_res=B_DC_RES
        Default: True
        是否反编译资源文件，默认为True
    --b_dc_src=B_DC_SRC
        Default: True
        是否反编译代码文件，默认为True
    --b_dc_in_one_path=B_DC_IN_ONE_PATH
        Default: False
        一个apk的src和res是否放在同一个目录内，默认为False
```

```commandline
EXAMPLE
    将要反编译的apk放到test/apk目录内
    python batch_decompile_apk.py ./test/apk
    
2022-02-25 15:21:56,800 - INFO - Start decompile_by_path, the apk file path is ./test/apk

2022-02-25 15:21:56,800 - INFO - total 4 apk to decompile

2022-02-25 15:21:56,800 - INFO - cpu count is 12, pool count is 6

2022-02-25 15:22:44,918 - INFO - 2 com.sina.news.apk 48.09787321090698 s

2022-02-25 15:23:22,688 - INFO - 1 com.zhihu.android.apk 85.8682587146759 s

2022-02-25 15:23:26,358 - INFO - 3 com.tencent.mtt.apk 89.53782272338867 s

2022-02-25 15:23:30,985 - INFO - 0 com.ximalaya.ting.android.apk 94.16623640060425 s

2022-02-25 15:23:31,012 - INFO - write the ['decompile'] to /workspace/BatchDecompileApk/decompile/decompile_apk--20220225_152330_94.xlsx

2022-02-25 15:23:31,013 - INFO - Finish decompile ./test/apk, total 4 apk,run 94.18735718727112 s

2022-02-25 15:23:31,014 - INFO - decompile path is /workspace/BatchDecompileApk/decompile


```

