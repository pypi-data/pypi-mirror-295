def vishayTable(parts):
    query= f"""
             SELECT PARTS AS VISHAY_PARTS, 'Vishay' AS VISHAY_MAN, LOWER_PART
             FROM VISHAY_STATUS_PARTS
             WHERE (LOWER_PART) IN ({parts})"""
    return query

def deleteTable(parts):
    query = fr"""
            SELECT PART_NUMBER, SUPPLIER, ISSUE_TYPE, MORE_DETAILS, CORRECT_PART, CORRECT_SUPPLIER, INSERTION_DATE
            FROM EMAILSYS.NEW_WRONG_PNS @ AUTO dal 
            WHERE LOWER(PART_NUMBER) IN ({parts})
            """
    return query

def componentTable(parts):
    query= fr"""
             SELECT  C.COM_ID,
                     C.COM_PARTNUM,
                     cm.get_man_name(C.MAN_ID) AS MAN_NAME ,
                     cm.get_pl_name(C.PL_id)   AS PL_Name  ,
                     cm.get_PDF_URL(C.PDF_id)  AS Datasheet,
                     C.COM_DESC AS DESCRIPTION,
                     C.LC_STATE AS Lifecycle_Status
             FROM cm.xlp_se_component  C
             WHERE C.COM_PARTNUM IN ({parts})"""
    return query

def pcnTable(parts):
    query= fr"""
            SELECT pcn.AFFECTED_PRODUCT_NAME AS PCN_PART, cm.get_man_name(pcf.MAN_ID) AS PCN_MAN_NAME, pcf.NOTIFICATION_DATE, cm.get_PDF_URL(pcn.PCN_ID) AS PCN_URL    
            FROM cm.tbl_pcn_parts pcn
            LEFT JOIN cm.tbl_pcn_distinct_feature pcf ON pcn.PCN_ID = pcf.PCN_ID
            WHERE pcn.AFFECTED_PRODUCT_NAME IN ({parts})
            AND pcf.GIDEP_NO = 'Trusted'
            AND pcn.PCN_SOURCE != 'Arrow'                
            """
    return query

def arrowTable(parts):
    query= fr"""
             SELECT PART_NUMBER AS "Arrow Price List", cm.get_man_name(MAN_ID) AS ARROW_MAN_NAME
             FROM UpdateSys.TBL_ARROW_PRICINGDATA @DB8
             WHERE (PART_NUMBER) IN ({parts})"""
    return query

def lifecycleTable(COM_ID):
    query= fr"""
             SELECT lc.COM_ID AS LC_COM_ID,
                    cm.get_PDF_URL(lc.PDF_ID) AS Lifecycle_Source,
                    t.LC_SRC_NAME AS LC_SOURCE_TYPE,
                    lc.CONTACTING_SUPPLIER,
                    cm.get_man_name(lc.MAN_ID) AS LC_MAN_NAME,
                    lc.LATEST
             FROM cm.TBL_LC_HSTRY lc
             JOIN cm.tbl_lc_lookup_db l on l.LC_LOOKUP_ID=lc.LC_LOOKUP_ID
             JOIN cm.tbl_lc_src_reason r on l.SORCE_REASON_ID=r.SORCE_REASON_ID
             JOIN cm.tbl_lc_src_typ t on r.LC_SRC_ID= t.LC_SRC_ID
             WHERE (lc.COM_ID) IN ({COM_ID}) 
                """
    return query

def fastTable(COM_ID):
    query= fr"""
             SELECT COM_ID AS FAST_TABLE,
                    COMMENTS AS Fast_Comment
             FROM cm.tbl_fast_data
             WHERE (COM_ID) IN ({COM_ID})"""
    return query








