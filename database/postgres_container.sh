
#!/bin/bash
docker run -d \
    --name jornal_db \
    -e POSTGRES_USER=jornal \
    -e POSTGRES_DB=jornal \
    -e POSTGRES_PASSWORD=jornal \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -p 5432:5432 \
    -v /home/junior/.postgres/data:/var/lib/postgresql/data \
    postgres
