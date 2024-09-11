cimport cython
cimport numpy as np
from adbshellexecuter import UniversalADBExecutor,iswindows
from cython.operator cimport dereference as deref, preincrement as inc
from cythoncubicspline import bresenham_line
from exceptdrucker import errwrite
from flatten_any_dict_iterable_or_whatsoever import fla_tu
from itertools import takewhile
from libcpp.queue cimport queue
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector
from nested2nested import nested_list_to_nested_dict
from parifinder import parse_pairs
import base64
import ctypes
import cython
import hashlib
import numpy as np
import os
import pandas as pd
import regex as re
import struct
import subprocess
import sys
import threading
import time
from libc.stdio cimport printf

configstuff=sys.modules[__name__]
cdef:
    dict tmp_cache_regexnumber={}
    dict tmp_cache_hierachyregex={}
    dict tmp_cache_finchi={}
    dict tmp_cache_stripped_strings={}
    dict tmp_cache_number_zero={}
    dict tmp_struct_dicts_temp={}
    dict tmp_cached_script_files={}
    list tmp_running_uiautomators =[]
    list tmp_running_parsing_threads=[]
    
configstuff.cache_regexnumber=tmp_cache_regexnumber
configstuff.cache_hierachyregex=tmp_cache_hierachyregex
configstuff.cache_finchi=tmp_cache_finchi
configstuff.cache_stripped_strings=tmp_cache_stripped_strings
configstuff.cache_number_zero=tmp_cache_number_zero
configstuff.struct_dicts_temp=tmp_struct_dicts_temp
configstuff.cached_script_files=tmp_cached_script_files
config_settings=sys.modules[__name__]
config_settings.running_uiautomators=tmp_running_uiautomators
config_settings.running_parsing_threads=tmp_running_parsing_threads
config_settings.debug_enabled=True
config_settings.read_events_data=True
config_settings.stop=False
np.import_array()
if iswindows:
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    kernel32 = windll.kernel32
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD

invisibledict = {}
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
re.cache_all(True)
cdef:
    object refi = re.compile(r"([^,]+),([^,]+)-([^,]+),([^,]+)", flags=re.I)
    object hierachyregex = re.compile(rb"^\s*(?:(?:View Hierarchy:)|(?:Looper))")
    str ADB_SHELL_GET_ALL_ACTIVITY_ELEMENTS = "dumpsys activity top -a -c --checkin"


def create_temp_memdisk(
    str memdisk_path="/media/ramdisk",
    object adb_path=None,
    object device_serial=None,
    str memdisk_size="128M",
    bint shell=False,
    str su_exe="su",
    **kwargs,
):
    cdef:
        str remountcmd
    remountcmd = (
        R"""
    SUEXEFILE
    check_if_mounted() {
        mountcheckervalue=0
        mountchecker="$(mount -v | grep -v 'rw' | grep 'ro' | awk 'BEGIN{FS="[\\(]+";}{print $2}' | awk 'BEGIN{FS="[\\),]+";}{if ($1 ~ /^ro$/){ print 1;exit}}')"
        echo -e "$mountchecker"
        mountcheckervalue=$((mountcheckervalue + mountchecker))
        return "$mountcheckervalue"
    }

    modr() {

        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat1
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount --all -o remount,rw -t ext4
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o remount,rw
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o remount,rw /;
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o rw&&remount /
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o rw;remount /
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat
        else
            return 0
        fi
        if ! check_if_mounted; then
            getprop --help >/dev/null;su -c 'mount -o remount,rw /;'
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount -o remount,rw /;
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -v | grep "^/" | grep -v '\\(rw,' | grep '\\(ro' | awk '{print "mount -o rw,remount " $1 " " $3}' | tr '\n' '\0' | xargs -0 -n1 su -c
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -v | grep "^/" | grep -v '\\(rw,' | grep '\\(ro' | awk '{print "mount -o rw,remount " $1 " " $3}' | su -c sh
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -v | grep "^/" | grep -v '\\(rw,' | grep '\\(ro' | awk '{system("mount -o rw,remount " $1 " " $3)}'
        else
            return 0
        fi

        if ! check_if_mounted; then
            su -c 'mount -v | grep -E "^/" | awk '\''{print "mount -o rw,remount " $1 " " $3}'\''' | tr '\n' '\0' | xargs -0 -n1 su -c
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -Ev | grep -Ev 'nodev' | grep -Ev '/proc' | grep -v '\\(rw,' | awk 'BEGIN{FS="([[:space:]]+(on|type)[[:space:]]+)|([[:space:]]+\\()"}{print "mount -o rw,remount " $1 " " $2}' | xargs -n5 | su -c
        else
            return 0
        fi

        if ! check_if_mounted; then
            su -c 'mount -v | grep -E "^/" | awk '\''{print "mount -o rw,remount " $1 " " $3}'\''' | sh su -c
        else
            return 0
        fi

        if ! check_if_mounted; then
            getprop --help >/dev/null;su -c 'mount -v | grep -E "^/" | awk '\''{print "mount -o rw,remount " $1 " " $3}'\''' | tr '\n' '\0' | xargs -0 -n1 | su -c sh
        else
            return 0
        fi
    return 1
    }
    if [ ! -e "MYMEMDISKPATH" ]; then
        if ! modr 2>/dev/null; then
            echo -e "FALSEFALSEFALSE"
        else
            echo -e "TRUETRUETRUE"
        fi
        mkdir -p MYMEMDISKPATH
        mount -t tmpfs -o size=SIZEOFMYMEMDISK tmpfs MYMEMDISKPATH
    fi

    """.replace("MYMEMDISKPATH", memdisk_path)
        .replace("SUEXEFILE", su_exe)
        .replace("SIZEOFMYMEMDISK", str(memdisk_size))
    )
    try:
        adbsh = UniversalADBExecutor(
            adb_path=adb_path, device_serial=device_serial, **kwargs
        )
        return adbsh.shell_without_capturing_stdout_and_stderr(
            command=remountcmd,
            debug=False,
            ignore_exceptions=True,
            shell=shell,
        )
    except Exception:
        if config_settings.debug_enabled:
            errwrite()



cpdef clean_cache():
    configstuff.cache_regexnumber.clear()
    configstuff.cache_hierachyregex.clear()
    configstuff.cache_finchi.clear()
    configstuff.cache_stripped_strings.clear()
    configstuff.cache_number_zero.clear()
    configstuff.struct_dicts_temp.clear()
    configstuff.cached_script_files.clear()

cdef class subi(dict):
    """
    A subclass of dict that automatically creates nested dictionaries for missing keys.
    """
    def __missing__(self, k):
        self[k] = self.__class__()
        return self[k]

cdef list list_split(list l, list indices_or_sections):
    """
    Splits a list into sublists based on the provided indices or sections.

    Parameters:
    l (list): The list to split.
    indices_or_sections (list): The indices or sections to split the list.

    Returns:
    list: A list of sublists.
    """
    cdef:
        Py_ssize_t Ntotal = len(l)
        Py_ssize_t Nsections = len(indices_or_sections) + 1
        Py_ssize_t i
        list[Py_ssize_t] div_points
        list sub_arys
    div_points = [0, *indices_or_sections, Ntotal]
    sub_arys = []
    for i in range(Nsections):
        if div_points[i] >= Ntotal:
            break
        sub_arys.append(l[div_points[i]:div_points[i + 1]])
    return sub_arys


cpdef strstrip(x):
    return configstuff.cache_stripped_strings.setdefault(x,x.strip())


cpdef iszero(Py_ssize_t o):
    return configstuff.cache_number_zero.setdefault(o,o == 0)

def indent2dict(data, removespaces):
    """
    Converts indented text data into a nested dictionary.

    Parameters:
    data (str or list): The indented text data.
    removespaces (bool): Whether to remove spaces from the keys.

    Returns:
    dict: The nested dictionary.
    """
    def convert_to_normal_dict_simple(di):
        globcounter = 0

        def _convert_to_normal_dict_simple(di):
            nonlocal globcounter
            globcounter = globcounter + 1
            if not di:
                return globcounter
            if isinstance(di, subi):
                di = {k: _convert_to_normal_dict_simple(v) for k, v in di.items()}
            return di

        return _convert_to_normal_dict_simple(di)

    def splitfunc(alli, dh):
        def splifu(lix, ind):
            try:
                firstsplit = [n for n, y in enumerate(lix) if y and y[0] == ind]
            except Exception:
                return lix
            result1 = list_split(l=lix, indices_or_sections=firstsplit)
            newi = ind + 1
            splitted = []
            for l in result1:
                if newi < (lendh):
                    if isinstance(l, list):
                        if l:
                            la = splifu(l, newi)
                            splitted.append(la)
                    else:
                        splitted.append(l)
                else:
                    splitted.append(l)
            return splitted

        lendh = len(dh.keys())
        alli2 = [alli[0]] + alli
        return splifu(alli2, ind=0)

    if isinstance(data, (str, bytes)):
        da2 = data.splitlines()
    else:
        da2 = list(data)
    d = {}
    dox = da2.copy()
    dox = [x for x in dox if x.strip()]
    for dx in dox:
        eg = len(dx) - len(dx.lstrip())
        d.setdefault(eg, []).append(dx)
    dh = {k: v[1] for k, v in enumerate(sorted(d.items()))}
    alli = []
    for xas in dox:
        for kx, kv in dh.items():
            if xas in kv:
                alli.append([kx, xas])
                break

    iu = splitfunc(alli, dh)
    allra = []
    d = nested_list_to_nested_dict(l=iu)
    lookupdi = {}
    for iasd, ius in enumerate((q for q in fla_tu(d) if not isinstance(q[0], int))):
        if iasd == 0:
            continue
        it = list(takewhile(iszero, reversed(ius[1][: len(ius[1]) - 2])))
        iuslen = len(ius[1])
        it = ius[1][: iuslen - 2 - len(it)]
        allra.append([it, ius[0]])
        lookupdi[it] = ius[0]

    allmils = []
    for allraindex in range(len(allra)):
        im = allra[allraindex][0]
        mili = []
        for x in reversed(range(1, len(im) + 1)):
            mili.append(lookupdi[im[:x]])
        mili = tuple(reversed(mili))
        allmils.append(mili)
    allmilssorted = sorted(allmils, key=len, reverse=True)
    countdict = {}
    difi = subi()
    allmilssorted = [
        tuple(map(strstrip, x) if removespaces else x) for x in allmilssorted
    ]
    ixas_range = len(allmilssorted)
    for ixas_index in range(ixas_range):
        for rad in range(len(allmilssorted[ixas_index]) + 1):
            ixasrad = allmilssorted[ixas_index][:rad]
            if ixasrad not in countdict:
                countdict[ixasrad] = 0
            countdict[ixasrad] += 1
    for key, item in countdict.items():
        if item != 1:
            continue
        vaxu = difi[key[0]]
        for inxa in range(len(key)):
            if inxa == 0:
                continue
            vaxu = vaxu[key[inxa]]
    difi2 = convert_to_normal_dict_simple(difi)
    return difi2


