# CPS Blue Diamond Backend System

## Dependencies

- python-pexpect
- python-beaker
- python-psycopg2
- paramiko >= 1.7.7.1
- pycrypto >= 2.5
- requests                            0.14.2 version developed with
- reportlab >= 2.4
- python-webob >= 1.1.1

# Batch Billing Process Diagram

```mermaid
flowchart TD
    F1[//server/corporate/bd-transactions.YYYYMMDD/]
    F2[//server/export/bd/files/bd-daily-trans.txt/]
    F3[//server/corporate/bd-archive/bd-tarnsactions.YYYY.zip/]
    F4[//server/corporate/bd-daily-transactions.YYYYMMDD/]
    D1[(Pg trans table)]

    P1(ar-sync-trans)
    P2(sp-process-blue a=ANYN)
    P3(sp-process-blue a=AYNN)
    P4(sp-process-blue-daily)
    P5(ar-batch-daily-trans)
    P6(ehoaudit)
    P7(bd-billing)

    P6 --> P5
    P6 --> P4
    P7 --> P2
    P7 --> P3
    P7 --> P1
    P3 -->|Creates| F1
    F1 -->|Loaded By| P1
    F4 -->|Loaded By| P1
    P1 -->|Inserts Into| D1
    P1 -->|Archives Transaction File| F3
    P4 -->|Creates| F2
    P5 -->|Creates| F4
    P5 -->|Removes Records From| F2
```

