def paper_needed(l, w, h):
    s0 = l * w
    s1 = l * h
    s2 = w * h
    extra = min([s0, s1, s2])
    return extra + 2 * s0 + 2 * s1 + 2 * s2


def ribbon_needed(l, w, h):
    f0 = 2 * l + 2 * w
    f1 = 2 * l + 2 * h
    f2 = 2 * w + 2 * h
    bow = l * w * h
    return bow + min([f0, f1, f2])


def main():
    with open("input.txt", "r") as f:
        total_paper = 0
        total_ribbon = 0
        for line in f:
            dims = line.split("x")
            if len(dims) != 3:
                continue
            dims = [a for a in map(int, dims)]
            total_paper += paper_needed(*dims)
            total_ribbon += ribbon_needed(*dims)
        print("total_paper:", total_paper)
        print("total_ribbon:", total_ribbon)


if __name__ == "__main__":
    main()