def execute_sh_command(
    command,
    serial="",
    adb_path="",
    subproc_shell=True,
):
    """
    Executes a shell command on an Android device using adb.

    Parameters:
    command (str): The shell command to execute.
    serial (str): The serial number of the device (default "").
    adb_path (str): The path to the adb executable (default "").
    subproc_shell (bool): Whether to use the shell in the subprocess (default True).

    Returns:
    list: The output lines of the command.
    """
    adbsh=UniversalADBExecutor(adb_path=adb_path,device_serial=serial)
    stdout, stderr, returncode = (
        adbsh.shell_with_capturing_import_stdout_and_stderr(
            command=command,
            shell=subproc_shell,
            debug=False,
            ignore_exceptions=True,
        )
    )
    try:
        return stdout.strip().splitlines()
    except Exception:
        if config_settings.debug_enabled:
            errwrite()
        return []

cpdef lenq(tuple q):
    """
    Returns the length of the first element in the tuple.

    Parameters:
    q (tuple): The tuple to get the length of the first element.

    Returns:
    int: The length of the first element.
    """
    if q:
        return len(q[0])
    return 0
    


cpdef get_regex_numbers(datadict_coords):
    if datadict_coords in configstuff.cache_regexnumber:
        return configstuff.cache_regexnumber[datadict_coords]

    regexresults = refi.findall(datadict_coords)
    resi=(0, 0, 0, 0)
    if regexresults:
        try:
            resi=tuple(
                map(int, (regexresults[0]))
            )
        except Exception:
            pass
    configstuff.cache_regexnumber[datadict_coords]=resi
    return resi

cpdef dict findchi(str ff):
    """
    Finds and parses key-value pairs from a string using a specific format.

    Parameters:
    ff (str): The input string.

    Returns:
    dict: A dictionary containing the parsed key-value pairs.
    """
    cdef:
        dict r0, datadict
        list maininfostmp
        Py_ssize_t maininfos_last_index, last_index_text, infosplitlen_last_index
        list otherdata, infosplit
        str firstimesearch, secondtimesearch, t,orgstri
    try:
        if ff in configstuff.cache_finchi:
            return configstuff.cache_finchi[ff]
        r0 = parse_pairs(string=ff, s1="{", s2="}", str_regex=False)
        if not r0:
            return {}
        datadict = {}
        maininfostmp = list(
            {k: v for k, v in sorted(r0.items(), key=lenq, reverse=True)}.items()
        )
        if not maininfostmp:
            return {}
        maininfos = maininfostmp[0]

        maininfos_last_index = len(maininfos) - 1
        last_index_text = len(maininfos[maininfos_last_index]["text"]) - 1
        otherdata = ff.split(maininfos[maininfos_last_index]["text"])
        orgstri=maininfos[maininfos_last_index]["text"][1 : last_index_text]
        t = (
            orgstri
            + " ÇÇÇÇÇÇ ÇÇÇÇÇÇ"
        )
        infosplit = t.split(maxsplit=5)
        firstimesearch = infosplit[1]
        secondtimesearch = infosplit[2]
        datadict={
            "START_X":-1,
            "START_Y":-1,
            "CENTER_X":-1,
            "CENTER_Y":-1,
            "AREA":-1,
            "END_X":-1,
            "END_Y":-1,
            "WIDTH":-1,
            "HEIGHT":-1,
            "START_X_RELATIVE":-1,
            "START_Y_RELATIVE":-1,
            "END_X_RELATIVE":-1,
            "END_Y_RELATIVE":-1,
            "COORDS":None,
            "INT_COORDS":(0, 0, 0, 0),
            "CLASSNAME":None,
            "HASHCODE":None,
            "ELEMENT_ID":None,
            "MID":None,
            "VISIBILITY":None,
            "FOCUSABLE":None,
            "ENABLED":None,
            "DRAWN":None,
            "SCROLLBARS_HORIZONTAL":None,
            "SCROLLBARS_VERTICAL":None,
            "CLICKABLE":None,
            "LONG_CLICKABLE":None,
            "CONTEXT_CLICKABLE":None,
            "PFLAG_IS_ROOT_NAMESPACE":None,
            "PFLAG_FOCUSED":None,
            "PFLAG_SELECTED":None,
            "PFLAG_PREPRESSED":None,
            "PFLAG_HOVERED":None,
            "PFLAG_ACTIVATED":None,
            "PFLAG_INVALIDATED":None,
            "PFLAG_DIRTY_MASK":None,
            "ORIGINAL_STRING":orgstri,
        }
        infosplitlen_last_index = len(infosplit)

        try:
            if infosplitlen_last_index >= 3:
                datadict["COORDS"] = infosplit[infosplitlen_last_index - 3].rstrip("Ç ")
        except Exception:
            pass
        try:
            datadict["INT_COORDS"] = get_regex_numbers(datadict["COORDS"])
        except Exception:
            pass
        try:
            if otherdata:
                datadict["CLASSNAME"] = otherdata[0]
        except Exception:
            pass
        try:
            if infosplitlen_last_index >= 2:
                datadict["HASHCODE"] = infosplit[infosplitlen_last_index - 2].rstrip("Ç ")
        except Exception:
            pass
        try:
            if infosplitlen_last_index >= 1:
                datadict["ELEMENT_ID"] = infosplit[infosplitlen_last_index-1].rstrip("Ç ")
        except Exception:
            pass
        try:
            if infosplit:
                datadict["MID"] = infosplit[0]
        except Exception:
            pass
        maxindexf1 = len(firstimesearch) - 1
        try:
            if maxindexf1 > 0:
                datadict["VISIBILITY"] = firstimesearch[0]
        except Exception:
            pass

        try:
            if maxindexf1 > 1:
                datadict["FOCUSABLE"] = firstimesearch[1]
        except Exception:
            pass

        try:
            if maxindexf1 > 2:
                datadict["ENABLED"] = firstimesearch[2]
        except Exception:
            pass

        try:
            if maxindexf1 > 3:
                datadict["DRAWN"] = firstimesearch[3]
        except Exception:
            pass

        try:
            if maxindexf1 > 4:
                datadict["SCROLLBARS_HORIZONTAL"] = firstimesearch[4]

        except Exception:
                pass
        try:
            if maxindexf1 > 5:
                datadict["SCROLLBARS_VERTICAL"] = firstimesearch[5]

        except Exception:
                pass
        try:
            if maxindexf1 > 6:
                datadict["CLICKABLE"] = firstimesearch[6]

        except Exception:
                pass
        try:
            if maxindexf1 > 7:
                datadict["LONG_CLICKABLE"] = firstimesearch[7]

        except Exception:
                pass
        try:
            if maxindexf1 >= 8:
                datadict["CONTEXT_CLICKABLE"] = firstimesearch[8]

        except Exception:
                pass

        maxindexf2 = len(secondtimesearch) - 1
        try:
            if maxindexf2 > 0:
                datadict["PFLAG_IS_ROOT_NAMESPACE"] = secondtimesearch[0]

        except Exception:
                pass
        try:
            if maxindexf2 > 1:
                datadict["PFLAG_FOCUSED"] = secondtimesearch[1]

        except Exception:
                pass
        try:
            if maxindexf2 > 2:
                datadict["PFLAG_SELECTED"] = secondtimesearch[2]

        except Exception:
                pass
        try:
            if maxindexf2 > 3:
                datadict["PFLAG_PREPRESSED"] = secondtimesearch[3]

        except Exception:
                pass
        try:
            if maxindexf2 > 4:
                datadict["PFLAG_HOVERED"] = secondtimesearch[4]

        except Exception:
                pass
        try:
            if maxindexf2 > 5:
                datadict["PFLAG_ACTIVATED"] = secondtimesearch[5]

        except Exception:
                pass
        try:
            if maxindexf2 > 6:
                datadict["PFLAG_INVALIDATED"] = secondtimesearch[6]

        except Exception:
                pass
        try:
            if maxindexf2 >= 7:
                datadict["PFLAG_DIRTY_MASK"] = secondtimesearch[7]

        except Exception:
                pass

        configstuff.cache_finchi[ff]=datadict
        return datadict
    except Exception:
        configstuff.cache_finchi[ff]={}
        return {}


