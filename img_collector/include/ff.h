//
// Created by saber on 2016/12/15.
//

#ifndef WIZNET_FF_H
#define WIZNET_FF_H
#define _MAX_SS 512
#define DATA_BUF_SIZE 512
#include <dirent.h>
#include <stdio.h>
#include <stdint.h>
typedef unsigned int UINT;
typedef enum {
    FR_OK = 0,				/* (0) Succeeded */
    FR_DISK_ERR,			/* (1) A hard error occurred in the low level disk I/O layer */
    FR_INT_ERR,				/* (2) Assertion failed */
    FR_NOT_READY,			/* (3) The physical drive cannot work */
    FR_NO_FILE,				/* (4) Could not find the file */
    FR_NO_PATH,				/* (5) Could not find the path */
    FR_INVALID_NAME,		/* (6) The path name format is invalid */
    FR_DENIED,				/* (7) Access denied due to prohibited access or directory full */
    FR_EXIST,				/* (8) Access denied due to prohibited access */
    FR_INVALID_OBJECT,		/* (9) The file/directory object is invalid */
    FR_WRITE_PROTECTED,		/* (10) The physical drive is write protected */
    FR_INVALID_DRIVE,		/* (11) The logical drive number is invalid */
    FR_NOT_ENABLED,			/* (12) The volume has no work area */
    FR_NO_FILESYSTEM,		/* (13) There is no valid FAT volume */
    FR_MKFS_ABORTED,		/* (14) The f_mkfs() aborted due to any parameter error */
    FR_TIMEOUT,				/* (15) Could not get a grant to access the volume within defined period */
    FR_LOCKED,				/* (16) The operation is rejected according to the file sharing policy */
    FR_NOT_ENOUGH_CORE,		/* (17) LFN working buffer could not be allocated */
    FR_TOO_MANY_OPEN_FILES,	/* (18) Number of open files > _FS_SHARE */
    FR_INVALID_PARAMETER	/* (19) Given parameter is invalid */
} FRESULT;

FRESULT scan_files(char* path, char* buf, int * buf_len);
int get_filesize(char* path, char *filename);
FRESULT f_open (FILE** fp, const char* path, const char* mode);				/* Open or create a file */
FRESULT f_close (FILE* fp);											/* Close an open file object */
FRESULT f_read (FILE* fp, void* buff, UINT btr, UINT* br);			/* Read data from a file */
FRESULT f_write (FILE* fp, const void* buff, UINT btw, UINT* bw);	/* Write data to a file */
FRESULT f_mkdir (const char* dir, const char* path);								/* Create a sub directory */
FRESULT f_unlink(const char* path);

void save_img(char* path);
#endif //WIZNET_FF_H

