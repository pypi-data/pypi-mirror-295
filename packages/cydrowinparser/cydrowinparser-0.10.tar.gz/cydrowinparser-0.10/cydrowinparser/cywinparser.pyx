cimport cython
cimport numpy as np
from adbshellexecuter import UniversalADBExecutor, iswindows
from cythondfprint import add_printer
import cythonevparser
from exceptdrucker import errwrite
import cython
import io
import numpy as np
import os
import pandas as pd
import regex as re
import struct
import sys
import zipfile

add_printer(1)
re.cache_all(True)
config_settings=sys.modules[__name__]
config_settings.debug_enabled=True
remove_non_word_chars = re.compile(rb"[\W_]")
cdef:
    int SIG_BOOLEAN = ord("Z")
    int SIG_BYTE = ord("B")
    int SIG_SHORT = ord("S")
    int SIG_INT = ord("I")
    int SIG_LONG = ord("J")
    int SIG_FLOAT = ord("F")
    int SIG_DOUBLE = ord("D")
    int SIG_STRING = ord("R")
    int SIG_MAP = ord("M")
    int SIG_END_MAP = 0
    str PYTHON_STRUCT_UNPACK_SIG_BOOLEAN = "?"
    str PYTHON_STRUCT_UNPACK_SIG_BYTE = "b"
    str PYTHON_STRUCT_UNPACK_SIG_SHORT = "h"
    str PYTHON_STRUCT_UNPACK_SIG_INT = "i"
    str PYTHON_STRUCT_UNPACK_SIG_LONG = "q"
    str PYTHON_STRUCT_UNPACK_SIG_FLOAT = "f"
    str PYTHON_STRUCT_UNPACK_SIG_DOUBLE = "d"
    str PYTHON_STRUCT_UNPACK_SIG_STRING = "s"
    str LITTLE_OR_BIG = ">"
    object STRUCT_UNPACK_SIG_BOOLEAN = struct.Struct(
    f"{LITTLE_OR_BIG}{PYTHON_STRUCT_UNPACK_SIG_BOOLEAN }"
    ).unpack
    object STRUCT_UNPACK_SIG_BYTE = struct.Struct(
        f"{LITTLE_OR_BIG}{PYTHON_STRUCT_UNPACK_SIG_BYTE }"
    ).unpack
    object STRUCT_UNPACK_SIG_SHORT = struct.Struct(
        f"{LITTLE_OR_BIG}{PYTHON_STRUCT_UNPACK_SIG_SHORT }"
    ).unpack
    object STRUCT_UNPACK_SIG_INT = struct.Struct(
        f"{LITTLE_OR_BIG}{PYTHON_STRUCT_UNPACK_SIG_INT }"
    ).unpack
    object STRUCT_UNPACK_SIG_LONG = struct.Struct(
        f"{LITTLE_OR_BIG}{PYTHON_STRUCT_UNPACK_SIG_LONG }"
    ).unpack
    object STRUCT_UNPACK_SIG_FLOAT = struct.Struct(
        f"{LITTLE_OR_BIG}{PYTHON_STRUCT_UNPACK_SIG_FLOAT }"
    ).unpack
    object STRUCT_UNPACK_SIG_DOUBLE = struct.Struct(
        f"{LITTLE_OR_BIG}{PYTHON_STRUCT_UNPACK_SIG_DOUBLE }"
    ).unpack

meta_name_column="bb_meta___hash__"