def regex_check(s):
    """
    Checks if a string matches a specific regex pattern.

    Parameters:
    s (str): The string to check.

    Returns:
    bool: True if the string matches the pattern, False otherwise.
    """
    if s in configstuff.cache_hierachyregex:
        return configstuff.cache_hierachyregex[s]

    if hierachyregex.search(s):
        configstuff.cache_hierachyregex[s]=True
    else:
        configstuff.cache_hierachyregex[s]=False
    return configstuff.cache_hierachyregex[s]

def get_all_activity_elements(str serial="", str adb_path="", Py_ssize_t number_of_max_views=-1, cython.bint subproc_shell=True):
    """
    Retrieves all activity elements from an Android device using adb.

    Parameters:
    serial (str): The serial number of the device (default "").
    adb_path (str): The path to the adb executable (default "").
    number_of_max_views (Py_ssize_t): The maximum number of views to retrieve (default -1).
    subproc_shell (cython.bint): Whether to use the shell in the subprocess (default True).

    Returns:
    list: A list of all activity elements.
    """
    cdef:
        dict datadict
        dict cachedict = {}
        list list2split = []
        list allda, allsplits, allsi
        cython.bytes hierachybytes = b"View Hierarchy:"
        Py_ssize_t indi1, indi2, len_allsplits, elemtindex, hierachcounter, hierachcounter2, ffindex, last_index_allchildrendata, last_index_item
        dict di
        list[list] allchildrendata
        list[list[list]] allconvdata
    try:
        allda = execute_sh_command(
            ADB_SHELL_GET_ALL_ACTIVITY_ELEMENTS,
            serial,
            adb_path,
            subproc_shell
        )
    except Exception:
        allda = []
    lenallda = len(allda)
    for indi1 in range(lenallda):
        if regex_check(allda[indi1]):
            list2split.append(indi1)
    allsi = list_split(
        allda,
        list2split,
    )
    allsplits = []
    for indi2 in range(len(allsi)):
        if allsi[indi2]:
            if hierachybytes in allsi[indi2][0]:
                allsplits.append(allsi[indi2])
    len_allsplits = len(allsplits)
    if number_of_max_views > 0:
        if len_allsplits - number_of_max_views < 0:
            raise IndexError('Out of bounds')
        allsplits = allsplits[len_allsplits - number_of_max_views:]

    len_allsplits = len(allsplits)
    allconvdata = []
    for elemtindex in range(len_allsplits):
        try:
            di = indent2dict(
                b"\n".join(allsplits[elemtindex]).decode("utf-8", "ignore"), removespaces=True
            )
        except Exception:
            di = {}
        if not di:
            continue
        allchildrendata = []
        hierachcounter = 0
        for f in fla_tu(di):
            allchildrendata.append([])

            hierachcounter += 1
            hierachcounter2 = 0
            for ffindex in range(len(f[1])):
                try:
                    try:
                        datadict = {kx: vx for kx, vx in cachedict.setdefault(f[1][ffindex], findchi(f[1][ffindex])).items()}
                        if not datadict:
                            continue
                    except Exception:
                        continue
                    last_index_allchildrendata = len(allchildrendata) - 1
                    allchildrendata[last_index_allchildrendata].append(datadict)
                    datadict["START_X"] = sum(
                        [
                            x["INT_COORDS"][0]
                            for x in allchildrendata[last_index_allchildrendata]
                        ]
                    )
                    datadict["START_Y"] = sum(
                        [
                            x["INT_COORDS"][1]
                            for x in allchildrendata[last_index_allchildrendata]
                        ]
                    )
                    datadict["WIDTH"] = (
                        datadict["INT_COORDS"][2] - datadict["INT_COORDS"][0]
                    )
                    datadict["HEIGHT"] = (
                        datadict["INT_COORDS"][3] - datadict["INT_COORDS"][1]
                    )

                    datadict["END_X"] = datadict["START_X"] + datadict["WIDTH"]
                    datadict["END_Y"] = datadict["START_Y"] + datadict["HEIGHT"]
                    datadict["CENTER_X"] = datadict["START_X"] + (
                        datadict["WIDTH"] // 2
                    )
                    datadict["CENTER_Y"] = datadict["START_Y"] + (
                        datadict["HEIGHT"] // 2
                    )

                    datadict["AREA"] = (datadict["HEIGHT"] * datadict["WIDTH"])

                    datadict["START_X_RELATIVE"] = datadict["INT_COORDS"][0]
                    datadict["START_Y_RELATIVE"] = datadict["INT_COORDS"][1]
                    datadict["END_X_RELATIVE"] = datadict["INT_COORDS"][2]
                    datadict["END_Y_RELATIVE"] = datadict["INT_COORDS"][3]
                    datadict["IS_PARENT"] = True
                    datadict["VIEW_INDEX"] = elemtindex
                    datadict["HIERACHY_CLUSTER"] = hierachcounter
                    datadict["HIERACHY_SINGLE"] = hierachcounter2
                    hierachcounter2 = hierachcounter2 + 1

                except Exception:
                    continue

        try:
            last_index_allchildrendata = len(allchildrendata) - 1
            last_index_item = len(allchildrendata[last_index_allchildrendata]) - 1
            allchildrendata[last_index_allchildrendata][last_index_item][
                "IS_PARENT"
            ] = False
            allconvdata.append([list(x) for x in allchildrendata])

        except Exception:
            pass
    return allconvdata

cpdef tuple[dict[cython.ulonglong,set],dict[cython.ulonglong,set[tuple]]] parse_children(
    cython.Py_ssize_t[:] HIERACHY_SINGLE,
    cython.Py_ssize_t[:] HIERACHY_CLUSTER,
    cython.ulonglong[:] ORIGINAL_STR_ID,
    dict mapping_dict):
    cdef:
        dict parentsdict
        dict[cython.ulonglong,set] all_my_children_together
        dict[cython.ulonglong,set[tuple]] all_my_children

        Py_ssize_t hierachyindex1, hierachyindex2
    parentsdict = {}
    for hierachyindex1 in range(len(HIERACHY_SINGLE)):
        if ORIGINAL_STR_ID[hierachyindex1] not in parentsdict:
            parentsdict[ORIGINAL_STR_ID[hierachyindex1]] = {}
        for hierachyindex2 in range(len(HIERACHY_SINGLE)):
            if hierachyindex2 <= hierachyindex1:
                continue
            if HIERACHY_CLUSTER[hierachyindex1] < HIERACHY_CLUSTER[hierachyindex2]:
                break

            if HIERACHY_SINGLE[hierachyindex2] > HIERACHY_SINGLE[hierachyindex1]:
                if HIERACHY_CLUSTER[hierachyindex2] not in parentsdict[ORIGINAL_STR_ID[hierachyindex1]]:
                    parentsdict[ORIGINAL_STR_ID[hierachyindex1]][HIERACHY_CLUSTER[hierachyindex2]] = {
                        HIERACHY_SINGLE[hierachyindex2]: {}
                    }
                parentsdict[ORIGINAL_STR_ID[hierachyindex1]][HIERACHY_CLUSTER[hierachyindex2]][
                    HIERACHY_SINGLE[hierachyindex2]
                ] = mapping_dict[ORIGINAL_STR_ID[hierachyindex2]]

    all_my_children_together = {}
    all_my_children = {}

    for parent, childrengroup in parentsdict.items():
        for childrendictx in childrengroup.values():
            if parent not in all_my_children:
                all_my_children[parent] = set()
            all_my_children[parent].add(tuple(childrendictx.values()))

            if parent not in all_my_children_together:
                all_my_children_together[parent] = set()
            all_my_children_together[parent].update((childrendictx.values()))
    return all_my_children_together,all_my_children

