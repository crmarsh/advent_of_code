#include <string>
#include <fstream>
#include <filesystem>
#include <iostream>
#include <cstdlib>

using namespace std;

// Find the size, allocate a buffer, read the file into it. Returns allocated buffer on success, else null.
string LoadFile(const filesystem::path &p)
{
    if (!filesystem::exists(p))
    {
        return "";
    }
    auto fileSize = filesystem::file_size(p);
    string buffer(fileSize, 0);
    ifstream inFile(p);
    inFile.read(buffer.data(), fileSize);
    return buffer;
}

int main(int argc, char *argv[], char *env[])
{
    /*
    for (int i = 0; env[i]; ++i)
    {
        cout << "env " << env[i] << endl;
    }
    */

    cout << "current dir: " << filesystem::current_path() << endl;

    const char *fname = "sample_input.txt";
    if (argc > 1)
    {
        fname = argv[1];
    }

    cout << "Loading input " << fname << endl;

    auto buffer = LoadFile(fname);

    cout << "Hello, world " << buffer.size() << "\n";

    return 0;
}