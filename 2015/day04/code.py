import hashlib


mbase = hashlib.md5()


def hash_str(a):
    m = mbase.copy()
    m.update(a)
    return m.hexdigest()


def check_answer(secret_key, num):
    s = secret_key + str(num)
    h = hash_str(s.encode())
    return h.startswith('000000')


def main():
    input_key = 'ckczppom'
    test_value = 3938038 # 117946
    while not check_answer(input_key, test_value):
        test_value += 1
        if (test_value % 100000) == 0:
            print(test_value)
    print("found it:", test_value)


if __name__ == '__main__':
    main()
