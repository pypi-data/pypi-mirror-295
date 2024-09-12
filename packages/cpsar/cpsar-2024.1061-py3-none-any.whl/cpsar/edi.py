""" Module to record EDI records """
import cpsar.runtime as R
import cpsar.util as U

def insert_all(batch_file_id):
    insert_aca(batch_file_id)
    insert_bridgepointe(batch_file_id)
    insert_bdstandard(batch_file_id)
    insert_creative_risk(batch_file_id)
    insert_ecm(batch_file_id)
    insert_fsbit(batch_file_id)
    insert_hill(batch_file_id)
    insert_liga(batch_file_id)
    insert_meadowbrook(batch_file_id)
    insert_mrm(batch_file_id)
    insert_nciga(batch_file_id)
    insert_saltlake(batch_file_id)
    insert_scmit(batch_file_id)
    insert_scsaf(batch_file_id)
    insert_scaoc(batch_file_id)
    insert_synergy(batch_file_id)
    insert_signal(batch_file_id)
    insert_uef(batch_file_id)

def insert_rebill(batch_file_id):
    insert_ecm(batch_file_id)
    insert_hill(batch_file_id)
    insert_liga(batch_file_id)
    insert_meadowbrook(batch_file_id)
    insert_mrm(batch_file_id)
    insert_nciga(batch_file_id)
    insert_scmit(batch_file_id)
    insert_scsaf(batch_file_id)
    insert_uef(batch_file_id)

def insert_creative_risk(batch_file_id):
    """ Create EDI file to send to Creative Risk """
    cursor = R.db.cursor()
    cursor.execute("""
         with sgroup as (
            select '70900' as group_number
            union
            select managed_group_number
            from managed_group where group_number = '70900'
         )
        select count(*)
        from trans
        join sgroup using(group_number)
        where batch_file_id=%s
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id, 'client': 'creative_risk_ncci'}
    cursor.execute(U.insert_sql('edi_file', args))
    args = {'batch_file_id': batch_file_id, 'client': '70900'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_ecm(batch_file_id):
    """ Create EDI file to send to ECM """
    cursor = R.db.cursor()
    cursor.execute("""
         with sgroup as (
            select '70024' as group_number
            union
            select managed_group_number
            from managed_group where group_number = '70024'
         )
        select count(*)
        from trans
        join sgroup using(group_number)
        where batch_file_id=%s
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id}

    # The new IVOS edi file
    args['client'] = '70024'
    cursor.execute(U.insert_sql('edi_file', args))