def parse_fragments_active_screen(
    object serial="",
    object adb_path="",
    Py_ssize_t number_of_max_views=1,
    Py_ssize_t screen_width=720,
    Py_ssize_t screen_height=1280,
    bint subproc_shell=False,
    bint with_children=False,
    bint add_screenshot=False,
    object screenshot_kwargs=None,
    bint add_input_tap=True,
    object input_tap_center_x="aa_center_x",
    object input_tap_center_y="aa_center_y",
    str input_tap_input_cmd='input touchscreen tap',
    object input_tap_kwargs=None,
    str sendevent_mouse_move_start_x="aa_start_x",
    str sendevent_mouse_move_start_y="aa_start_y",
    str sendevent_mouse_move_end_x="aa_end_x",
    str sendevent_mouse_move_end_y="aa_end_y",
    Py_ssize_t sendevent_mouse_move_y_max=65535,
    Py_ssize_t sendevent_mouse_move_x_max=65535,
    str sendevent_mouse_move_inputdev="/dev/input/event5",
    bint sendevent_mouse_move_add=True,
    object sendevent_mouse_move_kwargs=None,
    str sendevent_mouse_move_su_exe='su',
    str sendevent_mouse_move_sh_device='sh',
    str sendevent_mouse_move_cwd_on_device='/sdcard',
    Py_ssize_t sendevent_mouse_move_qty_blocks=12 * 24,
    bint debug=True,
):
    """
    Parses the active screen fragments from an Android device and returns them as a DataFrame.

    Parameters:
    serial (str): The serial number of the device (default "").
    adb_path (str): The path to the adb executable (default "").
    number_of_max_views (int): The number of maximum views to retrieve (default 1).
    screen_width (int): The width of the screen (default 720).
    screen_height (int): The height of the screen (default 1280).
    subproc_shell (bool): Whether to use the shell in the subprocess (default False).

    Returns:
    pd.DataFrame: The parsed screen fragments as a DataFrame.
    """
    cdef:
        list dframelist,last_element_list
        Py_ssize_t l1, l2, exax
    config_settings.debug_enabled = debug
    if not sendevent_mouse_move_kwargs:
        sendevent_mouse_move_kwargs={}
    if not input_tap_kwargs:
        input_tap_kwargs={}
    if not screenshot_kwargs:
        screenshot_kwargs={}
    if not serial:
        serial=""
    if not adb_path:
        adb_path=""
    screen_area = float(screen_width) * float(screen_height)
    d = get_all_activity_elements(
        serial, adb_path, number_of_max_views, subproc_shell
    )
    if not d:
        return pd.DataFrame()
    dframelist = []
    for l1 in range(len(d)):
        e = d[l1]
        for l2 in range(len(e)):
            ee = e[l2]
            last_element_list = []
            for exax in range(len(ee) - 1):
                last_element_list.append(False)
            last_element_list.append(True)
            try:
                for ele in range(len(last_element_list)):
                    ee[ele]['IS_LAST']=last_element_list[ele]
                    dframelist.append(ee[ele])
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()


    try:
        df = pd.DataFrame(dframelist, dtype='object')
        df=df.assign(AREA_PERCENTAGE=((df.AREA.astype("Float64") / screen_area) * 100.0).astype("Float64"))
        df.loc[:, "ORIGINAL_STR_ID"] = df.ORIGINAL_STRING.apply(id)
        df.loc[:, "ORIGINAL_STR_ID"] = (
            df["ORIGINAL_STR_ID"] + df.END_X + df.END_Y + df.WIDTH + df.HEIGHT
        ).astype(np.uint64)
        df.HIERACHY_CLUSTER = df.HIERACHY_CLUSTER.astype(np.int64)
        df.HIERACHY_SINGLE = df.HIERACHY_SINGLE.astype(np.int64)
        HIERACHY_CLUSTER = df.HIERACHY_CLUSTER.__array__().astype(np.int64)
        HIERACHY_SINGLE = df.HIERACHY_SINGLE.__array__().astype(np.int64)
        ORIGINAL_STR_ID = df.ORIGINAL_STR_ID.__array__().astype(np.uint64)
        dfn = df.drop_duplicates(subset=["ORIGINAL_STR_ID"]).reset_index(drop=True)
        dfn.loc[:,"REAL_INDEX"] = dfn.index.__array__().copy()
        if with_children:
            dfn.index = dfn.ORIGINAL_STR_ID.__array__().copy()
            mapping_dict = dfn.REAL_INDEX.to_dict()
            all_my_children_together,all_my_children=parse_children(HIERACHY_SINGLE,HIERACHY_CLUSTER,ORIGINAL_STR_ID,mapping_dict)
            dfn.loc[:,"ALL_MY_CHILDREN"] = dfn["ORIGINAL_STR_ID"].apply(lambda _: ())
            dfn.loc[all_my_children_together.keys(), "ALL_MY_CHILDREN"] = dfn.loc[
                all_my_children_together.keys()
            ].apply(lambda q: tuple(sorted(all_my_children_together[q.name])), axis=1)
            dfn.loc[:,"ALL_MY_CHILDREN_GROUPED"] = dfn["ORIGINAL_STR_ID"].apply(lambda _: ())
            dfn.loc[all_my_children.keys(), "ALL_MY_CHILDREN_GROUPED"] = dfn.loc[
                all_my_children.keys()
            ].apply(lambda q: tuple(all_my_children[q.name]), axis=1)
            dfn.index = dfn["REAL_INDEX"].__array__().copy()
        df2=dfn.drop(
            columns=[q for q in [
                "IS_PARENT",
                "VIEW_INDEX",
                "HIERACHY_CLUSTER",
                "HIERACHY_SINGLE",
                "IS_LAST",
                "ORIGINAL_STR_ID",

            ] if q in dfn.columns],inplace=False
        ).reset_index(drop=True)
        df2.columns = [
            ("aa_{}".format(df2.columns[i])).lower() for i in range(len(df2.columns))
        ]
        if add_screenshot:
            try:
                npimi=get_screenshot_as_bgra(screen_height=screen_height,screen_width=screen_width,adb_path=adb_path,device_serial=serial,**screenshot_kwargs)
                df2.loc[:, "aa_screenshot"] = df2.apply(lambda item: cropimage(
                    img=npimi,
                    coords=(
                        item.aa_start_x,
                        item.aa_start_y,
                        item.aa_end_x,
                        item.aa_end_y,
                    ),
                ),axis=1)
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()

        if add_input_tap:
            try:
                df2.loc[:, "aa_input_tap"] = df2.apply(
                    lambda q: InputTap(
                        fu=subprocess_input_tap,
                        x=q[input_tap_center_x],
                        y=q[input_tap_center_y],
                        input_cmd=input_tap_input_cmd,
                        adb_path=adb_path,
                        device_serial=serial,
                        debug=debug,
                        **input_tap_kwargs

                    ),
                    axis=1,
                )
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()

        if sendevent_mouse_move_add:
            try:
                df2.loc[:, "aa_mouse_move"] = df2.apply(
                    lambda q: SendEventMouseMove(
                        fu=subprocess_input_sendevent,
                        startx=q[sendevent_mouse_move_start_x],
                        starty=q[sendevent_mouse_move_start_y],
                        endx=  q[sendevent_mouse_move_end_x],
                        endy=  q[sendevent_mouse_move_end_y],
                        screen_height=screen_height,
                        screen_width=screen_width,
                        y_max=sendevent_mouse_move_y_max,
                        x_max=sendevent_mouse_move_x_max,
                        su_exe=sendevent_mouse_move_su_exe,
                        sh_device=sendevent_mouse_move_sh_device,
                        inputdev=sendevent_mouse_move_inputdev,
                        cwd_on_device=sendevent_mouse_move_cwd_on_device,
                        adb_path=adb_path,
                        device_serial=serial,
                        qty_blocks=sendevent_mouse_move_qty_blocks,
                        echo_or_printf=b'printf "%b"',
                        debug=debug,
                        **sendevent_mouse_move_kwargs,
                    ),
                    axis=1,
                )
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()
        return df2
    except Exception:
        if config_settings.debug_enabled:
            errwrite()
        return pd.DataFrame()

def cropimage(object img, tuple coords):
    try:
        return img[coords[1] if coords[1]>0 else 0 : coords[3] if coords[3]>0 else 0, coords[0] if coords[0]>0 else 0 : coords[2] if coords[2]>0 else 0]
    except Exception:
        return pd.NA

def get_screenshot_as_bgra(screen_height,screen_width,adb_path,device_serial,**kwargs):
    adbsh = UniversalADBExecutor(
                adb_path=adb_path,
                device_serial=device_serial,**kwargs
            )

    stdout, stderr, returncode = (
        adbsh.shell_with_capturing_import_stdout_and_stderr(
            command="screencap",
            debug=False,
            ignore_exceptions=True,
        )
    )
    if iswindows:
        stdouts = stdout.replace(b"\r\n", b"\n")
    else:
        stdouts = stdout
    return np.frombuffer(stdouts,offset=16, dtype=np.uint8).reshape(
        (screen_height, screen_width, 4)
    )[..., [2, 1, 0, 3]]


class InputTap:
    __slots__ = ("fu",
        "x",
        "y",
        "kwargs",
        "adb_path",
        "device_serial",
        "input_cmd",
        "debug",)

    def __init__(self, fu, x, y, input_cmd='input touchscreen tap',adb_path=None, device_serial=None, debug=True, **kwargs):
        self.fu = fu
        self.x = x
        self.y = y
        self.kwargs = kwargs
        self.adb_path=adb_path
        self.device_serial=device_serial
        self.input_cmd=input_cmd
        self.debug=debug

    def __call__(self, offset_x=0, offset_y=0, **kwargs):
        try:
            return self.fu(
                x=int(self.x + offset_x), y=int(self.y + offset_y),input_cmd=self.input_cmd,adb_path=self.adb_path,device_serial=self.device_serial, **{**self.kwargs, **kwargs}
            )
        except Exception:
            if config_settings.debug_enabled:
                errwrite()


    def __str__(self):
        return f"{self.x}, {self.y}"

    def __repr__(self):
        return self.__str__()

def subprocess_input_tap(x, y, input_cmd='input touchscreen tap', adb_path=None, device_serial=None, **kwargs):
    adbsh = UniversalADBExecutor(adb_path=adb_path, device_serial=device_serial, **kwargs)
    return adbsh.shell_with_capturing_import_stdout_and_stderr(
        command=f"{input_cmd} {int(x)} {int(y)}",
        debug=False,
        ignore_exceptions=True,
    )



def create_numpy_struct_data_byte_array(i, FORMAT):
    return np.frombuffer(
        np.fromiter(
            i,
            dtype=np.dtype(
                [(str(q[0]), str(q[1])) for q in enumerate(FORMAT)],
                align=True,
            ),
        ).tobytes(),
        dtype="V"+str(configstuff.struct_dicts_temp.setdefault(
        FORMAT, (struct.calcsize(FORMAT))
    )))
