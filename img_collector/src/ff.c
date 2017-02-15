//
// Created by saber on 2016/12/15.
//

#include "ff.h"
#include <dirent.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

FRESULT scan_files(char* path, char* buf, int * buf_len) {
    FILE * fp;
    char tmpstr[512]="ls -l ";
    strcat(tmpstr, path);
    fp=popen(tmpstr,"r");
    *buf_len=ftell(fp);
    fread(buf,1,*buf_len,fp);
    pclose(fp);
    return FR_OK;

}

void save_img(char* path){
    char tmpstr[512] = "sudo python ./save_img.py \"";
    char* p = strstr(path,"jpg");
    if(p!=NULL){
        strcat(tmpstr, path);
        strcat(tmpstr, "\"");
        printf(tmpstr);
        system(tmpstr);
    }
}
int get_filesize(char* path, char *filename){
    uint32_t path_len = strlen(path);
    uint32_t filename_len = strlen(path);
    char *filepath = malloc(path_len+filename_len+1);

    struct stat buf;
    stat( filepath, &buf );
    if(S_ISDIR(buf.st_mode)) {
        return 0;
    }else if(S_ISREG(buf.st_mode)){
        filepath = strcat(filepath, path);
        filepath = strcat(filepath, filename);
        FILE *fp;
        fp = fopen(filepath,"r");
        return ftell(fp);
    }
    return 0;
}
FRESULT f_open (FILE** fp, const char* path, const char* mode){
    *fp = fopen(path,mode);
    return FR_OK;
}
FRESULT f_close (FILE* fp){
    fclose(fp);
    return FR_OK;
}
FRESULT f_read (FILE* fp, void* buff, UINT btr, UINT* br){
    *br = fread(buff,1,btr, fp);
    return FR_OK;
}
FRESULT f_write (FILE* fp, const void* buff, UINT btw, UINT* bw){
    *bw = fwrite(buff, 1, btw, fp);
    return FR_OK;
}

FRESULT f_mkdir (const char* dir, const char* path){
    char tmppath[512] = {0};
    strcpy(tmppath, dir);
    strcat(tmppath, path);
    return mkdir(tmppath, 0755);
}

FRESULT f_unlink(const char* path){
    return remove(path);
}
