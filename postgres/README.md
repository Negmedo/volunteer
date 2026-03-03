## Init PG DB
```commandline
    docker compose up -d --build
```

## Clear DB volume 
```commandline
    rmdir /S ./postgres_data
```

## Connect to DB
```
   postgresql://postgres:postgres@localhost:5432/volunteer_db 
```
