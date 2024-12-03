#pragma once

#include "buffer.h"
#include "hash.h"

template<typename KeyType, typename ValueType> class Map {
	const size_t kMinSize = 7;
	const double kMaxLoadFactor = 0.75;

public:
	struct Entry {
		size_t _hash; // store this?
		KeyType _key;
		ValueType _value;

		Entry() {
			_hash = 0;
		}

		Entry(KeyType key, ValueType val) : _key(key), _value(val) {
			_hash = Hash(key);
		}

		Entry(const Entry& other) = default;
		Entry(Entry&& other) = default;
	};

private:
	Buffer<Entry> _table;
	
public:
	Map(size_t size = kMinSize) : _size(0), _allocated(size), _table(new Entry[_allocated]) {}

	~Map() = default;

	ValueType& Add(KeyType key, ValueType val) {
		if ((double)(_size + 1) / (double)_table.All
	}
};
