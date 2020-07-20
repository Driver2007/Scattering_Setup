/* menuSscan.h generated from menuSscan.dbd */

#ifndef INC_menuSscan_H
#define INC_menuSscan_H

typedef enum {
    sscanPAUS_Go                    /* GO */,
    sscanPAUS_Pause                 /* PAUSE */,
    sscanPAUS_NUM_CHOICES
} sscanPAUS;

typedef enum {
    sscanDSTATE_UNPACKED            /* UNPACKED */,
    sscanDSTATE_TRIG_ARRAY_READ     /* TRIG_ARRAY_READ */,
    sscanDSTATE_ARRAY_READ_WAIT     /* ARRAY_READ_WAIT */,
    sscanDSTATE_ARRAY_GET_CALLBACK_WAIT /* ARRAY_GET_CALLBACK_WAIT */,
    sscanDSTATE_RECORD_ARRAY_DATA   /* RECORD_ARRAY_DATA */,
    sscanDSTATE_SAVE_DATA_WAIT      /* SAVE_DATA_WAIT */,
    sscanDSTATE_PACKED              /* PACKED */,
    sscanDSTATE_POSTED              /* POSTED */,
    sscanDSTATE_NUM_CHOICES
} sscanDSTATE;

typedef enum {
    sscanP1NV_PV_OK                 /* PV OK */,
    sscanP1NV_No_PV                 /* No PV */,
    sscanP1NV_PV_NoRead             /* PV NoRead */,
    sscanP1NV_PV_xxx                /* PV illegal1 */,
    sscanP1NV_PV_NoWrite            /* PV NoWrite */,
    sscanP1NV_PV_yyy                /* PV illegal2 */,
    sscanP1NV_PV_NC                 /* PV BAD */,
    sscanP1NV_NUM_CHOICES
} sscanP1NV;

typedef enum {
    sscanP1AR_Absolute              /* ABSOLUTE */,
    sscanP1AR_Relative              /* RELATIVE */,
    sscanP1AR_NUM_CHOICES
} sscanP1AR;

typedef enum {
    sscanACQT_SCALAR                /* SCALAR */,
    sscanACQT_1D_ARRAY              /* 1D ARRAY */,
    sscanACQT_NUM_CHOICES
} sscanACQT;

typedef enum {
    sscanFAZE_IDLE                  /* IDLE */,
    sscanFAZE_INIT_SCAN             /* INIT_SCAN */,
    sscanFAZE_BEFORE_SCAN           /* DO:BEFORE_SCAN */,
    sscanFAZE_BEFORE_SCAN_WAIT      /* WAIT:BEFORE_SCAN */,
    sscanFAZE_MOVE_MOTORS           /* MOVE_MOTORS */,
    sscanFAZE_CHECK_MOTORS          /* WAIT:MOTORS */,
    sscanFAZE_TRIG_DETCTRS          /* TRIG_DETCTRS */,
    sscanFAZE_READ_DETCTRS          /* WAIT:DETCTRS */,
    sscanFAZE_RETRACE_MOVE          /* RETRACE_MOVE */,
    sscanFAZE_RETRACE_WAIT          /* WAIT:RETRACE */,
    sscanFAZE_AFTER_SCAN_DO         /* DO:AFTER_SCAN */,
    sscanFAZE_AFTER_SCAN_WAIT       /* WAIT:AFTER_SCAN */,
    sscanFAZE_SCAN_DONE             /* SCAN_DONE */,
    sscanFAZE_SCAN_PENDING          /* SCAN_PENDING */,
    sscanFAZE_PREVIEW               /* PREVIEW */,
    sscanFAZE_RECORD_SCALAR_DATA    /* RECORD SCALAR DATA */,
    sscanFAZE_NUM_CHOICES
} sscanFAZE;

typedef enum {
    sscanLINKWAIT_YES               /* Wait */,
    sscanLINKWAIT_NO                /* NoWait */,
    sscanLINKWAIT_NUM_CHOICES
} sscanLINKWAIT;

typedef enum {
    sscanFPTS_No                    /* NO */,
    sscanFPTS_Freeze                /* FREEZE */,
    sscanFPTS_NUM_CHOICES
} sscanFPTS;

typedef enum {
    sscanFFO_Use_F_Flags            /* USE F-FLAGS */,
    sscanFFO_Override               /* OVERRIDE */,
    sscanFFO_NUM_CHOICES
} sscanFFO;

typedef enum {
    sscanACQM_NORMAL                /* NORMAL */,
    sscanACQM_ACC                   /* ACCUMULATE */,
    sscanACQM_ADD                   /* ADD TO PREV */,
    sscanACQM_NUM_CHOICES
} sscanACQM;

typedef enum {
    sscanCMND_CLEAR_MSG             /* Clear msg */,
    sscanCMND_CHECK_LIMITS          /* Check limits */,
    sscanCMND_PREVIEW_SCAN          /* Preview scan */,
    sscanCMND_CLEAR_ALL_PVS         /* Clear all PV's */,
    sscanCMND_CLEAR_POS_PVS_ETC     /* Clear pos PV's, etc */,
    sscanCMND_CLEAR_POS_PVS         /* Clear pos PV's */,
    sscanCMND_CLEAR_POS_RDBK_PVS_ETC /* Clear pos&rdbk PV's, etc */,
    sscanCMND_CLEAR_POS_RDBK_PVS    /* Clear pos&rdbk PV's */,
    sscanCMND_NUM_CHOICES
} sscanCMND;

typedef enum {
    sscanNOYES_NO                   /* NO */,
    sscanNOYES_YES                  /* YES */,
    sscanNOYES_NUM_CHOICES
} sscanNOYES;

typedef enum {
    sscanP1SM_Linear                /* LINEAR */,
    sscanP1SM_Table                 /* TABLE */,
    sscanP1SM_On_The_Fly            /* FLY */,
    sscanP1SM_NUM_CHOICES
} sscanP1SM;

typedef enum {
    sscanPASM_Stay                  /* STAY */,
    sscanPASM_Start_Pos             /* START POS */,
    sscanPASM_Prior_Pos             /* PRIOR POS */,
    sscanPASM_Peak_Pos              /* PEAK POS */,
    sscanPASM_Valley_Pos            /* VALLEY POS */,
    sscanPASM_RisingEdge_Pos        /* +EDGE POS */,
    sscanPASM_FallingEdge_Pos       /* -EDGE POS */,
    sscanPASM_COM                   /* CNTR OF MASS */,
    sscanPASM_NUM_CHOICES
} sscanPASM;


#endif /* INC_menuSscan_H */
