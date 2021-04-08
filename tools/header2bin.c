#define HEADER_INCLUDE  "../include/truemove3.h"
#define ARRAY_NAME      truemove3

#include <stdio.h>
#include <stdlib.h>
#include HEADER_INCLUDE

int main()
{
    FILE *fptr;

    fptr = fopen("h2b_output.bin","wb");

    if(fptr == NULL)
    {
        printf("Could not open binary.");
        exit(1);
    }

    for(size_t i = 0; i < sizeof(ARRAY_NAME); i++)
    {
        unsigned char byte = ARRAY_NAME[i];
        fwrite(&byte, sizeof(byte), 1, fptr);
    }

    fclose(fptr);

    exit(0);
}