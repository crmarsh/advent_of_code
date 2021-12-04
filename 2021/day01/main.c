#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    const char *fname = "sample_input.txt";
    if (argc > 1)
    {
        fname = argv[1];
    }
    FILE *fp = fopen(fname, "r");
    if (!fp)
    {
        printf("Error: file %s not found\n", fname);
        return 1;
    }

    char buffer[1024];
    while (fgets(buffer, sizeof(buffer), fp))
    {
        printf("line: %s\n", buffer);
    }

    return 0;
}
