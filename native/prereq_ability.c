#include <sys/neutrino.h>
#include <sys/procmgr.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
/* Ability control only; not pathname policy. Separate process per mode. */
int main(int argc,char **argv) {
 int deny=argc==2 && !strcmp(argv[1],"deny");
 if(deny && procmgr_ability(0,PROCMGR_ADN_ROOT|PROCMGR_ADN_NONROOT|PROCMGR_AOP_DENY|PROCMGR_AOP_LOCK|PROCMGR_AID_IO,PROCMGR_AID_EOL)==-1){printf("DROP_FAILED errno=%d\n",errno);return 2;}
 errno=0;int rc=ThreadCtl(_NTO_TCTL_IO_LEVEL,(void *)(uintptr_t)_NTO_IO_LEVEL_1);int e=errno;
 printf("ABILITY mode=%s operation=ThreadCtl_IO_LEVEL_1 rc=%d errno=%d\n",deny?"deny":"default",rc,e);
 if(!rc)ThreadCtl(_NTO_TCTL_IO_LEVEL,(void *)(uintptr_t)_NTO_IO_LEVEL_NONE);
 return deny ? !(rc==-1 && e==EPERM) : rc!=0;
}
