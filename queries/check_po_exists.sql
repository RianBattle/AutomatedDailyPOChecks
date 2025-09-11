SELECT sklc_actualpo
FROM skl$orders
WHERE sklc_actualpo = :poNumber
UNION
SELECT sklc_reference
FROM skl$deal
WHERE sklc_reference = :poNumber
  or sklc_reference = :poNumber || 'BK'
UNION
SELECT sklc_actualpo
FROM skl$skl_ediload
WHERE sklc_actualpo = :poNumber
UNION
SELECT sklc_actualpo
FROM skl$skl_ediload2
WHERE sklc_actualpo = :poNumber
UNION
SELECT sklc_actualpo
FROM skl$skl_ediload3
WHERE sklc_actualpo = :poNumber
UNION
SELECT orderid
FROM skl$sklc_amazonload
WHERE orderid = :poNumber
UNION
SELECT po_no
FROM ediadmin.edi850q
WHERE po_no = :poNumber
UNION
SELECT po_no
FROM ediadmin.edi850q
WHERE po_no in(
    SELECT po_no
    FROM ediadmin.edi850hbeg
    WHERE actualpo = :poNumber
  )