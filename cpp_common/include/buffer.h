#pragma once

#include <cstdio>
#include <initializer_list>

#include "span.h"

// buffer holder, resizable
template <typename T> class Buffer
{
protected:
    size_t _size;
    size_t _allocated;
    T *_buffer;

  public:
    Buffer() noexcept
    {
        _buffer = nullptr;
        _size = 0;
        _allocated = 0;
    }

    Buffer(std::initializer_list<T> il)
    {
        _size = _allocated = il.size();
        if (_size)
        {
            _buffer = new T[_allocated];
            T* insertAt = _buffer;
            for (const auto& item : il) {
                *insertAt++ = item;
            }
        }
        else
        {
            _buffer = nullptr;
        }
    }

    Buffer(const T fromArray[])
    {
        _size = _allocated = sizeof(fromArray) / sizeof(T);
        if (_size)
        {
            _buffer = new T[_allocated];
            memcpy(_buffer, fromArray, _size * sizeof(T));
        }
        else
        {
            _buffer = nullptr;
        }
    }

    Buffer(const Buffer<T> &other)
    {
        if (other._buffer)
        {
            _buffer = new T[other._allocated];
            _size = other._size;
            _allocated = other._allocated;
            memcpy(_buffer, other._buffer, _size * sizeof(T));
        }
        else
        {
            _buffer = nullptr;
            _size = 0;
            _allocated = 0;
        }
    }

    Buffer(Buffer<T> &&other) noexcept
    {
        _buffer = other._buffer;
        _size = other._size;
        _allocated = other._allocated;
        other._buffer = nullptr;
        other._size = 0;
        other._allocated = 0;
    }

    Buffer(size_t size)
    {
        _buffer = new T[size];
        _size = 0;
        _allocated = size;
    }

    Buffer<T> &operator=(const Buffer<T> &other)
    {
        if (_allocated < other._size)
        {
            if (_buffer)
            {
                delete[] _buffer;
            }
            _buffer = new T[other._size];
            _allocated = other._size;
        }
        _size = other._size;
        memcpy(_buffer, other._buffer, _size * sizeof(T));
    }

    ~Buffer()
    {
        if (_buffer)
        {
            delete[] _buffer;
        }
    }

    Span<T> AsSpan() const
    {
        return Span<T>(_buffer, _buffer + _size);
    }

    // this does not seem to work the way I expected
    operator Span<T>() const
    {
        return Span<T>(_buffer, _buffer + _size);
    }

    // support range-based for
    T *begin() const
    {
        return _buffer;
    }

    // support range-based for
    T *end() const
    {
        return _buffer + _size;
    }

    size_t Size() const
    {
        return _size;
    }

    void Resize(size_t n)
    {
        if (n <= _allocated)
        {
            _size = n;
        }
        else
        {
            T *resized = new T[n];
            if (_buffer)
            {
                fprintf(stderr, "Warning: doing a realloc\n");
                memcpy(resized, _buffer, _size * sizeof(T));
                delete[] _buffer;
            }
            _buffer = resized;
            _size = n;
            _allocated = n;
        }
    }

    // seek to beginning, read whole file into this buffer
    void Read(FILE *fp)
    {
        fseek(fp, 0, SEEK_END);
        // note, if file is not mutliple of T size, last one is truncated
        auto fileSize = ftell(fp) / sizeof(T);
        Resize(fileSize);
        fseek(fp, 0, SEEK_SET);
        // note: could be less than fileSize if not reading in binary mode
        _size = fread(_buffer, sizeof(T), fileSize, fp);
    }

    void Append(const T &value)
    {
        auto i = _size;
        Resize(_size + 1);
        _buffer[i] = value;
    }
};
