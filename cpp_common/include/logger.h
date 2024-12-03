#pragma once

#include <cstdio>

class Logger
{
    FILE *ownedTarget;
    FILE *ownedErrTarget;

  public:
    FILE *target;
    FILE *errTarget;

    Logger()
    {
        target = stdout;
        errTarget = stderr;
        ownedTarget = ownedErrTarget = nullptr;
    }

    void CloseOutput()
    {
        if (ownedTarget)
        {
            fclose(ownedTarget);
        }
        target = stdout;
    }

    void CloseErrorOutput()
    {
        if (ownedErrTarget)
        {
            fclose(ownedErrTarget);
        }
        errTarget = stderr;
    }

    ~Logger()
    {
        CloseOutput();
        CloseErrorOutput();
    }

    void OpenOutput(const char *fname, bool append = false)
    {
        CloseOutput();
        ownedTarget = fopen(fname, append ? "a" : "w");
        if (ownedTarget)
        {
            target = ownedTarget;
        }
    }

    void OpenErrorOutput(const char *fname, bool append = false)
    {
        CloseErrorOutput();
        ownedErrTarget = fopen(fname, append ? "a" : "w");
        if (ownedErrTarget)
        {
            errTarget = ownedTarget;
        }
    }

    template <typename T> void Print([[maybe_unused]] const T &val)
    {
        fputs("not sure how to print that\n", errTarget);
    }

    void Print(const char *s)
    {
        fputs(s, target);
    }

    void Print(const char &c)
    {
        fputc(c, target);
    }

    void Print(const double &x)
    {
        fprintf(target, "%lf", x);
    }

    void Print(const int &i)
    {
        fprintf(target, "%d", i);
    }

    void Print(const Span<char> &spanValues)
    {
        fwrite(spanValues.begin(), 1, spanValues.Size(), target);
    }

    template <typename T> void PrintList(const Span<T> &spanValues, const char *separator = "")
    {
        bool first = true;
        for (const auto &val : spanValues)
        {
            if (!first && separator && separator[0])
            {
                Print(separator);
            }
            Print(val);
            first = false;
        }
        Print('\n');
    }

    template <typename T> void Print(const Span<T> &spanValues)
    {
        PrintList(spanValues, ", ");
    }

    template <typename T> void Print(const Buffer<T> &buff)
    {
        PrintList(buff.AsSpan(), ", ");
    }

    template <typename T> void PrintList(const Buffer<T> &buff, const char *separator = "")
    {
        PrintList(buff.AsSpan(), separator);
    }

    template <typename T> void Println(const T &val)
    {
        Print(val);
        Print('\n');
    }

    template <typename T, typename... Targs> void Print(const T &value, Targs... Fargs)
    {
        Print(value);
        Print(' ');
        Print(Fargs...);
    }

    void Printf(const char *format)
    {
        Print(format);
    }

    template <typename T, typename... Targs> void Printf(const char *format, T value, Targs... Fargs)
    {
        for (; *format; ++format)
        {
            if (*format == '\\')
            {
                ++format;
            }
            else if (*format == '%')
            {
                Print(value);
                Printf(format + 1, Fargs...);
                return;
            }
            Print(*format);
        }
    }
};

extern Logger logger;
