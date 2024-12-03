#pragma once

#include "logger.h"

template <typename T> struct Vec2D
{
    T x;
    T y;
};

using Int2D = Vec2D<int>;

template <> void Logger::Print(const Int2D &pos);

template <typename T> struct Range
{
    T low;
    T high;

    bool Contains(const T &pos) const
    {
        return low <= pos && pos <= high;
    }
};

using IntRange = Range<int>;

template <> void Logger::Print(const IntRange &rng);

template <typename T> struct Aabb
{
    Range<T> xRange;
    Range<T> yRange;

    bool Contains(const Vec2D<T> &pos) const
    {
        return xRange.Contains(pos.x) && yRange.Contains(pos.y);
    }
};

using IntAabb = Aabb<int>;