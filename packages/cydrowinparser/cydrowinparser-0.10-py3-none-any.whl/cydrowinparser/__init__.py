from __future__ import annotations
import pandas as pd 
import numpy as np 
meta_name_column = "bb_meta___hash__"
try:
    import cywinparser

except Exception as e:
    import Cython, adbshellexecuter, setuptools, numpy, cythondfprint, cythonevparser, exceptdrucker, pandas, regex, platform, os, subprocess, sys, time

    iswindows = "win" in platform.platform().lower()
    if iswindows:
        addtolist = []
    else:
        addtolist = ["&"]

    olddict = os.getcwd()
    dirname = os.path.dirname(__file__)
    os.chdir(dirname)
    compile_file = os.path.join(dirname, "cywinparser_compile.py")
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
        time.sleep(60)
    import cywinparser

    os.chdir(olddict)


def _convert_to_int(x):
    try:
        return int(x, 16)
    except Exception:
        return pd.NA

def parse_elements_and_window(
    adb_exe,
    device_serial,
    number_of_max_views=1,
    screen_width=720,
    screen_height=1280,
    subproc_shell=False,
    with_children=False,
    add_screenshot=False,
    screenshot_kwargs=None,
    add_input_tap=True,
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
    sendevent_mouse_move_cwd_on_device="/sdcard",
    sendevent_mouse_move_qty_blocks=12 * 24,
    debug=True,
    **kwargs,
):
    dfx = cywinparser.parse_fragment_eles(
        serial=device_serial,
        adb_path=adb_exe,
        number_of_max_views=number_of_max_views,
        screen_width=screen_width,
        screen_height=screen_height,
        subproc_shell=subproc_shell,
        with_children=with_children,
        add_screenshot=add_screenshot,
        screenshot_kwargs=screenshot_kwargs,
        add_input_tap=add_input_tap,
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
    #dfx.loc[:, meta_name_column] = dfx.aa_mid.apply(_convert_to_int)
    try:
        df = cywinparser.parse_window_elements(
            dfx=dfx,
            adbexe=adb_exe,
            device_serial=device_serial,
            dump_cmd="cmd window dump-visible-window-views",
        )
        print(df)
        return df
    except Exception as e:
        print(e)
    return dfx
