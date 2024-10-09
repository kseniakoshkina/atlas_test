CREATE EVENT cleaning
ON SCHEDULE EVERY 1 MONTH
DO
  CREATE TEMPORARY TABLE duplicates AS
  SELECT analysis1.analysisName
  FROM Analysis analysis1
  INNER JOIN Analysis analysis2 ON analysis1.barcodeName = analysis2.barcodeName AND analysis1.analysisName < analysis2.analysisName
  LEFT JOIN MutationResult mutres ON analysis1.analysisName = mutres.Analysis_analysisName
  WHERE mutres.Analysis_analysisName IS NULL
  AND EXISTS (
    SELECT 1
    FROM MutationResult mutres2
    WHERE mutres2.Analysis_analysisName = analysis2.analysisName
  );

  SET @dup_count = (SELECT COUNT(*) FROM duplicates);

  DELETE analys FROM Analysis analys
  INNER JOIN duplicates dups ON analysis.analysisName = dups.analysisName;

  INSERT INTO log_table (log_date, log_message)
  VALUES (NOW(), CONCAT('Удалено ', @dup_count, ' дубликатов из таблицы Analysis'));

  DROP TEMPORARY TABLE duplicate_analyses;
