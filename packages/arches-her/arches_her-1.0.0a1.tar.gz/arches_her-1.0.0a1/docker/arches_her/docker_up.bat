docker-compose -f docker-compose-dependencies.yml -p arches_her up -d
timeout /t 30 /nobreak
docker-compose -f docker-compose.yml -p arches_her up -d --build