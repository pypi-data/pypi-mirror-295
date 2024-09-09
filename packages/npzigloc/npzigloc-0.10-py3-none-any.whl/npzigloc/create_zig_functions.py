import os
this_folder = os.path.dirname(__file__)
zigoutput = os.path.join(this_folder, "zignpwherex.zig")

functionheader = r"""const std = @import("std");
extern fn malloc(usize) callconv(.C) ?[*]void;
extern fn free([*]usize) callconv(.C) void;

fn uf0(x: anytype, y: anytype) bool {
    return x < y;
}
fn uf1(x: anytype, y: anytype) bool {
    return x <= y;
}
fn uf2(x: anytype, y: anytype) bool {
    return x == y;
}
fn uf3(x: anytype, y: anytype) bool {
    return x >= y;
}
fn uf4(x: anytype, y: anytype) bool {
    return x > y;
}
fn uf5(x: anytype, y: anytype) bool {
    return x != y;
}

fn uf0_not(x: anytype, y: anytype) bool {
    return !(x < y);
}
fn uf1_not(x: anytype, y: anytype) bool {
    return !(x <= y);
}
fn uf2_not(x: anytype, y: anytype) bool {
    return !(x == y);
}
fn uf3_not(x: anytype, y: anytype) bool {
    return !(x >= y);
}
fn uf4_not(x: anytype, y: anytype) bool {
    return !(x > y);
}
fn uf5_not(x: anytype, y: anytype) bool {
    return !(x != y);
}
const func_pointers = [6]*const fn (anytype, anytype) bool{
    uf0,
    uf1,
    uf2,
    uf3,
    uf4,
    uf5,
};
export fn npwhere_argwhere_bool(array_address: usize, array_len: usize, address_np_shape: usize, np_shape_len: usize, resultsarray: usize) ?[*]usize {
    const thisdtype = [*]bool;
    const pointer_address_of_numpy_array: thisdtype = @ptrFromInt(array_address);
    var counter: usize = 0;
    const ptrvoid = malloc(array_len * @sizeOf(usize)) orelse return null;
    var ptr: [*]usize = @alignCast(@ptrCast(ptrvoid));
    defer free(ptr);

    for (0..array_len) |flat_index| {
        if (pointer_address_of_numpy_array[flat_index]) {
            ptr[counter] = flat_index;
            counter += 1;
        }
    }
    const ptrresult_void = malloc((np_shape_len * (counter) * @sizeOf(usize))) orelse return null;
    const result_array: [*]usize = @ptrFromInt(resultsarray);
    const myresult: [*]usize = convert2np(ptrresult_void, address_np_shape, np_shape_len, counter, ptr);
    result_array[0] = np_shape_len * (counter) * @sizeOf(usize);
    result_array[1] = @intFromPtr(ptrresult_void);
    return myresult;
}
fn convert2np(ptrresults: [*]void, address_np_shape: usize, np_shape_len: usize, counter: usize, ptr: [*]usize) [*]usize {
    @setFloatMode(.optimized);
    var ptrresultsx: [*]usize = @alignCast(@ptrCast(ptrresults));
    var var_get_out_0: usize = 0;
    var var_get_out_1: usize = 0;
    const pointer_np_shapep: [*]usize = @ptrFromInt(address_np_shape);
    const len_of_numpy_shape_array_minus_1: usize = np_shape_len - 1;
    var ptrresultscounter: usize = 0;
    const pointer_np_shape = init: {
        var init_value: [32]usize = undefined;
        for (init_value, 0..) |_, i| {
            init_value[i] = pointer_np_shapep[i];
        }
        break :init init_value;
    };
    for (0..counter) |i| {
        var_get_out_0 = ptr[i];
        for (0..np_shape_len) |shape_index| {
            var_get_out_1 = @divFloor(var_get_out_0, pointer_np_shape[len_of_numpy_shape_array_minus_1 - shape_index]);
            ptrresultsx[ptrresultscounter] += @mod(var_get_out_0, pointer_np_shape[len_of_numpy_shape_array_minus_1 - shape_index]);
            ptrresultscounter += 1;
            var_get_out_0 = var_get_out_1;
        }
    }
    return ptrresultsx;
}
export fn flatten_index(address_np_shape: usize, np_shape_len: usize, counter: usize, resultsarray: usize) ?[*]usize {
    @setFloatMode(.optimized);
    const ptrvoid = malloc(np_shape_len * counter * @sizeOf(usize)) orelse return null;
    var ptrresultsx: [*]usize = @alignCast(@ptrCast(ptrvoid));
    var var_get_out_0: usize = 0;
    var var_get_out_1: usize = 0;
    const pointer_np_shapep: [*]usize = @ptrFromInt(address_np_shape);
    const len_of_numpy_shape_array_minus_1: usize = np_shape_len - 1;
    var ptrresultscounter: usize = 0;
    const pointer_np_shape = init: {
        var init_value: [32]usize = undefined;
        for (init_value, 0..) |_, i| {
            init_value[i] = pointer_np_shapep[i];
        }
        break :init init_value;
    };
    for (0..counter) |i| {
        var_get_out_0 = i;
        for (0..np_shape_len) |shape_index| {
            var_get_out_1 = @divFloor(var_get_out_0, pointer_np_shape[len_of_numpy_shape_array_minus_1 - shape_index]);
            ptrresultsx[ptrresultscounter] += @mod(var_get_out_0, pointer_np_shape[len_of_numpy_shape_array_minus_1 - shape_index]);
            ptrresultscounter += 1;
            var_get_out_0 = var_get_out_1;
        }
    }
    const result_array: [*]usize = @ptrFromInt(resultsarray);
    result_array[0] = np_shape_len * (counter) * @sizeOf(usize);
    result_array[1] = @intFromPtr(ptrresultsx);
    return ptrresultsx;
}

"""
# FUNCTIONZIG_DATATYPEZIG
# const thisdtype = [*]DATATYPEZIG;
# const thisdtype_no_pointer = DATATYPEZIG;
zigfuncraws=[]
#zigfunction = "npwhere_argwhere"
zigfuncraws.append(
    {
        "npwhere_argwhere": {
            "zigfuncraw": R"""export fn FUNCTIONZIG_DATATYPEZIG(array_address: usize, search_for: usize, array_len: usize, operation: usize, address_np_shape: usize, np_shape_len: usize, resultsarray: usize) ?[*]usize {
    const thisdtype = [*]DATATYPEZIG;
    const thisdtype_no_pointer = DATATYPEZIG;
    const pointer_address_of_numpy_array: thisdtype = @ptrFromInt(array_address);
    const pointer_value_to_search_for: thisdtype = @ptrFromInt(search_for);
    const real_value_to_search_for: thisdtype_no_pointer = pointer_value_to_search_for[0];
    var counter: usize = 0;
    const ptrvoid = malloc(array_len * @sizeOf(usize)) orelse return null;
    var ptr: [*]usize = @alignCast(@ptrCast(ptrvoid));
    defer free(ptr);
    inline for (0..func_pointers.len) |i| {
        if (operation == i) {
            for (0..array_len) |flat_index| {
                if (func_pointers[i](pointer_address_of_numpy_array[flat_index], real_value_to_search_for)) {
                    ptr[counter] = flat_index;
                    counter += 1;
                }
            }
        }
    }
    const ptrresult_void = malloc((np_shape_len * (counter) * @sizeOf(usize))) orelse return null;
    const result_array: [*]usize = @ptrFromInt(resultsarray);
    const myresult: [*]usize = convert2np(ptrresult_void, address_np_shape, np_shape_len, counter, ptr);
    result_array[0] = np_shape_len * (counter) * @sizeOf(usize);
    result_array[1] = @intFromPtr(ptrresult_void);
    return myresult;
}"""
        }
    }
)
zigfuncraws.append(
    {
        "np_boolean_numpy_array": {
            "zigfuncraw": R"""export fn FUNCTIONZIG_DATATYPEZIG(array_address: usize, search_for: usize, array_len: usize, operation: usize, resultsarray: usize) void {
    const thisdtype = [*]DATATYPEZIG;
    const thisdtype_no_pointer = DATATYPEZIG;
    const pointer_address_of_numpy_array: thisdtype = @ptrFromInt(array_address);
    const pointer_value_to_search_for: thisdtype = @ptrFromInt(search_for);
    const real_value_to_search_for: thisdtype_no_pointer = pointer_value_to_search_for[0];
    const ptr: [*]u8 = @ptrFromInt(resultsarray);
    inline for (0..func_pointers.len) |i| {
        if (operation == i) {
            for (0..array_len) |flat_index| {
                if (func_pointers[i](pointer_address_of_numpy_array[flat_index], real_value_to_search_for)) {
                    ptr[flat_index] += 1;
                }
            }
        }
    }
}
"""
        }
    }
)
zigdatatypes = [
    "c_int",
    "c_int",
    "c_uint",
    "c_uint",
    "c_char",
    "u8",
    "c_short",
    "c_ushort",
    "c_longlong",
    "c_ulonglong",
    "f32",
    "f64",
    "f128",
]
numpy_short_dtypes = [
    "i",
    "l",
    "L",
    "I",
    "b",
    "B",
    "h",
    "H",
    "q",
    "Q",
    "f",
    "d",
    "D",
]


collectedfunctions=[]
# from rich import print
for each_function in zigfuncraws:
    allfunctions = {}
    for zigfunction, fuval in each_function.items():
        zigfuncraw=fuval["zigfuncraw"]
        for zigdatatype, numpy_short_dtype in zip(zigdatatypes, numpy_short_dtypes):
            zigfuncdtyped = zigfuncraw.replace("DATATYPEZIG", zigdatatype).replace(
                "FUNCTIONZIG", zigfunction
            )
            allfunctions[numpy_short_dtype] = {
                "funcname": zigfunction + "_" + zigdatatype,
                "func": zigfuncdtyped,
            }
    collectedfunctions.append(allfunctions)
with open(zigoutput, "w") as myfile:
    myfile.write(functionheader)
    for allfunctions in collectedfunctions:
        allfus = sorted({h["func"] for h in allfunctions.values()})
        for f in allfus:
            #print(f)
            myfile.write(f + "\n")

        print("functiondict={")
        for k, v in allfunctions.items():
            print(f""""{k}":"{v["funcname"]}",""")

        print("}")

        print("functiondict={")
        for k, v in allfunctions.items():
            print(f""""{v["funcname"]}":["{v["funcname"]}",1],""")

        print("}")