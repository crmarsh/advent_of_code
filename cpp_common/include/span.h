#pragma once

// reference to a range, does not own values pointed to
// this is just two pointers, should be okay to treat as a value type
template <typename T> class Span
{
  protected:
    const T *_start;
    const T *_end;

  public:
    Span() : _start(nullptr), _end(nullptr)
    {
    }

    Span(const T *start, const T *ending) : _start(start), _end(ending)
    {
    }

    /// <summary>
    /// Span from a false terminated array, computes the end
    /// </summary>
    Span(const T *start) : _start(start), _end(start)
    {
        while (*_end)
        {
            ++_end;
        }
    }

    Span(const Span<T> &other) : _start(other._start), _end(other._end)
    {
    }

    Span<T> &operator=(const Span<T> &other)
    {
        _start = other._start;
        _end = other._end;
        return *this;
    }

    const T *begin() const
    {
        return _start;
    }

    const T *end() const
    {
        return _end;
    }

    bool Empty() const
    {
        return _end <= _start;
    }

    T First() const
    {
        return *_start;
    }

    size_t Size() const
    {
        return (size_t)(_end - _start);
    }

    int StartOffsetFrom(const T *other) const
    {
        return (int)(_start - other);
    }

    size_t Count(const T &value) const
    {
        size_t valueCount = 0;
        for (const T *ptr = _start; ptr < _end; ++ptr)
        {
            if (value == *ptr)
            {
                ++valueCount;
            }
        }
        return valueCount;
    }
};
