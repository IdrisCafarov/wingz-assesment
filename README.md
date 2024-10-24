# Wingz Assessment - Ride Management API

This repository contains a **Django web application** configured to run with **PostgreSQL** using **Docker Compose**. Follow the instructions below to set up and run the project.

---



## Prerequisites

Make sure you have the following tools installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- A terminal or command prompt

---

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/IdrisCafarov/wingz-assesment.git
   cd wingz-assesment

2. **Create environment variables:**
    ```bash
    cp .env.sample .env

3. **Build and start Docker containers:**
    ```bash
    docker-compose up --build -d

4. **Create a superuser (admin access):**
    ```bash
    sudo docker-compose run --rm app sh -c "python3 manage.py createsuperuser"

5. **Access the app:**
    The application will be available at
    ```bash
    http://localhost:8000/

## Swagger Documentation
    Swagger provides an interactive UI to explore and test the API endpoints.

    Swagger URL:
    ```bash
        http://localhost:8000/api/docs/

## SQL Report Query
    This query returns the count of trips longer than 1 hour, grouped by month and driver name.

    ```bash
    WITH pickup_dropoff_times AS (
        SELECT
            r.id AS ride_id,
            r.driver_id,
            DATE_TRUNC('month', pickup_event.created_at) AS month,
            pickup_event.created_at AS pickup_time,
            dropoff_event.created_at AS dropoff_time,
            EXTRACT(EPOCH FROM (dropoff_event.created_at - pickup_event.created_at)) / 3600 AS  duration_in_hours
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

## Running the SQL Query
1. **Connect to PostgreSQL inside the container:**

    ```bash
    docker-compose exec db sh -c "PGPASSWORD='YOUR_DBPASS' psql -U YOUR_DBUSER -d YOUR_DBNAME"

1. **Run the Query Using Django’s Management Command:**

    ```bash
    sudo docker-compose run --rm app sh -c "python3 manage.py run_trip_report"
