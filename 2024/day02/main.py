#!/usr/bin/env python3

import pathlib

here = pathlib.Path(__file__).parent
in_file = here / "input.txt"


def load_input():
    reports = []
    with open(in_file, "r") as f:
        for line in f.readlines():
            report = [int(p) for p in line.split() if p != ""]
            if report:
                reports.append(report)
    return reports


def check_safety(report):
    diffs = [report[i] - report[i - 1] for i in range(1, len(report))]
    first_diff = diffs[0]
    for d in diffs:
        if d * first_diff < 0:
            return False
        if d == 0 or not -3 <= d <= 3:
            return False
    return True


def check_safety_removing_one(report):
    if check_safety(report):
        return True
    for i in range(len(report)):
        subreport = report[0:i] + report[i + 1 :]
        if check_safety(subreport):
            return True


def main(input):
    safe_count = 0
    alt_safe_count = 0
    for report in input:
        is_safe = check_safety(report)
        if is_safe:
            # print("safe", report)
            safe_count += 1
        else:
            alt_safe = check_safety_removing_one(report)
            if alt_safe:
                # print("altsafe", report)
                alt_safe_count += 1
            else:
                # print("unsafe", report)
                pass
            pass
    print("safe_count:", safe_count)
    print("safe or alt safe count:", safe_count + alt_safe_count)


if __name__ == "__main__":
    input = load_input()
    main(input)
