/* Original target-only acceptance client/supervisor. No emulated MMIO/model. */
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

static pid_t start(const char *path) {
    pid_t child=fork();
    if (child==0) { execl(path,path,(char *)NULL); _exit(127); }
    return child;
}
static int reap(pid_t child) {
    int status;
    if (child<0) return 1;
    while (waitpid(child,&status,0)<0) if (errno!=EINTR) return 1;
    return !(WIFEXITED(status) && WEXITSTATUS(status)==0);
}
static int command(const void *data, size_t length, int expected, int flags) {
    int fd=open("/dev/edu",O_WRONLY|flags);
    if (fd<0) { perror("accept open write"); return 1; }
    errno=0; ssize_t result=write(fd,data,length); int error=errno;
    close(fd);
    if (expected) return !(result==-1 && error==expected);
    return result!=(ssize_t)length;
}
static int result_is(const char *expected) {
    int fd=open("/dev/edu",O_RDONLY);
    if (fd<0) return 1;
    char data[32]; size_t used=0; ssize_t n;
    while ((n=read(fd,data+used,1))==1 && used<sizeof(data)-1) used++;
    close(fd);
    if (n<0 || used>=sizeof(data)-1) return 1;
    data[used]=0;
    return strcmp(data,expected)!=0;
}
static int tests(void) {
    struct stat info;
    if (stat("/dev/edu",&info)<0 || !S_ISCHR(info.st_mode) || (info.st_mode&0777)!=0660) return 1;
    int fd=open("/dev/edu",O_RDONLY); char one;
    if (fd<0) return 1;
    errno=0; ssize_t n=read(fd,&one,1); int error=errno; close(fd);
    if (n!=-1 || error!=EAGAIN) return 1;
    if (command("10\n",3,0,0) || result_is("3628800\n")) return 1;
    puts("EDU RESMGR write10/read3628800 PASS");
    if (command("0\n",2,0,0) || result_is("1\n")) return 1;
    if (command("12\n",3,0,0) || result_is("479001600\n")) return 1;
    if (command("-1\n",3,EINVAL,0) || command("13\n",3,ERANGE,0) ||
        command("1234",4,EMSGSIZE,0) || command("1x",2,EINVAL,0) ||
        command("1\0",2,EINVAL,0) || command("1",1,EAGAIN,O_NONBLOCK) ||
        command("",0,0,0) || result_is("479001600\n")) return 1;
    puts("EDU RESMGR invalid/range/oversize/NUL/nonblock/zero-I/O PASS");
    fd=open("/dev/edu",O_RDWR);
    if (fd<0) return 1;
    char text[32]={0};
    if (write(fd,"10\n",3)!=3 || read(fd,text,sizeof(text)-1)!=8 || strcmp(text,"3628800\n")) {
        close(fd); return 1;
    }
    if (read(fd,&one,1)!=0 || read(fd,&one,0)!=0) { close(fd); return 1; }
    close(fd);
    fd=open("/dev/edu",O_RDONLY);
    if (fd<0) return 1;
    if (read(fd,text,1)!=1 || text[0]!='3' || command("0\n",2,0,0)) { close(fd); return 1; }
    memset(text,0,sizeof(text));
    if (read(fd,text,sizeof(text)-1)!=7 || strcmp(text,"628800\n")) { close(fd); return 1; }
    close(fd);
    if (result_is("1\n")) return 1;
    puts("EDU RESMGR partial/EOF/same-fd/independent-snapshot PASS");
    return 0;
}
int main(void) {
    setvbuf(stdout,NULL,_IONBF,0);
    if (access("/dev/edu",F_OK)==0) { fputs("Refuse existing /dev/edu owner\n",stderr); return 1; }
    if (reap(start("/proc/boot/edu_probe_native"))) return 1;
    pid_t server=start("/proc/boot/edu_resmgr");
    if (server<0) return 1;
    int ready=0;
    for (int i=0;i<100;i++) {
        if (access("/dev/edu",F_OK)==0) { ready=1; break; }
        usleep(50000);
    }
    int rc=ready?tests():1;
    if (!ready) fputs("EDU RESMGR startup deadline\n",stderr);
    if (kill(server,SIGTERM)<0) { perror("owned resmgr stop"); rc=1; }
    /* Service default SIGTERM is expected; reap without claiming graceful cleanup. */
    int status;
    while (waitpid(server,&status,0)<0) if (errno!=EINTR) { rc=1; break; }
    if (access("/dev/edu",F_OK)==0) { fputs("EDU path retained after stop\n",stderr); rc=1; }
    puts(rc?"EDU RESMGR ACCEPT FAIL":"EDU RESMGR ACCEPT PASS (normal I/O only; robustness pending)");
    return rc;
}
