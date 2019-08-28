# Science History Institute Community History Platform

The Science History Institute (formerly Chemical Heritage Foundation) merged with the Life Sciences Foundation. In the process, they acquired a collection of oral histories (interviews) of key players in the development of the biotech industry in the Bay Area. The collaboration between the Science History Institute and the UW Datalab in the summer of 2018 was an effort to use these oral histories as the basis for a project to facilitate the collaborative construction of the history of biotech by the community itself. Specifically, what came out of this effort was a prototype for a Community History Platform---an online platform which allows users (i.e., members of the community of people who worked in or were somehow involved in the biotech industry as it emerged) to register an account and annotate the oral histories. This could be expanded to include other texts or artifacts (pictures, documents, etc.) in addition to the oral histories. The annotation functionality is meant to serve as a way for the community to discuss and thereby create the history---a history that is living and multifaceted.

The frontend app is a Python Flask app that allows users to register an account, browse the oral history texts, and leave annotations on segments of the oral histories. Users can also reply to others’ annotations. This app lives in a separate repository: <https://github.com/h1-the-swan/science_history_institute_chp_app>, which is a submodule of this repository.

The backend setup uses the Hypothesis annotation service to allow annotations on the oral histories.

The Hypothesis Project (https://web.hypothes.is) is a non-profit organization that, among other things, creates open-source software to facilitate collective annotations of web content. Behind the Community History Platform runs a custom instance of the Hypothesis software that allows users of the app to create annotations on the oral histories using their CHP accounts.

To make this system easy to deploy on a server, all of the components run side-by-side in Docker containers. Docker is a platform that allows contained software services to be run on any systems. The services that run for the CHP are the Hypothesis service, the Hypothesis client, several additional backend services (Elasticsearch, PostgreSQL, RabbitMQ, Nginx) and the frontend app. These services are all integrated using Docker Compose, a tool which orchestrates multiple Docker containers to work together as one application.


### Installation on an AWS EC2 instance:

Follow these instructions to deploy the Community History Platform on an AWS EC2 instance. The instructions must be followed in order.

1. Launch an AWS instance: Ubuntu Server, t2.medium; 4GiB RAM, 8GiB EBS storage
  - In step 6: Configure Security Group, add a rule for HTTP (allow incoming HTTP requests on port 80)
  - You will need to either generate SSH keys or use an existing key pair to access the server via SSH
  - Once the instance is running, copy the Public DNS address (e.g., `ec2-##-###-###-###.us-west-2.compute.amazonaws.com`). This will be referred to as `<PUBLIC-DNS>` below.
2. SSH into the EC2 instance:
  - `ssh -i <SSH-PRIVATE-KEY> ubuntu@<PUBLIC-DNS>`
3. Once on the EC2 instance, clone this repository, then initialize and update the submodule:
  - `git clone https://github.com/h1-the-swan/science_history_institute_community_history_platform.git`
  - `cd science_history_institute_community_history_platform`
  - `git submodule init && git submodule update`
4. There are some files that are not included in the repository and need to be added manually. These include the `.env` file with environment variables, and the Oral Histories Word documents.
  - Put the `.env` file in the project directory (`~/science_history_institute_community_history_platform/`). See below for the environment variables that must be set.
  - Put the Oral Histories word documents in `~/science_history_institute_community_history_platform/science_history_institute_chp_app/app/static/LSF_oral_histories/`
5. Install Docker-CE and docker-compose by running:
  - `cd ~/science_history_institute_community_history_platform`
  - `source install-docker.sh`
6. Run a script that modifies some environment variables:
  - `cd ~/science_history_institute_community_history_platform`
  - `python3 modify_envfile.py --ec2`
7. Run Docker Compose to start all of the components:
  - `sudo docker-compose build && sudo docker-compose up`
8. The platform is now running and can be accessed via a web browser at `http://<PUBLIC-DNS>/chp`. Register an account and log in to use it.

#### To restore a database snapshot
1. If docker-compose is running in the foreground, Press CTRL-Z, then run the command `bg` to move the process to the background
2. `source load_database_snapshot.sh`
  - (see the comments in `load_database_snapshot.sh` to understand what it does)
  
#### To create a database snapshot
Use `backup_postgres.sh`

### Environment variables
You need to manually add a `.env` file not included in this repo (in step 4 of the installation instructions above). Here is an example `.env` file:

```
PYTHONUNBUFFERED=0
FLASK_ENV=development
APP_NAME="Science History Institute Community History"
FRONT_APP_URL=http://localhost:5050
ADMIN_USERNAME=lsf_dev
ADMIN_EMAIL=<EMAIL>
ADMIN_PASSWORD=<PASSWORD>
HYPOTHESIS_SERVICE=http://localhost:5000
HYPOTHESIS_AUTHORITY=sciencehistory.org
HYPOTHESIS_CLIENT_ID=<CLIENT_ID>
HYPOTHESIS_CLIENT_SECRET=<CLIENT_SECRET>
HYPOTHESIS_JWT_CLIENT_ID=<JWT_CLIENT_ID>
HYPOTHESIS_JWT_CLIENT_SECRET=<JWT_CLIENT_SECRET>
SIDEBAR_APP_URL=http://localhost:5000/app.html
HYPOTHESIS_CLIENT_URL=http://localhost:3001/hypothesis
WEBSOCKET_URL=ws://localhost:5001/ws
SECRET_KEY=<SECRET_KEY>
ELASTICSEARCH_HOST=http://localhost:9200
ELASTICSEARCH_URL=http://localhost:9201
DATABASE_URL=postgresql://postgres@localhost/postgres
BROKER_URL=amqp://guest:guest@localhost:5672//
DEV_DATABASE_URL=postgresql://postgres@localhost/chp
```


