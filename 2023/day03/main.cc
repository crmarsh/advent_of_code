
#include "common.h"

enum class InputType
{
    Dot = 0,
    Digit = 1,
    Symbol = 2,
    Gear = 3,
};

template <> void Logger::Print(const InputType &it)
{
    switch (it)
    {
    case InputType::Dot:
        Print("Dot");
        break;
    case InputType::Digit:
        Print("Digit");
        break;
    case InputType::Symbol:
        Print("Symbol");
        break;
    case InputType::Gear:
        Print("Gear");
        break;
    }
}

InputType ClassifyChar(const char &c)
{
    if (c == '.')
    {
        return InputType::Dot;
    }
    if (c == '*')
    {
        return InputType::Gear;
    }
    if ('0' <= c && c <= '9')
    {
        return InputType::Digit;
    }
    return InputType::Symbol;
}

bool KeepClassification(InputType c)
{
    return c != InputType::Dot;
}

struct NumberEntry
{
    int _number;
    int _length;
    Int2D _startPosition;
    IntAabb _bounds;
    bool _active;

    NumberEntry() = default;

    NumberEntry(int row, Span<char> line, Span<char> part)
    {
        _number = Atoi(part);
        _length = (int)part.Size();
        _startPosition.x = part.StartOffsetFrom(line.begin());
        _startPosition.y = row;
        _bounds.xRange.low = _startPosition.x - 1;
        _bounds.xRange.high = _startPosition.x + _length;
        _bounds.yRange.low = row - 1;
        _bounds.yRange.high = row + 1;
        _active = false;
    }
};

template <> void Logger::Print(const NumberEntry &entry)
{
    Printf("<%, %, %>", entry._number, entry._startPosition, entry._active ? "active" : "inactive");
}

int main(int argc, char *argv[])
{
    const char *fileName = argc > 1 ? argv[1] : "input.txt";

    auto buffer = LoadSmallFile(fileName);

    auto lines = Split<char>(buffer, '\n');

    Buffer<Int2D> symbolPositions(buffer.Size());
    Buffer<Int2D> gearPositions(buffer.Size());
    Buffer<NumberEntry> numberEntries(buffer.Size());

    auto row = 0;
    for (auto line : lines)
    {
        auto parts = Partition<char, InputType>(line, ClassifyChar, KeepClassification);

        for (auto part : parts)
        {
            auto c = ClassifyChar(part.First());
            if (c == InputType::Digit)
            {
                numberEntries.Append(NumberEntry(row, line, part));
            }
            else
            {
                auto pos = Int2D{part.StartOffsetFrom(line.begin()), row};
                symbolPositions.Append(pos);
                if (c == InputType::Gear)
                {
                    gearPositions.Append(pos);
                }
            }
        }

        ++row;
    }

    for (const auto &symPos : symbolPositions)
    {
        for (auto &entry : numberEntries)
        {
            if (entry._active)
            {
                continue;
            }
            if (entry._bounds.Contains(symPos))
            {
                entry._active = true;
            }
        }
    }

    int total = 0;
    for (const auto &entry : numberEntries)
    {
        if (!entry._active)
        {
            continue;
        }
        total += entry._number;
    }

    logger.Print(total);

    return 0;
}
