load("@rules_cc//cc:defs.bzl", "cc_binary")
load("//cpp_common:cpp_variables.bzl", "CPPOPTS")

cc_binary(
    name = "solution",
    copts = CPPOPTS,
    srcs = ["main.cpp"],
    data = [":inputs"],
)

filegroup(
    name = "inputs",
    data = glob(["*.txt"]),
    visibility = ["//visibility:public"],
)
