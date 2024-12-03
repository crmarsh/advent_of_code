#pragma once

using String = Buffer<char>;
using StringRef = Span<char>;

String LoadSmallFile(const char *fileName);

template <typename IntType = int> IntType Atoi(StringRef digits)
{
    if (digits.Empty())
    {
        return 0;
    }
    if (digits.First() == '-')
    {
        return -Atoi(StringRef(digits.begin() + 1, digits.end()));
    }
    IntType result = 0;
    for (auto digit : digits)
    {
        if (digit < '0' || '9' < digit)
        {
            break;
        }
        IntType val = (IntType)(digit - '0');
        result = result * 10 + val;
    }
    return result;
}
