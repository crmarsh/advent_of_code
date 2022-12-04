#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// returns non-zero if given whitespace character
int IsWhitespace(char c)
{
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

char *SkipWhitespace(char *curr)
{
    while (*curr && IsWhitespace(*curr))
    {
        curr++;
    }
    return curr;
}

// Removes leading and trailing whitespace in place, returns resulting string length
size_t StripWhitespace(char *buffer)
{
    size_t n = strlen(buffer);
    int read_index = 0;
    char c;
    while ((c = buffer[read_index]) != 0)
    {
        if (!IsWhitespace(c))
        {
            break;
        }
        read_index++;
    }
    if (read_index != 0)
    {
        memmove(buffer, &buffer[read_index], n - read_index);
        n -= read_index;
    }
    for (read_index = (int)n - 1; read_index >= 0; --read_index)
    {
        c = buffer[read_index];
        if (IsWhitespace(c))
        {
            buffer[read_index] = 0;
        }
        else
        {
            break;
        }
    }
    return n;
}

// Find the size, allocate a buffer, read the file into it. Returns allocated buffer on success, else null.
char *LoadFile(const char *fname)
{
    FILE *fp = fopen(fname, "rb");
    if (!fp)
    {
        fprintf(stderr, "Error: file %s not found\n", fname);
        return NULL;
    }
    fseek(fp, 0, SEEK_END);
    size_t n = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    char *buffer = malloc(n + 1);
    if (!buffer)
    {
        fclose(fp);
        fprintf(stderr, "Error: Could not allocate %zu bytes for file %s\n", n, fname);
        return NULL;
    }
    size_t bytesRead = fread(buffer, 1, n, fp);
    fclose(fp);
    if (bytesRead != n)
    {
        free(buffer);
        fprintf(stderr, "Error: for file %s, should have %zu bytes but only read %zu\n", fname, n, bytesRead);
        return NULL;
    }
    buffer[n] = 0;
    return buffer;
}

typedef struct LineIterator
{
    char *source;
    char *sourceEnd;
    char *curr;
    char *currEnd;
    char *next;
} LineIterator;

void Iterate(LineIterator *it)
{
    it->curr = it->next;
    it->currEnd = strchr(it->curr + 1, '\n');
    if (!it->currEnd)
    {
        it->currEnd = it->sourceEnd;
        it->next = it->sourceEnd;
    }
    else
    {
        *(it->currEnd) = 0;
        it->next = SkipWhitespace(it->currEnd + 1);
    }
}

LineIterator IterateLines(char *buffer)
{
    LineIterator it;
    it.source = buffer;
    it.sourceEnd = buffer + strlen(buffer);
    it.next = buffer;
    Iterate(&it);
    return it;
}

int IteratorDone(const LineIterator *it)
{
    return it->curr >= it->sourceEnd;
}

char *IteratorCurrent(const LineIterator *it)
{
    StripWhitespace(it->curr);
    return it->curr;
}

int main(int argc, char *argv[])
{
    const char *fname = "sample_input.txt";
    if (argc > 1)
    {
        fname = argv[1];
    }

    char *buffer = LoadFile(fname);
    if (!buffer)
    {
        return 1;
    }

    int firstLine = 1;
    int prevValue;
    int increases = 0;

    for (LineIterator it = IterateLines(buffer); !IteratorDone(&it); Iterate(&it))
    {
        char *line = IteratorCurrent(&it);
        int val = atoi(line);
        if (val == 0 && line[0] != '0')
        {
            continue;
        }
        if (firstLine)
        {
            firstLine = 0;
            prevValue = val;
            continue;
        }
        if (val > prevValue)
        {
            increases++;
        }
        prevValue = val;
    }
    printf("%d increases\n", increases);

    free(buffer);
    return 0;
}
