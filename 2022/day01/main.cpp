#include <cstdlib>
#include <cstdio>
#include <cstring>

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
    char *buffer = new char[n + 1];
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
        fprintf(stderr, "Error: for file %s, should have %zu bytes but only read %zu\n", fname, n, bytesRead);
        delete[] buffer;
        return NULL;
    }
    buffer[n] = 0;
    return buffer;
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

    printf("Hello, world %d", strlen(buffer));

    delete[] buffer;
    return 0;
}