cpdef int parsedata(bytes sbytes, list resultlist):
    cdef:
        object restofstringasbytes = io.BytesIO(sbytes)
        bytes nextbyte, bytes2convert
        object convertedbytes
        int ordnextbyte

    while nextbyte := restofstringasbytes.read(1):
        try:
            convertedbytes = b""
            ordnextbyte = ord(nextbyte)
            if ordnextbyte == SIG_STRING:
                bytes2convert2 = restofstringasbytes.read(2)
                bytes2convert = restofstringasbytes.read(
                    bytes2convert2[len(bytes2convert2) - 1]
                )
                convertedbytes = bytes2convert.decode("utf-8", errors="ignore")
                resultlist.append(convertedbytes)
            elif ordnextbyte == SIG_SHORT:
                bytes2convert = restofstringasbytes.read(2)
                convertedbytes = STRUCT_UNPACK_SIG_SHORT(bytes2convert)[0]
                resultlist.append(convertedbytes)
            elif ordnextbyte == SIG_BOOLEAN:
                bytes2convert = restofstringasbytes.read(1)
                convertedbytes = STRUCT_UNPACK_SIG_BOOLEAN(bytes2convert)[0]
                resultlist.append(convertedbytes)
            elif ordnextbyte == SIG_BYTE:
                bytes2convert = restofstringasbytes.read(1)
                convertedbytes = STRUCT_UNPACK_SIG_BYTE(bytes2convert)[0]
                resultlist.append(convertedbytes)
            elif ordnextbyte == SIG_INT:
                bytes2convert = restofstringasbytes.read(4)
                convertedbytes = STRUCT_UNPACK_SIG_INT(bytes2convert)[0]
                resultlist.append(convertedbytes)
            elif ordnextbyte == SIG_FLOAT:
                bytes2convert = restofstringasbytes.read(4)
                convertedbytes = STRUCT_UNPACK_SIG_FLOAT(bytes2convert)[0]
                resultlist.append(convertedbytes)
            elif ordnextbyte == SIG_DOUBLE:
                bytes2convert = restofstringasbytes.read(8)
                convertedbytes = STRUCT_UNPACK_SIG_DOUBLE(bytes2convert)[0]
                resultlist.append(convertedbytes)
            elif ordnextbyte == SIG_LONG:
                bytes2convert = restofstringasbytes.read(8)
                convertedbytes = STRUCT_UNPACK_SIG_LONG(bytes2convert)[0]
                resultlist.append(convertedbytes)
        except Exception:
            if config_settings.debug_enabled:
                errwrite()
    return 0


cpdef list[tuple] extract_files_from_zip(object zipfilepath):
    cdef:
        bytes data=b""
        object ioby
        list[tuple] single_files_extracted
        Py_ssize_t len_single_files, single_file_index
    if isinstance(zipfilepath, str) and os.path.exists(zipfilepath):
        with open(zipfilepath, "rb") as f:
            data = f.read()
    else:
        data = zipfilepath
    ioby = io.BytesIO(data)
    single_files_extracted = []
    with zipfile.ZipFile(ioby, "r") as zip_ref:
        single_files = zip_ref.namelist()
        len_single_files = len(single_files)
        for single_file_index in range(len_single_files):
            try:
                single_files_extracted.append(
                    (
                        single_files[single_file_index],
                        zip_ref.read(single_files[single_file_index]),
                    )
                )
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()
    return single_files_extracted


def _convert_to_int(str x):
    try:
        return int(x, 16)
    except Exception:
        return pd.NA


