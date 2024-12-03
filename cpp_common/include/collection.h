#pragma once

#include "span.h"
#include "buffer.h"

template <typename T> Buffer<Span<T>> Split(const Span<T> thing, const T &splitOn, bool skipEmpty = false)
{
    Buffer<Span<T>> result(1 + thing.Count(splitOn));
    const T *ending = thing.end();
    const T *spanStart = thing.begin();
    for (const T *ptr = spanStart; ptr < ending; ++ptr)
    {
        if (splitOn == *ptr)
        {
            if (!skipEmpty || spanStart != ptr)
            {
                result.Append(Span<T>(spanStart, ptr));
            }
            spanStart = ptr + 1;
        }
    }
    if (!skipEmpty || spanStart != ending)
    {
        result.Append(Span<T>(spanStart, ending));
    }
    return result;
}

// Returns a set of spans of the original thing, partitioned by the classifier function result, keeping those
// that "keep" returns true for.
template <typename T, typename C>
Buffer<Span<T>> Partition(const Span<T> thing, C (*classifier)(const T &), bool (*keep)(C))
{
    Buffer<Span<T>> result(thing.Size());
    const T *ending = thing.end();
    const T *spanStart = thing.begin();
    if (ending <= spanStart)
    {
        return result;
    }
    auto prevClass = classifier(*spanStart);
    for (const T *ptr = spanStart + 1; ptr < ending; ++ptr)
    {
        auto currClass = classifier(*ptr);
        if (prevClass != currClass)
        {
            if (keep(prevClass))
            {
                result.Append(Span<T>(spanStart, ptr));
            }
            spanStart = ptr;
        }
        prevClass = currClass;
    }
    if (keep(prevClass))
    {
        result.Append(Span<T>(spanStart, ending));
    }
    return result;
}
