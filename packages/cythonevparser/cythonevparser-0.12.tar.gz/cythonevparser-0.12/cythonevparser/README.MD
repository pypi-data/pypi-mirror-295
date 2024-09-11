# eventparser parser for Android

### Tested against Windows 10 / Python 3.11 / Anaconda / BlueStacks

### pip install cythonevparser

### Cython and a C compiler must be installed!

```PY
Coordinates the parsing of UI Automator events by initiating a thread to gather data and then processing that data using regex matching based on user-specified criteria. This function aims to facilitate real-time event handling for UI analysis.

Parameters:
    myregex_keys (str): Regex pattern to match keys.
    myregex_values (str): Regex pattern to match values.
    filter_function (callable, optional): A function to apply as a filter for matched regex patterns. Should return 1 to stop parsing.
    regex_flags_keys (int): Regex flags for key matching.
    regex_flags_values (int): Regex flags for value matching.
    sleep_between_each_scan (float): Time to wait between each scan loop.
    print_results (bool): Flag to determine whether to print the results.
    regex_nogil (bool): Flag to enable or disable GIL during regex operations.
    device_serial (str), adb_exe (str), device_shell (str), uiautomator_cmd (bytes): Parameters for the thread and subprocess.
    sleep_after_starting_thread (float): Time to wait after starting the thread before processing.
    thread_daemon (bool): Whether the thread should run as a daemon.
    uiautomator_kill_cmd (bytes): Command to kill the uiautomator process.
    observe_results (bool): Whether to observe and react to the results in real-time.

Notes:
    This function leverages threading and subprocess management to maintain continuous monitoring and processing of UI events.

import regex as re
import cythonevparser
import shutil
cythonevparser.evparse.config_settings.debug_enabled = False

def filter_keys_function(
    key=b"",
    value=b"",
    myregex_keys=b"",
    myregex_values=b"",
    regex_flags_keys=0,
    regex_flags_values=0,
):
    # print('observing')
    try:
        if b"Metallica" in value:
            return 1

        if re.search(myregex_keys, key, flags=regex_flags_keys) and re.search(
            myregex_values, value, flags=regex_flags_values
        ):
            print(key, value)
            return 1 # stops the loop
        return 0
    except Exception:
        return 0


device_serial = "127.0.0.1:5560"
adb_exe = shutil.which("adb")
device_shell = "shell"
uiautomator_cmd = b"uiautomator events"
regex_nogil = True
sleep_after_starting_thread = 5
thread_daemon = True
print_results = True
sleep_between_each_scan = 0.001
regex_flags_keys = re.IGNORECASE
regex_flags_values = re.IGNORECASE
filter_function = filter_keys_function
myregex_keys = b"Text|Content"
myregex_values = rb"Metallica"
uiautomator_kill_cmd = b"pkill uiautomator"
observe_results = True


cythonevparser.evparse.start_parsing(
    myregex_keys=myregex_keys,
    myregex_values=myregex_values,
    filter_function=filter_function,
    regex_flags_keys=regex_flags_keys,
    regex_flags_values=regex_flags_values,
    sleep_between_each_scan=sleep_between_each_scan,
    print_results=print_results,
    regex_nogil=regex_nogil,
    device_serial=device_serial,
    adb_exe=adb_exe,
    device_shell=device_shell,
    uiautomator_cmd=uiautomator_cmd,
    sleep_after_starting_thread=sleep_after_starting_thread,
    thread_daemon=thread_daemon,
    uiautomator_kill_cmd=uiautomator_kill_cmd,
    observe_results=observe_results,
)

```