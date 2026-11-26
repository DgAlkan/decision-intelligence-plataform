-- DuckDB; generate data first with python generate_data.py
SELECT date_trunc('month',date) AS month, unit, count(*) AS appointments,
count(*) FILTER (WHERE status='No show') AS missed,
count(*) FILTER (WHERE status='No show')::DOUBLE / nullif(count(*) FILTER (WHERE status IN ('Attended','No show')),0) AS no_show_rate
FROM read_csv_auto('data/synthetic.csv') GROUP BY 1,2 ORDER BY 1,2;
