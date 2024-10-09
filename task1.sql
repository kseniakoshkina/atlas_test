SELECT
    patient.patientId,
    COUNT(mutres.idMutationResult) AS somMutCount
FROM
    Patient patient
JOIN
    `Case` case_ ON patient.patientId = case_.patientId
JOIN
    Barcode barcode ON case_.caseId = barcode.caseId
JOIN
    Analysis analysis ON barcode.barcodeId = analysis.barcodeId
JOIN
    MutationResult mutres ON analysis.analysisName = mutres.Analysis_analysisName
WHERE 1=1
    AND mutres.zygosity = 'somatic'
    AND analysis.analysisRole = 'Major'
GROUP BY
    patient.patientId;
