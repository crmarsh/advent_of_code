// cpp_common.cpp : Defines the functions for the static library.
//

#include "common.h"

Logger logger;

String LoadSmallFile(const char *fileName)
{
    auto fp = fopen(fileName, "r");
    if (!fp)
    {
        fprintf(stderr, "File not found: %s", fileName);
        return String();
    }
    String buffer;
    buffer.Read(fp);
    fclose(fp);
    return buffer;
}

template <> void Logger::Print(const Int2D &pos)
{
    Printf("(%, %)", pos.x, pos.y);
}

template <> void Logger::Print(const IntRange &rng)
{
    Printf("[%, %]", rng.low, rng.high);
}

size_t IsPrime(size_t n) {
	if (n < 2) {
		return false;
	}
	if (n == 2) {
		return true;
	}
	if ((n % 2) == 0) {
		return false;
	}
	for (auto k = 3; k <= n / k; k += 2) {
		if ((n % k) == 0) {
			return false;
		}
	}
	return true;
}
