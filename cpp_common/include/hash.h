#pragma once

#include <stdint.h>

#include "span.h"
#include "buffer.h"

// internal, probably?
constexpr uint64_t _hashOffsetBasis = 14695981039346656037ULL;
uint64_t MurmurHash64A(const void* key, int len, uint64_t seed);

// basic version
template<typename T> uint64_t Hash(const T& value) {
	return MurmurHash64A(&value, sizeof(T), _hashOffsetBasis);
}

template<typename T> uint64_t Hash(const Span<T>& value) {
	return MurmurHash64A(value.begin(), sizeof(T) * value.Size(), _hashOffsetBasis);
}

template<typename T> uint64_t Hash(const Buffer<T>& value) {
	return MurmurHash64A(value.begin(), sizeof(T) * value.Size(), _hashOffsetBasis);
}

inline uint64_t HashMerge(uint64_t a, uint64_t b) {
	return a ^ (b << 1);
}