import os

try:
    import evparse

except Exception as e:
    import Cython, setuptools, platform, subprocess, os, sys, time, regex, exceptdrucker,numpy,adbshellexecuter,cythoncubicspline,flatten_any_dict_iterable_or_whatsoever,nested2nested,parifinder,pandas

    iswindows = "win" in platform.platform().lower()
    if iswindows:
        addtolist = []
    else:
        addtolist = ["&"]

    olddict = os.getcwd()
    dirname = os.path.dirname(__file__)
    os.chdir(dirname)
    compile_file = os.path.join(dirname, "evparse_compile.py")
    subprocess._USE_VFORK = False
    subprocess._USE_POSIX_SPAWN = False
    subprocess.run(
        " ".join([sys.executable, compile_file, "build_ext", "--inplace"] + addtolist),
        shell=True,
        env=os.environ,
        preexec_fn=None
        if iswindows
        else os.setpgrp
        if hasattr(os, "setpgrp")
        else None,
    )
    if not iswindows:
        time.sleep(300)
    import evparse

    os.chdir(olddict)