def parse_screen_elements(
    bytes data,
):
    cdef:
        bint firstnonzero
        object joined_regex_re, dummyvalue, finalvalue, df
        bytes window_data, property_data, key_spli
        list property_data_split, windows_conjunction, for_regex, val_spli_list, splidata, tmpval_spli_list, alldfs
        Py_ssize_t property_data_split_len, counter, pindex, windows_conjunction_len, co_index, len_mapped_properties, pro_index
        Py_ssize_t group_counter, member_counter, len_splitdata, spl_data0_index, len_splitdata_spl_data0_index, spl_data1_index
        Py_ssize_t key_spli_val_spli_index, val_spli_list_len, tmval_index,  indi
        list[list] mapped_properties,splitdata
        str meta_name_column = "bb_meta___name__"

        dict properymap, all_elements_sorted, i0, i1
        list[np.ndarray] realitemindexlist
        dict string_columns_none
    window_data, property_data = data.split(b"R\x00\rpropertyIndex", maxsplit=1)
    property_data_split = property_data.split(b"R\x00")
    counter = 0
    mapped_properties = [[]]
    property_data_split_len = len(property_data_split)
    for pindex in range(property_data_split_len):
        if counter == 0:
            mapped_properties[len(mapped_properties) - 1].extend(
                [
                    property_data_split[pindex],
                    STRUCT_UNPACK_SIG_SHORT(property_data_split[pindex][1:]),
                ]
            )
            counter = counter + 1
            continue
        counter = counter + 1

        mapped_properties[len(mapped_properties) - 1].append(
            property_data_split[pindex][1 : property_data_split[pindex][0] + 1]
        )
        if property_data_split_len == counter:
            break
        mapped_properties.append(
            [
                property_data_split[pindex][property_data_split[pindex][0] + 1 :],
                STRUCT_UNPACK_SIG_SHORT(property_data_split[pindex][property_data_split[pindex][0] + 2 :]),
            ]
        )

    windows_conjunction = window_data.replace(
        b"R\x00\x03ENDS", b"R\x00\x03R\x00\x03ENDSS"
    ).split(b"R\x00\x03ENDS")
    splitdata = []
    windows_conjunction_len = len(windows_conjunction)
    for co_index in range(windows_conjunction_len):
        firstpass = (
            windows_conjunction[co_index]
            .replace(b"MS\x00\x03R", b"MS\x00\x03RS\x00\x03R")
            .split(b"MS\x00\x03R")
        )
        splitdata.append(firstpass)
    for_regex = []
    properymap = {}
    len_mapped_properties = len(mapped_properties)
    for pro_index in range(len_mapped_properties):
        properymap[mapped_properties[pro_index][0]] = mapped_properties[pro_index][2]
        for_regex.append(b"(?:" + re.escape(mapped_properties[pro_index][0]) + b")")
    string_columns_none={
        v: None for v in (properymap.values())
    }
    joined_regex_re = re.compile(b"(" + b"|".join(for_regex) + b")")
    group_counter = 0
    member_counter = 0
    all_elements_sorted = {}
    val_spli_list = []
    len_splitdata = len(splitdata)
    for spl_data0_index in range(len_splitdata):
        if group_counter not in all_elements_sorted:
            all_elements_sorted[group_counter] = {}
        member_counter = 0
        len_splitdata_spl_data0_index = len(splitdata[spl_data0_index])
        for spl_data1_index in range(len_splitdata_spl_data0_index):
            if member_counter not in all_elements_sorted[group_counter]:
                all_elements_sorted[group_counter][member_counter] = {}
                for dummyvalue in properymap.values():
                    all_elements_sorted[group_counter][member_counter][dummyvalue] = (
                        None
                    )
            splidata = joined_regex_re.split(
                splitdata[spl_data0_index][spl_data1_index]
            )
            if not splidata[0]:
                del splidata[0]
            if not splidata[len(splidata) - 1]:
                del splidata[len(splidata) - 1]
            for key_spli_val_spli_index in range(0, len(splidata) - 1, 2):
                key_spli = splidata[key_spli_val_spli_index]
                val_spli_list.clear()
                parsedata(
                    sbytes=splidata[key_spli_val_spli_index + 1],
                    resultlist=val_spli_list,
                )
                finalvalue = None
                if len(val_spli_list) == 1:
                    finalvalue = val_spli_list[0]
                elif len(val_spli_list) > 1:
                    finalvalue = val_spli_list
                    tmpval_spli_list = []
                    firstnonzero = False
                    val_spli_list_len = len(val_spli_list)
                    for tmval_index in range(val_spli_list_len - 1, -1, -1):
                        if val_spli_list[tmval_index] == 0 and not firstnonzero:
                            continue
                        tmpval_spli_list.append(val_spli_list[tmval_index])
                        firstnonzero = True
                    if not tmpval_spli_list:
                        finalvalue = 0
                    elif len(tmpval_spli_list) == 1:
                        finalvalue = tmpval_spli_list[0]
                    else:
                        finalvalue = tuple(reversed(tmpval_spli_list))
                all_elements_sorted[group_counter][member_counter][
                    properymap[key_spli]
                ] = finalvalue
            member_counter += 1
        group_counter += 1

    alldfs = []
    for k0, i0 in all_elements_sorted.items():
        for k1, i1 in i0.items():
            try:
                alldfs.append({**string_columns_none,**i1,**{'aa_group':k0,'aa_member':k1}})
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()
    df = pd.DataFrame(alldfs, dtype='object')
    df.columns = [
        (b"bb_"+remove_non_word_chars.sub(b'_', i).lower()).decode()
        if i not in ["aa_group", "aa_member"]
        else i
        for i in df.columns
    ]
    decview = df.loc[
         df[meta_name_column].str.contains(r"DecorView\s*$", na=False, regex=True)
    ].index
    if not len(decview)>0:
        df.drop(range(decview[0]), axis=0, inplace=True)
    df.dropna(axis=1, how="all", inplace=True)
    df=df.dropna(axis=0, how="all", inplace=False)
    df.loc[:, "aa_category"] = (
        df[meta_name_column]
        .str.rsplit("$", n=1)
        .apply(
            lambda h: pd.NA
            if not hasattr(h, "__len__")
            else h[1]
            if len(h) == 2
            else "RealItem"
        )
    )
    realitemindexlist = np.array_split(
        df.index.__array__(),
        (df.loc[df.aa_category == "RealItem"].index.__array__() + 1),
    )
    for indi in range(len(realitemindexlist)):
        df.loc[realitemindexlist[indi], "aa_subelements"] = indi
    return df


