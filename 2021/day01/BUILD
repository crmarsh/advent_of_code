load("@rules_cc//cc:defs.bzl", "cc_binary")
load("//cpp_common:cpp_variables.bzl", "COPTS")

cc_binary(
    name = "solution",
    copts = COPTS,
    srcs = ["main.c"],
)

exports_files(["input.txt"])