def insert_fsbit(batch_file_id):
    """ Create EDI file to send to fsbit """
    cursor = R.db.cursor()
    cursor.execute("""
        select count(*)
        from trans
        where group_number = '70846' and batch_file_id=%s
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id, 'client': 'fsbit'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_aca(batch_file_id):
    cursor = R.db.cursor()
    cursor.execute("""
         with sgroup as (
            select '70897' as group_number
            union
            select managed_group_number
            from managed_group where group_number = '70897'
         )
        select count(*)
        from trans
        join sgroup using(group_number)
        where batch_file_id=%s
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id, 'client': '70897'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_bridgepointe(batch_file_id):
    cursor = R.db.cursor()
    cursor.execute("""
         with sgroup as (
            select '70036' as group_number
            union
            select managed_group_number
            from managed_group where group_number = '70036'
         )
        select count(*)
        from trans
        join sgroup using(group_number)
        where batch_file_id=%s
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id, 'client': 'bridgepointe'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_bdstandard(batch_file_id):
    """ Create EDI file to send to fsbit """
    cursor = R.db.cursor()
    cursor.execute("""
         with sgroup as (
            select '70062' as group_number
            union
            select managed_group_number
            from managed_group where group_number = '70062'
         )
        select count(*)
        from trans
        join sgroup using(group_number)
        where batch_file_id=%s
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id, 'client': 'bdstandard'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_liga(batch_file_id):
    """ Create EDI file to send for LIGA if any transactions in the
     batch """
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT COUNT(*)
      FROM trans
      WHERE batch_file_id=%s AND group_number = '70076'
      """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return

    args = {'batch_file_id': batch_file_id, 'client': 'liga'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_meadowbrook(batch_file_id):
    # 70010 is parent
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM trans
        WHERE batch_file_id=%s
          AND group_number IN ('70017', '70010', '70020', '70014')
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id}
    cursor.execute(U.insert_sql('meadowbrook_edi_file', args))

def insert_mrm(batch_file_id):
    """ Create EDI file to send for SCSAF if any UEF transactions in the
     batch """
    cursor = R.db.cursor()
    cursor.execute("""
      with sgroup as (
        select '70005' as group_number
        union
        select managed_group_number
        from managed_group where group_number = '70005')
      select count(*)
      from trans
      join sgroup using(group_number)
      where batch_file_id=%s
      """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return

    args = {'batch_file_id': batch_file_id, 'client': 'mrm'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_hill(batch_file_id):
    # 56700 parent
    cursor = R.db.cursor()
    cursor.execute("""
     with sgroup (group_number) as (values
        ('56700'),
        ('57700'),
        ('70336'),
        ('70396'),
        ('59300'))
      select count(*)
      from trans
      join sgroup using(group_number)
      where batch_file_id=%s
      """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return

    args = {'batch_file_id': batch_file_id, 'client': 'hill'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_nciga(batch_file_id):
    """ Create EDI file to send for NCIGA if any transactions in the
     batch """
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT COUNT(*)
      FROM trans
      WHERE batch_file_id=%s AND group_number = '59000'
      """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return

    args = {'batch_file_id': batch_file_id}
    cursor.execute(U.insert_sql('nciga_edi_file', args))
    args['client'] = 'nciga'
    cursor.execute(U.insert_sql('edi_file', args))

def insert_scmit(batch_file_id):
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT COUNT(*)
      FROM trans
      WHERE batch_file_id=%s AND group_number='70636'
      """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return

    args = {'batch_file_id': batch_file_id}
    cursor.execute(U.insert_sql('scmit_edi_file', args))

def insert_scsaf(batch_file_id):
    """ Create EDI file to send for SCSAF if any UEF transactions in the
     batch """
     # 56600 parent group
     # need to go change module and carve out 70483
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT COUNT(*)
      FROM trans
      WHERE batch_file_id=%s AND group_number IN 
         ('56600', '70300', '70303', '70543', '70081', '70303', '70300')
      """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return

    args = {'batch_file_id': batch_file_id, 'group_number': '56600'}
    cursor.execute(U.insert_sql('scsaf_edi_file', args))

def insert_scaoc(batch_file_id):
    """ Create EDI file to send for SCSAF if any UEF transactions in the
     batch """
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT COUNT(*)
      FROM trans
      WHERE batch_file_id=%s AND group_number = '59100'
      """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return

    args = {'batch_file_id': batch_file_id, 'client': 'scaoc'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_saltlake(batch_file_id):
    """ Create EDI file to send for Salt Lake County in the batch """
    # 70765 is parent group
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT COUNT(*)
      FROM trans
      WHERE batch_file_id=%s AND group_number IN ('70765', '70768')
      """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return

    args = {'batch_file_id': batch_file_id, 'client': 'saltlake'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_synergy(batch_file_id):
    cursor = R.db.cursor()
    cursor.execute("""
         with sgroup as (
            select '70828' as group_number
            union
            select managed_group_number
            from managed_group where group_number = '70828'
         )
        select count(*)
        from trans
        join sgroup using(group_number)
        where batch_file_id=%s
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id, 'client': 'synergy'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_signal(batch_file_id):
    cursor = R.db.cursor()
    cursor.execute("""
         with sgroup as (
            select '71225' as group_number
            union
            select managed_group_number
            from managed_group where group_number = '71225'
         )
        select count(*)
        from trans
        join sgroup using(group_number)
        where batch_file_id=%s
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id, 'client': 'signal'}
    cursor.execute(U.insert_sql('edi_file', args))

def insert_uef(batch_file_id):
    # Create EDI file to send for UEF if any UEF transactions in the batch
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM trans
        WHERE batch_file_id=%s AND group_number = '70483'
        """, (batch_file_id,))
    if not cursor.fetchone()[0]:
        return
    args = {'batch_file_id': batch_file_id, 'group_number': '70483'}
    cursor.execute(U.insert_sql('scsaf_edi_file', args))
