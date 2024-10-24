from django.core.management.base import BaseCommand
from django.db import connection

SQL_QUERY = """
WITH pickup_dropoff_times AS (
    SELECT
        r.id AS ride_id,
        r.driver_id,
        DATE_TRUNC('month', pickup_event.created_at) AS month,
        pickup_event.created_at AS pickup_time,
        dropoff_event.created_at AS dropoff_time,
        EXTRACT(EPOCH FROM (dropoff_event.created_at - pickup_event.created_at)) / 3600 AS duration_in_hours
    FROM
        ride_ride r
    JOIN ride_rideevent pickup_event
        ON r.id = pickup_event.ride_id
        AND pickup_event.description = 'Status changed to pickup'
    JOIN ride_rideevent dropoff_event
        ON r.id = dropoff_event.ride_id
        AND dropoff_event.description = 'Status changed to dropoff'
)
SELECT
    TO_CHAR(month, 'YYYY-MM') AS month,
    u.name AS driver_name,
    COUNT(ride_id) AS count_of_trips_over_1_hr
FROM
    pickup_dropoff_times pdt
JOIN
    account_myuser u ON pdt.driver_id = u.id
WHERE
    pdt.duration_in_hours > 1
GROUP BY
    month, driver_name
ORDER BY
    month, driver_name;

"""

class Command(BaseCommand):
    help = 'Run trip report query'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(SQL_QUERY)
            rows = cursor.fetchall()
            print("Month\tDriver Name\tCount of Trips > 1 hr")
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t{row[2]}")