def parse_window_elements(dfx,adbexe='',device_serial='', str dump_cmd="cmd window dump-visible-window-views"):
    adbsh = UniversalADBExecutor(
            adb_path=adbexe,
            device_serial=device_serial,
        )
    stdout, stderr, returncode = (
        adbsh.shell_with_capturing_import_stdout_and_stderr(
            command=dump_cmd,
            debug=False,
            ignore_exceptions=True,
        )
    )
    if iswindows:
        zipfilepath = stdout.replace(b"\r\n", b"\n")
    else:
        zipfilepath = stdout
    zipname_zipdata = extract_files_from_zip(zipfilepath)
    len_zipname_zipdata = len(zipname_zipdata)
    for zip_index in range(len_zipname_zipdata):
        try:
            df = parse_screen_elements(
                            zipname_zipdata[zip_index][1]
                        )
            df8=concat_frames(df,dfx,meta_name_column = "bb_meta___hash__")
            if not df8.empty:
                return df8
        except Exception:
            if config_settings.debug_enabled:
                errwrite()
    return pd.DataFrame()

def parse_fragment_eles(
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
        bint debug=True,):
    dfx= cythonevparser.evparse.parse_fragments_active_screen(
        serial= serial,
        adb_path= adb_path,
        number_of_max_views= number_of_max_views,
        screen_width= screen_width,
        screen_height= screen_height,
        subproc_shell= subproc_shell,
        with_children= with_children,
        add_screenshot= add_screenshot,
        screenshot_kwargs= screenshot_kwargs,
        add_input_tap= add_input_tap,
        input_tap_center_x= input_tap_center_x,
        input_tap_center_y= input_tap_center_y,
        input_tap_input_cmd= input_tap_input_cmd,
        input_tap_kwargs= input_tap_kwargs,
        sendevent_mouse_move_start_x= sendevent_mouse_move_start_x,
        sendevent_mouse_move_start_y= sendevent_mouse_move_start_y,
        sendevent_mouse_move_end_x= sendevent_mouse_move_end_x,
        sendevent_mouse_move_end_y= sendevent_mouse_move_end_y,
        sendevent_mouse_move_y_max= sendevent_mouse_move_y_max,
        sendevent_mouse_move_x_max= sendevent_mouse_move_x_max,
        sendevent_mouse_move_inputdev= sendevent_mouse_move_inputdev,
        sendevent_mouse_move_add= sendevent_mouse_move_add,
        sendevent_mouse_move_kwargs= sendevent_mouse_move_kwargs,
        sendevent_mouse_move_su_exe= sendevent_mouse_move_su_exe,
        sendevent_mouse_move_sh_device= sendevent_mouse_move_sh_device,
        sendevent_mouse_move_cwd_on_device= sendevent_mouse_move_cwd_on_device,
        sendevent_mouse_move_qty_blocks= sendevent_mouse_move_qty_blocks,
        debug= debug,
    )

    dfx.loc[:, meta_name_column] = dfx.aa_mid.apply(_convert_to_int)
    return dfx

def concat_frames(df,dfx,str meta_name_column = "bb_meta___hash__"):
    meta_name_column = "bb_meta___hash__"
    df2 = dfx.merge(df, on=meta_name_column)
    df7 = (
        pd.concat([df2, df.loc[~df[meta_name_column].isin(dfx[meta_name_column])]])
        .sort_values(by=["aa_group", "aa_member", "aa_subelements"])
        .assign(
            aa_subelements1=lambda xx: xx.aa_subelements,
            aa_subelements2=lambda xx: xx.aa_subelements,
        )
        .groupby(["aa_subelements1"])
        .ffill()
        .groupby(["aa_subelements2"])
        .bfill()
    )
    return (
        df7.loc[~df7["aa_start_x"].isna()]
        .dropna(
            axis=1,
            how="all",
        )
        .reset_index(drop=True)
    )
