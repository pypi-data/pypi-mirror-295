# window dump parser for Android

### Tested against Windows 10 / Python 3.11 / Anaconda /  Bluestacks

### pip install cydrowinparser

### Cython and a C compiler must be installed!

```PY
import time
import regex as re
import cythonevparser
import shutil
import pandas as pd
import cydrowinparser

adb_exe = shutil.which("adb")
device_serial = "127.0.0.1:5560"
cythonevparser.evparse.create_temp_memdisk(
    memdisk_path="/media/ramdisk",
    adb_path=adb_exe,
    device_serial=device_serial,
    memdisk_size="128M",
    shell=False,
    su_exe="su",
)
allargs = dict(
    adb_exe=adb_exe,
    device_serial=device_serial,
    field_size=50,
    record_count=100,
    sleep_between_each_scan=0.01,
    regex_nogil=True,
    device_shell="shell",
    uiautomator_cmd=b"uiautomator events",
    sleep_after_starting_thread=5,
    thread_daemon=True,
    uiautomator_kill_cmd=b"pkill uiautomator",
    timeout_scan=0.1,
    screen_width=720,
    screen_height=1280,
    subproc_shell=False,
    with_children=False,
    add_screenshot=False,
    screenshot_kwargs=None,
    input_tap_center_x="aa_center_x",
    input_tap_center_y="aa_center_y",
    input_tap_input_cmd="input touchscreen tap",
    input_tap_kwargs=None,
    sendevent_mouse_move_start_x="aa_start_x",
    sendevent_mouse_move_start_y="aa_start_y",
    sendevent_mouse_move_end_x="aa_end_x",
    sendevent_mouse_move_end_y="aa_end_y",
    sendevent_mouse_move_y_max=65535,
    sendevent_mouse_move_x_max=65535,
    sendevent_mouse_move_inputdev="/dev/input/event5",
    sendevent_mouse_move_add=True,
    sendevent_mouse_move_kwargs=None,
    sendevent_mouse_move_su_exe="su",
    sendevent_mouse_move_sh_device="sh",
    sendevent_mouse_move_cwd_on_device="/media/ramdisk",
    sendevent_mouse_move_qty_blocks=8 * 24,
    debug=True,
)
evp = cythonevparser.evparse.EvParse(**allargs)
callback_function_kwargs = {}
callback_function_kwargs["regex_to_check"] = rb"Metallica"
callback_function_kwargs["regex_flags"] = re.IGNORECASE
while True:
    try:
        df = cydrowinparser.parse_elements_and_window(**allargs)
        for mousecmd in df.loc[
            df.aa_classname.str.contains("textview")
            & df.aa_element_id.str.contains("title")
        ].aa_mouse_move:
            try:
                evp.data_array[:] = b""
                mousecmd()
                evp.starttime.append(time.time())
                result = evp.start_event_parser(
                    callback_function=evp.callback_function,
                    max_timeout=0.1,
                    callback_function_kwargs=callback_function_kwargs,
                    sleep_between_each_scan=0.01,
                    print_elements=True,
                )
                if evp.last_results:
                    dfparsed = pd.DataFrame(evp.last_results, dtype="object")
                    print(dfparsed["Text"])
                    evp.last_results.clear()
                    if b"Nothing" in dfparsed["Text"].iloc[0]:
                        print("found Nothing, sleeping .1 seconds")
                        time.sleep(.1)
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        pass
```