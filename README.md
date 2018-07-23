Packaging Science History Institute Community History Platform using Docker.

Relies on the Hypothesis service, and the Hypothesis client.

Packaged using Docker Compose.

Uses the Community Science Platform as a submodule.
Use `git submodule init` and `git submodule update`

Need to import oral histories into `community_history_platform/flask/app/static/LSF_oral_histories/`

After that, run:
`sudo docker-compose build`
`sudo docker-compose up`

This will build the images, and then run all of the services concurrently in Docker containers.