def create_numpy_struct_data_bytes(i, FORMAT,sep=b'\n'):
    return sep.join(create_numpy_struct_data_byte_array(i, FORMAT))

def create_struct_mouse_move_commands(
    list[tuple] allcoords,
    Py_ssize_t y_max,
    Py_ssize_t x_max,
    Py_ssize_t screen_height,
    Py_ssize_t screen_width,
    str inputdev="/dev/input/event3",
    str FORMAT="llHHI" * 3,
    str path_on_device="/sdcard/neu.bin",
    Py_ssize_t qty_blocks=6,
    str exec_or_eval="exec",
    Py_ssize_t sleepbetweencommand=0,
    bint debug=True,
):
    cdef:
        long tstamp = int(time.time())
        Py_ssize_t lendata,blocksize,numberofloops
        Py_ssize_t len_allcoords=len(allcoords)
        bytes binary_data
        str ddscript
    chunk_size= configstuff.struct_dicts_temp.setdefault(
        FORMAT, (struct.calcsize(FORMAT))
    )

    binary_data = create_numpy_struct_data_bytes(
                    i=((
                        tstamp,
                        363320,
                        3,
                        0,
                        int(allcoords[x_y_index][0] * x_max / screen_width),
                        tstamp,
                        363321,
                        3,
                        1,
                        int(allcoords[x_y_index][1] * y_max / screen_height),
                        tstamp,
                        363322,
                        0,
                        0,
                        0,
                    )
                    for x_y_index in range(len_allcoords))
                , FORMAT=FORMAT,sep=b'\n')
    lendata = len(binary_data)
    blocksize = (chunk_size) * qty_blocks
    numberofloops = (lendata // blocksize) + 1

    ddscript = _write_data_using_dd(
        path_on_device=path_on_device,
        lendata=len(binary_data),
        numberofloops=numberofloops,
        inputdev=inputdev,
        blocksize=blocksize,
        sleepbetweencommand=sleepbetweencommand,
        exec_or_eval=exec_or_eval,
    )
    return ddscript, binary_data


cpdef str _write_data_using_dd(
    str path_on_device,
    Py_ssize_t lendata,
    Py_ssize_t numberofloops,
    str inputdev="/dev/input/event3",
    Py_ssize_t blocksize=72,
    object sleepbetweencommand=0,
    str exec_or_eval="exec",
):
    if sleepbetweencommand > 0:
        sleepbetweencommand = f"sleep {sleepbetweencommand}"
    else:
        sleepbetweencommand = ""
    if exec_or_eval == "eval":
        quotes = '"'
        commandline = f"eval {quotes}dd status=none conv=sync count=1 skip=$skiphowmany bs=$blocksize if=$inputfile of=$outdevice{quotes}"
    else:
        commandline = 'dd status=none conv=sync count=1 skip="$skiphowmany" bs="$blocksize" if="$inputfile" of="$outdevice"'
    return rf"""#!/bin/sh
inputfile={path_on_device}
outdevice={inputdev}
totalchars={lendata}
blocksize={blocksize}
howmanyloops={numberofloops}
skiphowmany=0
for line in $(seq 1 $howmanyloops); do
        skiphowmany=$((line-1))
        {commandline}
        {sleepbetweencommand}
        skiphowmany=$((skiphowmany+1))
done
        """

def subprocess_input_sendevent(
        int startx,
        int starty,
        int endx,
        int endy,
        int screen_height,
        int screen_width,
        int y_max=65535,
        int x_max=65535,
        object su_exe="su",
        object sh_device="sh",
        str inputdev="/dev/input/event5",
        str cwd_on_device="/sdcard",
        object adb_path=None,
        object device_serial=None,
        int qty_blocks=12*12,
        bytes echo_or_printf=b'printf "%b"',
        bint debug=True,
        **kwargs,
):
    cdef:
        str arg_hash, path_on_device, path_on_device_sh, ddscript
        object adbexecommand, adbsh
        bytes binary_data
    arg_hash = hashlib.md5(
        str(
            [
                startx,
                starty,
                endx,
                endy,
                screen_height,
                screen_width,
                y_max,
                x_max,
                su_exe,
                sh_device,
                inputdev,
                cwd_on_device,
                adb_path,
                device_serial,
                qty_blocks,
                echo_or_printf,
                kwargs,
            ]
        ).encode("utf-8")
    ).hexdigest()
    adbexecommand = configstuff.cached_script_files.get(arg_hash, None)
    adbsh = None
    if not adbexecommand:
        path_on_device = join_folder_file_make_abs_sh(cwd_on_device,f"{arg_hash}.bin")
        path_on_device_sh = join_folder_file_make_abs_sh(cwd_on_device,f"{arg_hash}.sh")
        if su_exe:
            adbexecommand = f"{su_exe} -c '{sh_device} {path_on_device_sh}'"
        else:
            adbexecommand = f"{sh_device} {path_on_device_sh}"
        ddscript, binary_data = create_struct_mouse_move_commands(
            allcoords=bresenham_line(int(startx), int(starty), int(endx), int(endy)),
            y_max=y_max,
            x_max=x_max,
            screen_height=screen_height,
            screen_width=screen_width,
            inputdev=inputdev,
            FORMAT="llHHI" * 3,
            path_on_device=path_on_device,
            qty_blocks=qty_blocks,
            exec_or_eval="exec",
            sleepbetweencommand=0,
            debug=debug,
        )
        if not adb_path:
            with open(path_on_device, mode="wb") as f:
                f.write(binary_data)
            with open(path_on_device_sh, mode="w", encoding="utf-8") as f:
                f.write(ddscript)

        else:
            adbsh = UniversalADBExecutor(adb_path=adb_path, device_serial=device_serial,**kwargs)
            adbexecommand_first_step = convert_to_concat_str_and_bytes(
                data=(
                    f"{su_exe}\n" if su_exe else "",
                    b"\n",
                    convert_to_base64_blocks(
                        data=binary_data,
                        outputpath=path_on_device,
                        chunksize=1024,
                        echo_or_printf=echo_or_printf,
                        split_into_chunks=True,
                    ),
                    b"\n",
                    convert_to_base64_blocks(
                        data=ddscript,
                        outputpath=path_on_device_sh,
                        chunksize=1024,
                        echo_or_printf=echo_or_printf,
                        split_into_chunks=True,
                    ),
                ),
                sep=b"\n",
            )
            adbsh.shell_without_capturing_stdout_and_stderr(
                command=adbexecommand_first_step,
                debug=False,
                ignore_exceptions=True,
            )

        configstuff.cached_script_files[arg_hash] = adbexecommand
    if not adb_path:
        return subprocess.run(
            sh_device,
            input=adbexecommand.encode(),
            shell=True,
            env=os.environ,
            capture_output=False,
        )
    else:
        if not adbsh:
            adbsh = UniversalADBExecutor(adb_path=adb_path, device_serial=device_serial,**kwargs)
        return adbsh.shell_without_capturing_stdout_and_stderr(
            command=adbexecommand,
            debug=False,
            ignore_exceptions=True,
        )

def join_folder_file_make_abs_sh(folder,file):
    if isinstance(folder,bytes):
        folder=folder.decode('utf-8')
    if isinstance(file,bytes):
        file=file.decode('utf-8')
    return "/" + folder.strip("/") + f"/{file}"


def dos2unix(data):
    if isinstance(data, str):
        return data.replace("\r\n", b"\n")
    return data

def convert_to_concat_str_and_bytes(data, sep=b""):
    if not isinstance(data, (tuple)):
        data = tuple(data)
    return (sep if isinstance(sep, bytes) else dos2unix(sep.encode("utf-8"))).join(
        d if isinstance(d, bytes) else dos2unix(d.encode("utf-8")) for d in data
    )
def convert_to_base64_blocks(
    object data,
    object outputpath="/dev/input/event3",
    Py_ssize_t chunksize=128,
    object echo_or_printf=b'printf "%b"',
    bint split_into_chunks=True,
):
    cdef:
        bytes outputdata, outputpathtmp
    if isinstance(echo_or_printf, str):
        echo_or_printf = echo_or_printf.encode()
    if isinstance(data, str):
        data = data.encode()
    data = base64.b64encode(data)
    if isinstance(outputpath, str):
        outputpath = outputpath.encode()
    outputpathtmp = outputpath + b".tmp"
    if split_into_chunks:
        outputdata = b"\n".join(
            (
                (
                    echo_or_printf
                    + b" '"
                    + (data[i : i + chunksize]).replace(b"'", b"'\\''")
                )
                + b"'"
                + (b" > " if i == 0 else b" >> ")
                + outputpathtmp
                for i in range(0, len(data), chunksize)
            )
        ).replace(b"\r\n", b"\n")
    else:
        outputdata = (
            (echo_or_printf + b" '" + (data).replace(b"'", b"'\\''") + b"'")
            + b" > "
            + outputpathtmp
        ).replace(b"\r\n", b"\n")
    outputdata = outputdata + b"\nbase64 -d " + outputpathtmp + b" > " + outputpath
    return outputdata


class SendEventMouseMove:
    __slots__=("fu",
                "startx",
                "starty",
                "endx",
                "endy",
                "y_max",
                "x_max",
                "screen_height",
                "screen_width",
                "su_exe",
                "sh_device",
                "inputdev",
                "cwd_on_device",
                "adb_path",
                "device_serial",
                "qty_blocks",
                "echo_or_printf",
                "debug",
                "kwargs",)
    def __init__(
        self,
        fu,
        startx,
        starty,
        endx,
        endy,
        screen_height,
        screen_width,
        y_max=65535,
        x_max=65535,
        su_exe="su",
        sh_device="sh",
        inputdev="/dev/input/event5",
        cwd_on_device="/sdcard",
        adb_path=None,
        device_serial=None,
        qty_blocks=12*12,
        echo_or_printf=b'printf "%b"',
        debug=True,
        **kwargs,
    ):
        self.fu = fu
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.y_max = y_max
        self.x_max = x_max
        self.screen_height=screen_height
        self.screen_width=screen_width
        self.su_exe = su_exe
        self.sh_device=sh_device
        self.inputdev = inputdev
        self.cwd_on_device = cwd_on_device
        self.adb_path = adb_path
        self.device_serial = device_serial
        self.qty_blocks = qty_blocks
        self.echo_or_printf=echo_or_printf
        self.debug = debug
        self.kwargs = kwargs

    def __call__(self, **kwargs):
        return self.fu(
            startx=int(self.startx),
            starty=int(self.starty),
            endx=int(self.endx),
            endy=int(self.endy),
            screen_height=int(self.screen_height),
            screen_width=int(self.screen_width),
            y_max=int(self.y_max),
            x_max=int(self.x_max),
            su_exe=self.su_exe,
            sh_device=self.sh_device,
            inputdev=self.inputdev,
            cwd_on_device=self.cwd_on_device,
            adb_path=self.adb_path,
            device_serial=self.device_serial,
            qty_blocks=int(self.qty_blocks),
            echo_or_printf=self.echo_or_printf if isinstance(self.echo_or_printf, bytes ) else self.echo_or_printf.encode(),
            debug=self.debug,
            **{**self.kwargs, **kwargs},
        )

    def __str__(self):
        return f"{self.startx}, {self.starty} -> {self.endx}, {self.endy}"

    def __repr__(self):
        return self.__str__()



def killthread(threadobject):
    """
    Attempts to terminate a thread by forcefully setting an asynchronous exception
    of type SystemExit in the thread's Python interpreter state. This function
    only operates on alive threads.

    Parameters:
        threadobject (threading.Thread): The thread object to terminate.

    Returns:
        bool: True if the thread was successfully found and an attempt to terminate it was made,
        False otherwise.

    Raises:
        ValueError: If threadobject does not refer to a valid active thread.
    """
    # based on https://pypi.org/project/kthread/
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True




ctypedef queue[string] ququ
ctypedef vector[string] stringvector
ctypedef unordered_map[string,string] strmap
cdef:
    ququ my_parsing_queue
    tuple[bytes] all_categories_eventparser=(
            b"AccessibilityDataSensitive",
            b"AccessibilityFocused",
            b"AccessibilityTool",
            b"Action",
            b"Active",
            b"AddedCount",
            b"BeforeText",
            b"BooleanProperties",
            b"Checked",
            b"ClassName",
            b"ConnectionId",
            b"ContentChangeTypes",
            b"ContentDescription",
            b"ContentInvalid",
            b"CurrentItemIndex",
            b"Empty",
            b"Enabled",
            b"EventTime",
            b"EventType",
            b"Focused",
            b"FromIndex",
            b"FullScreen",
            b"ItemCount",
            b"Loggable",
            b"MaxScrollX",
            b"MaxScrollY",
            b"MovementGranularity",
            b"PackageName",
            b"ParcelableData",
            b"Password",
            b"Records",
            b"RemovedCount",
            b"ScrollDeltaX",
            b"ScrollDeltaY",
            b"ScrollX",
            b"ScrollY",
            b"Scrollable",
            b"Sealed",
            b"Source",
            b"SourceDisplayId",
            b"SourceNodeId",
            b"SourceWindowId",
            b"SpeechStateChangeTypes",
            b"Text",
            b"ToIndex",
            b"WindowChangeTypes",
            b"WindowChanges",
            b"WindowId",
            b"TimeStamp",
            b'TimeNow',
            b"recordCount",
        )
    tuple all_categories_eventparser_utf8 = tuple(q.decode("utf-8") for q in all_categories_eventparser)
    dict[bytes,str]  all_categories_lookupdict={k:v for k,v in zip(all_categories_eventparser,all_categories_eventparser_utf8)}
    dict[str,bytes]  all_categories_lookupdict_string={v:k for k,v in zip(all_categories_eventparser,all_categories_eventparser_utf8)}

cdef class MyDict:
    cdef strmap c_dict
    cpdef int add_values(self,stringvector mykeys, stringvector myvalues) except + :
        cdef:
            Py_ssize_t i
            Py_ssize_t len_keys=mykeys.size()
        for i in range(len_keys):
            try:
                self.c_dict[<string>mykeys[i]]=<string>myvalues[i]
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()
        return 0

    def __getitem__(self, key,/):
        return self.c_dict[key]

    def __setitem__(self, i, item) -> None:
        self.c_dict[i]=item

    def __str__(self) -> str:
        cdef:
            strmap.iterator  begin = self.c_dict.begin()
            strmap.iterator  end = self.c_dict.end()
        while (begin!=end):
            printf("%-28s\t:\t%-50s\n",deref(begin).first.c_str(),deref(begin).second.c_str())
            inc(begin)
        return ""
    def add_to_struct_array(self,np.ndarray structarray, Py_ssize_t print_counter):
        cdef:
            strmap.iterator  begin = self.c_dict.begin()
            strmap.iterator  end = self.c_dict.end()
        while (begin!=end):
            structarray[all_categories_lookupdict[(deref(begin).first)]][print_counter]=deref(begin).second
            inc(begin)
    def __repr__(self) -> str:
        return self.__str__()

    def __delitem__(self, i):
        cdef:
            bint delete_first = False
            bint delete_second = False
            string dictkey = b''
            string dictvalue =b''
            list[bytes] dictvalues=[]
            Py_ssize_t valiter
            strmap.iterator it_start, it_end
        if isinstance(i,tuple):
            delete_first=True
            delete_second=True
            dictkey=i[0]
            dictvalue=i[1]
        elif isinstance(i,bytes):
            delete_first=True
            delete_second=False
            dictkey=i
        elif isinstance(i,list):
            delete_first=False
            delete_second=True
            dictvalues=i
        it_start = self.c_dict.begin()
        it_end = self.c_dict.end()
        while it_start != it_end:
            try:
                defa=deref(it_start)
                if delete_first and delete_second:
                    if (defa.first == dictkey) and (defa.second == dictvalue):
                        self.c_dict.erase(it_start)
                elif delete_first:
                    if (defa.first == dictkey):
                        self.c_dict.erase(it_start)
                        break
                elif delete_second:
                    for valiter in range(len(dictvalues)):
                        if (defa.second == <string>dictvalues[valiter]):
                            self.c_dict.erase(it_start)
                inc(it_start)
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()


def start_subproc(str adb_exe='',str device_serial='',str device_shell='', bytes uiautomator_cmd=b'uiautomator events'):
    r"""
    Starts a subprocess that executes the `uiautomator` command using the Android Debug Bridge (ADB)
    executable specified by the user. This function is designed to be run as a target of a thread for
    asynchronous operation.

    Parameters:
        adb_exe (str): The path to the ADB executable.
        device_serial (str): The serial number of the target device (for ADB commands).
        device_shell (str): The shell command to execute (default is 'sh').
        uiautomator_cmd (bytes): The command to send to uiautomator, typically to trigger event monitoring.

    Effects:
        This function modifies global configurations and appends to the running_uiautomators list to track subprocesses.
    """
    cdef:
        list[str] adb_commando=[]
        object readfunction
    if adb_exe:
        adb_commando.append(adb_exe)
    if device_serial:
        adb_commando.append('-s')
        adb_commando.append(device_serial)
    if device_shell:
        adb_commando.append(device_shell)
    else:
        adb_commando.append('sh')

    obsproc = subprocess.Popen(
        adb_commando,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    config_settings.running_uiautomators.append(obsproc)
    obsproc.stdin.write(uiautomator_cmd + b'\n\n')
    obsproc.stdin.flush()
    obsproc.stdin.close()
    readfunction=obsproc.stdout.readline
    try:
        for line in iter(readfunction, b""):
            if not config_settings.read_events_data:
                break
            my_parsing_queue.push(line)
    except:
        pass
my_parsing_queue.push(b'')

def start_thread(str adb_exe='',str device_serial='',str device_shell='shell',bytes uiautomator_cmd=b'uiautomator events',bint thread_daemon=True):
    r"""
    Initializes and starts a thread that runs a subprocess for capturing UI Automator events.
    This function is a higher-level wrapper intended to facilitate threading of the `start_subproc` function.

    Parameters:
        adb_exe (str): The path to the ADB executable.
        device_serial (str): The device serial number to target with ADB.
        device_shell (str): The shell to use in the device, defaults to 'shell'.
        uiautomator_cmd (bytes): The command for UI Automator to execute.
        thread_daemon (bool): Whether the thread should be a daemon.

    Returns:
        threading.Thread: The thread that was started.
    """
    t=threading.Thread(target=start_subproc,kwargs={'adb_exe':adb_exe,'device_serial':device_serial,'device_shell':device_shell, 'uiautomator_cmd':uiautomator_cmd},daemon=thread_daemon)
    t.start()
    return t


def start_parsing_thread(adb_exe,device_serial,device_shell,uiautomator_cmd,thread_daemon,sleep_after_starting_thread):
    t=start_thread(adb_exe=adb_exe if adb_exe else '',device_serial=device_serial,device_shell=device_shell,uiautomator_cmd=uiautomator_cmd,thread_daemon=thread_daemon)
    config_settings.running_parsing_threads.append(t)
    time.sleep(sleep_after_starting_thread)
    while not config_settings.running_uiautomators:
        time.sleep(1)
    return t


cdef: 
    object categories_regex=re.compile(rb"\L<options>", options=all_categories_eventparser, ignore_unused=True)
    list all_categories_eventparser_with_timenow_sorted=sorted(all_categories_eventparser+(b'TimeNow',))
    stringvector fillkeys=[<string>bv for bv in all_categories_eventparser_with_timenow_sorted]
    stringvector dummykeys=[<string>b'' for _ in range(len(fillkeys))]

def start_parsing(
    object callback_function,
    object callback_function_after_each_loop,
    np.ndarray dataarray,
    Py_ssize_t len_dataarray,
    object callback_function_kwargs=None,
    float sleep_between_each_scan=0.001,
    bint regex_nogil=True,
    str device_serial = "",
    str adb_exe = '',
    str device_shell = "shell",
    bytes uiautomator_cmd = b"uiautomator events",
    float sleep_after_starting_thread = 5,
    bint thread_daemon = True,
    bytes uiautomator_kill_cmd=b'pkill uiautomator',
    bint print_elements=False

):
    cdef:
        list[str] adb_commando_kill=[]
        MyDict parsingdict = MyDict()
        Py_ssize_t start, end, coun
        list firstfilelds, myke_myva
        Py_ssize_t print_counter=0
        bytes strax, hxq
        bint start_new_parsing_thread=True
        object killsubproc = None
        object t=None
        Py_ssize_t stop_or_continue

    if not callback_function_kwargs:
        callback_function_kwargs={}
    if config_settings.running_parsing_threads:
        try:
            if config_settings.running_parsing_threads[len(config_settings.running_parsing_threads)-1].is_alive():
                t=config_settings.running_parsing_threads[len(config_settings.running_parsing_threads)-1]
                start_new_parsing_thread=False
        except Exception:
            pass
    if start_new_parsing_thread:
        t= start_parsing_thread(adb_exe,device_serial,device_shell,uiautomator_cmd,thread_daemon,sleep_after_starting_thread)
    parsingdict.add_values(mykeys=fillkeys, myvalues=dummykeys)
    config_settings.read_events_data=True
    config_settings.stop=False
    try:
        while not config_settings.stop:
            try:
                time.sleep(sleep_between_each_scan)
                while not my_parsing_queue.empty():
                    if config_settings.stop:
                        break
                    try:
                        start=0
                        end=0
                        coun=0
                        try:
                            for resu in categories_regex.finditer(hxq:=my_parsing_queue.front(),concurrent=regex_nogil):
                                if config_settings.stop:
                                    break
                                try:
                                    if coun==0:
                                        firstfilelds=hxq.split(maxsplit=2)
                                        if len(firstfilelds)==3:
                                            parsingdict.c_dict[b'TimeNow']= firstfilelds[1]
                                        coun+=1
                                        continue
                                    end=resu.start()
                                    strax=(hxq[start:end])
                                    if coun!=1:
                                        myke_myva=re.split(br':\s+', strax.rstrip(b'; '),maxsplit=1,)
                                        if len(myke_myva)==2:
                                            parsingdict.c_dict[<string>myke_myva[0]]=<string>myke_myva[1]
                                    start=end
                                    coun+=1
                                except Exception:
                                    if config_settings.debug_enabled:
                                        errwrite()
                        except Exception:
                            if config_settings.debug_enabled:
                                errwrite()
                        my_parsing_queue.pop()
                        parsingdict.add_to_struct_array(dataarray, print_counter%len_dataarray)

                        if print_elements:
                            str(parsingdict)
                        stop_or_continue=callback_function(counter=print_counter,dataarray=dataarray,**callback_function_kwargs)
                        print_counter+=1
                        if stop_or_continue==2:
                            return 1
                        parsingdict.c_dict.clear()
                        parsingdict.add_values(mykeys=fillkeys, myvalues=dummykeys)
                    except Exception:
                        if config_settings.debug_enabled:
                            errwrite()
                stop_or_continue=callback_function_after_each_loop()
                if stop_or_continue==2:
                    return 0
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()

    except Exception:
        pass
    except KeyboardInterrupt:
        try:
            print('Shutting down...')
            config_settings.stop=True
            config_settings.read_events_data=False
            time.sleep(0.001)
        except:
            pass

        if adb_exe:
            adb_commando_kill.append(adb_exe)
        if device_serial:
            adb_commando_kill.append('-s')
            adb_commando_kill.append(device_serial)
        if device_shell:
            adb_commando_kill.append(device_shell)
        else:
            adb_commando_kill.append('sh')
        try:
            killsubproc=kill_uiautomator(adb_commando_kill,uiautomator_kill_cmd)
        except Exception:
            pass
        try:
            if t:
                killthread(t)
        except Exception:
            if config_settings.debug_enabled:
                errwrite()
        for subpro in config_settings.running_uiautomators:
            try:
                subpro.kill()
            except Exception:
                pass
        config_settings.running_uiautomators.clear()
        config_settings.read_events_data=True
        config_settings.stop=False
        try:
            killsubproc.kill()
        except Exception:
            if config_settings.debug_enabled:
                errwrite()


def kill_uiautomator(adb_commando_kill,uiautomator_kill_cmd):
    killsubproc=subprocess.Popen(
            adb_commando_kill,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    killsubproc.stdin.write(uiautomator_kill_cmd + b'\n\n')
    killsubproc.stdin.flush()
    killsubproc.stdin.close()
    return killsubproc


class EvParse:
    def __init__(
        self,
        str adb_exe="",
        str device_serial="",
        Py_ssize_t field_size=50,
        Py_ssize_t  record_count=100,
        double sleep_between_each_scan=0.001,
        bint regex_nogil=True,
        str device_shell="sh",
        bytes uiautomator_cmd=b"uiautomator events",
        Py_ssize_t  sleep_after_starting_thread=5,
        bint thread_daemon=True,
        bytes uiautomator_kill_cmd=b"pkill uiautomator",
        double timeout_scan=0.01,
        Py_ssize_t screen_width=720,
        Py_ssize_t screen_height=1280,
        bint subproc_shell=False,
        bint with_children=False,
        bint add_screenshot=True,
        object screenshot_kwargs=None,
        str input_tap_center_x="aa_center_x",
        str input_tap_center_y="aa_center_y",
        str input_tap_input_cmd="input touchscreen tap",
        object input_tap_kwargs=None,
        str sendevent_mouse_move_start_x="aa_start_x",
        str sendevent_mouse_move_start_y="aa_start_y",
        str sendevent_mouse_move_end_x="aa_end_x",
        str sendevent_mouse_move_end_y="aa_end_y",
        Py_ssize_t sendevent_mouse_move_y_max=65535,
        Py_ssize_t sendevent_mouse_move_x_max=65535,
        str sendevent_mouse_move_inputdev="/dev/input/event5",
        bint sendevent_mouse_move_add=True,
        object sendevent_mouse_move_kwargs=None,
        str sendevent_mouse_move_su_exe="su",
        str sendevent_mouse_move_sh_device="sh",
        str sendevent_mouse_move_cwd_on_device="/sdcard",
        Py_ssize_t sendevent_mouse_move_qty_blocks=4 * 24,
        bint debug=True,
    ):

        self.npdtype = np.dtype(
            [(q, f"S{field_size}") for q in (all_categories_eventparser_utf8)],
            align=True,
        )
        self.data_array = np.array(
            [b"" for _ in range(record_count)],
            dtype=self.npdtype,
        )
        self.data_array_strides = self.data_array.strides[0]
        self.data_array_shape = self.data_array.shape[0]
        self.data_array_address = self.data_array.ctypes._arr.__array_interface__[
            "data"
        ][0]
        self.data_array_haystack_buffer = (
            ctypes.c_char * (self.data_array_strides * self.data_array_shape)
        ).from_address(self.data_array_address)
        self.last_results = []
        self.data_array_number_of_fields = len(self.data_array.dtype.fields)
        self.data_array_itemsize = self.data_array.itemsize
        self.data_array_fields = self.data_array.dtype.names
        self.starttime = [time.time()]
        self.data_array_len = len(self.data_array)
        self.sleep_between_each_scan = sleep_between_each_scan
        self.regex_nogil = regex_nogil
        self.device_serial = device_serial
        self.adb_exe = adb_exe
        self.device_shell = device_shell
        self.uiautomator_cmd = uiautomator_cmd
        self.sleep_after_starting_thread = sleep_after_starting_thread
        self.thread_daemon = thread_daemon
        self.uiautomator_kill_cmd = uiautomator_kill_cmd
        self.timeout_scan = timeout_scan
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.subproc_shell = subproc_shell
        self.with_children = with_children
        self.add_screenshot = add_screenshot
        self.screenshot_kwargs = screenshot_kwargs
        self.input_tap_center_x = input_tap_center_x
        self.input_tap_center_y = input_tap_center_y
        self.input_tap_input_cmd = input_tap_input_cmd
        self.input_tap_kwargs = input_tap_kwargs
        self.sendevent_mouse_move_start_x = sendevent_mouse_move_start_x
        self.sendevent_mouse_move_start_y = sendevent_mouse_move_start_y
        self.sendevent_mouse_move_end_x = sendevent_mouse_move_end_x
        self.sendevent_mouse_move_end_y = sendevent_mouse_move_end_y
        self.sendevent_mouse_move_y_max = sendevent_mouse_move_y_max
        self.sendevent_mouse_move_x_max = sendevent_mouse_move_x_max
        self.sendevent_mouse_move_inputdev = sendevent_mouse_move_inputdev
        self.sendevent_mouse_move_add = sendevent_mouse_move_add
        self.sendevent_mouse_move_kwargs = sendevent_mouse_move_kwargs
        self.sendevent_mouse_move_su_exe = sendevent_mouse_move_su_exe
        self.sendevent_mouse_move_sh_device = sendevent_mouse_move_sh_device
        self.sendevent_mouse_move_cwd_on_device = sendevent_mouse_move_cwd_on_device
        self.sendevent_mouse_move_qty_blocks = sendevent_mouse_move_qty_blocks
        self.debug = debug

    def callback_function(self, **kwargs):
        cdef:
            Py_ssize_t allresults_counter, regex_flags, xstart, start_table
            bytes regex_to_check,column
        try:
            regex_to_check = kwargs.get("regex_to_check", b".*")
            regex_flags = kwargs.get("regex_flags",2)
            allresults_counter = 0
            for x in re.finditer(
                regex_to_check,
                self.data_array_haystack_buffer[:],
                flags=regex_flags,
            ):
                try:
                    xstart = x.start()
                    start_table = xstart // self.data_array_strides
                    column = all_categories_eventparser[
                        xstart
                        % self.data_array_strides
                        // (
                            self.data_array_itemsize // self.data_array_number_of_fields
                        )
                    ]
                    allresults_counter += 1
                    if start_table>=self.data_array_len:
                        print(f'OVER {self.data_array_len}',start_table)
                        continue
                    self.last_results.append(
                        dict(zip(self.data_array_fields, self.data_array[start_table]))
                    )
                    self.last_results[len(self.last_results) - 1].update(
                        {"TimeNow": time.time(), "RegexColumn": column, "RegexMatch": x}
                    )
                except Exception:
                    if config_settings.debug_enabled:
                        errwrite()
            self.data_array[:]=b''
        except Exception:
            if config_settings.debug_enabled:
                errwrite()
        return 0

    def start_event_parser(
        self,
        callback_function=None,
        max_timeout=0.1,
        callback_function_kwargs=None,
        sleep_between_each_scan=-1,
        print_elements=False

    ):
        if not callback_function:
            callback_function = self.callback_function
        if not callback_function_kwargs:
            callback_function_kwargs = {}
        if sleep_between_each_scan <= 0:
            sleep_between_each_scan = self.sleep_between_each_scan
        self.starttime.append(max_timeout)
        return start_parsing(
            callback_function=callback_function,
            callback_function_after_each_loop=self.callback_function_after_each_loop,
            dataarray=self.data_array,
            len_dataarray=self.data_array_len,
            callback_function_kwargs=callback_function_kwargs,
            sleep_between_each_scan=sleep_between_each_scan,
            regex_nogil=self.regex_nogil,
            device_serial=self.device_serial,
            adb_exe=self.adb_exe,
            device_shell=self.device_shell,
            uiautomator_cmd=self.uiautomator_cmd,
            sleep_after_starting_thread=self.sleep_after_starting_thread,
            thread_daemon=self.thread_daemon,
            uiautomator_kill_cmd=self.uiautomator_kill_cmd,
            print_elements=print_elements,
        )

    def callback_function_after_each_loop(self, **kwargs):
        if self.starttime:
            if (
                self.starttime[len(self.starttime) - 1] + self.timeout_scan
                < time.time()
            ):
                self.starttime.clear()
                return 2
        return 0

    def kill_ui_automator(self, open_shell_cmd):
        kill_uiautomator(
            adb_commando_kill=open_shell_cmd,
            uiautomator_kill_cmd=self.uiautomator_kill_cmd,
        )

    def parse_elements_dataframe(
        self,
        screen_width=None,
        screen_height=None,
        subproc_shell=None,
        with_children=None,
        add_screenshot=None,
        screenshot_kwargs=None,
        input_tap_center_x=None,
        input_tap_center_y=None,
        input_tap_input_cmd=None,
        input_tap_kwargs=None,
        sendevent_mouse_move_start_x=None,
        sendevent_mouse_move_start_y=None,
        sendevent_mouse_move_end_x=None,
        sendevent_mouse_move_end_y=None,
        sendevent_mouse_move_y_max=None,
        sendevent_mouse_move_x_max=None,
        sendevent_mouse_move_inputdev=None,
        sendevent_mouse_move_add=None,
        sendevent_mouse_move_kwargs=None,
        sendevent_mouse_move_su_exe=None,
        sendevent_mouse_move_sh_device=None,
        sendevent_mouse_move_cwd_on_device=None,
        sendevent_mouse_move_qty_blocks=None,
        debug=None,
        **kwargs,
    ):
        if not screen_width:
            screen_width = self.screen_width
        if not screen_height:
            screen_height = self.screen_height
        if not subproc_shell:
            subproc_shell = self.subproc_shell
        if not with_children:
            with_children = self.with_children
        if not add_screenshot:
            add_screenshot = self.add_screenshot
        if not screenshot_kwargs:
            screenshot_kwargs = self.screenshot_kwargs
        if not input_tap_center_x:
            input_tap_center_x = self.input_tap_center_x
        if not input_tap_center_y:
            input_tap_center_y = self.input_tap_center_y
        if not input_tap_input_cmd:
            input_tap_input_cmd = self.input_tap_input_cmd
        if not input_tap_kwargs:
            input_tap_kwargs = self.input_tap_kwargs
        if not sendevent_mouse_move_start_x:
            sendevent_mouse_move_start_x = self.sendevent_mouse_move_start_x
        if not sendevent_mouse_move_start_y:
            sendevent_mouse_move_start_y = self.sendevent_mouse_move_start_y
        if not sendevent_mouse_move_end_x:
            sendevent_mouse_move_end_x = self.sendevent_mouse_move_end_x
        if not sendevent_mouse_move_end_y:
            sendevent_mouse_move_end_y = self.sendevent_mouse_move_end_y
        if not sendevent_mouse_move_y_max:
            sendevent_mouse_move_y_max = self.sendevent_mouse_move_y_max
        if not sendevent_mouse_move_x_max:
            sendevent_mouse_move_x_max = self.sendevent_mouse_move_x_max
        if not sendevent_mouse_move_inputdev:
            sendevent_mouse_move_inputdev = self.sendevent_mouse_move_inputdev
        if not sendevent_mouse_move_add:
            sendevent_mouse_move_add = self.sendevent_mouse_move_add
        if not sendevent_mouse_move_kwargs:
            sendevent_mouse_move_kwargs = self.sendevent_mouse_move_kwargs
        if not sendevent_mouse_move_su_exe:
            sendevent_mouse_move_su_exe = self.sendevent_mouse_move_su_exe
        if not sendevent_mouse_move_sh_device:
            sendevent_mouse_move_sh_device = self.sendevent_mouse_move_sh_device
        if not sendevent_mouse_move_cwd_on_device:
            sendevent_mouse_move_cwd_on_device = self.sendevent_mouse_move_cwd_on_device
        if not sendevent_mouse_move_qty_blocks:
            sendevent_mouse_move_qty_blocks = self.sendevent_mouse_move_qty_blocks
        if not debug:
            debug = self.debug
        return parse_fragments_active_screen(
            serial=self.device_serial,
            adb_path=self.adb_exe,
            number_of_max_views=1,
            screen_width=screen_width,
            screen_height=screen_height,
            subproc_shell=subproc_shell,
            with_children=with_children,
            add_screenshot=add_screenshot,
            screenshot_kwargs=screenshot_kwargs,
            input_tap_center_x=input_tap_center_x,
            input_tap_center_y=input_tap_center_y,
            input_tap_input_cmd=input_tap_input_cmd,
            input_tap_kwargs=input_tap_kwargs,
            sendevent_mouse_move_start_x=sendevent_mouse_move_start_x,
            sendevent_mouse_move_start_y=sendevent_mouse_move_start_y,
            sendevent_mouse_move_end_x=sendevent_mouse_move_end_x,
            sendevent_mouse_move_end_y=sendevent_mouse_move_end_y,
            sendevent_mouse_move_y_max=sendevent_mouse_move_y_max,
            sendevent_mouse_move_x_max=sendevent_mouse_move_x_max,
            sendevent_mouse_move_inputdev=sendevent_mouse_move_inputdev,
            sendevent_mouse_move_add=sendevent_mouse_move_add,
            sendevent_mouse_move_kwargs=sendevent_mouse_move_kwargs,
            sendevent_mouse_move_su_exe=sendevent_mouse_move_su_exe,
            sendevent_mouse_move_sh_device=sendevent_mouse_move_sh_device,
            sendevent_mouse_move_cwd_on_device=sendevent_mouse_move_cwd_on_device,
            sendevent_mouse_move_qty_blocks=sendevent_mouse_move_qty_blocks,
            debug=debug,
        )

