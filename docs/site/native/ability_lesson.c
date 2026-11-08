/* Original ability-only teaching module. No pathname policy or device I/O. */
#include <sys/neutrino.h>
#include <sys/procmgr.h>
#include <stdint.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
int main(int argc,char **argv){
 if(argc!=2 || (strcmp(argv[1],"deny") && strcmp(argv[1],"allow")))return 2;
 int deny=!strcmp(argv[1],"deny");
 unsigned domains=PROCMGR_ADN_ROOT|PROCMGR_ADN_NONROOT;
 unsigned end=domains|PROCMGR_AOP_DENY|PROCMGR_AOP_LOCK|PROCMGR_AID_EOL;
 int setup;
 if(deny)setup=procmgr_ability(0,end);
 else setup=procmgr_ability(0,domains|PROCMGR_AOP_ALLOW|PROCMGR_AOP_SUBRANGE|PROCMGR_AOP_LOCK|PROCMGR_AID_IO,(uint64_t)0,(uint64_t)0,end);
 if(setup){printf("ABILITY_SETUP mode=%s rc=%d errno=%d\n",argv[1],setup,errno);return 2;}
 errno=0;int rc=ThreadCtl(_NTO_TCTL_IO_LEVEL,(void *)(uintptr_t)_NTO_IO_LEVEL_1),e=errno;
 printf("ABILITY_LESSON mode=%s io_subrange=%s others=deny-lock operation=IO_LEVEL_1 rc=%d errno=%d\n",argv[1],deny?"none":"0-0",rc,e);
 if(!rc && ThreadCtl(_NTO_TCTL_IO_LEVEL,(void *)(uintptr_t)_NTO_IO_LEVEL_NONE))return 3;
 return deny?!(rc==-1&&e==EPERM):rc!=0;
}
