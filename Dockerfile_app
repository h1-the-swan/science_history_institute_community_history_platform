FROM python:3.6

WORKDIR /var/lib/community_history_platform

COPY ./flask/requirements.txt ./

# Install build deps, build, and then clean up.
RUN pip install -r requirements.txt

COPY ./flask .

# Expose the default port.
EXPOSE 5050

# Set the application environment
ENV PATH /var/lib/community_history_platform/bin:$PATH
ENV PYTHONIOENCODING utf_8
ENV PYTHONPATH /var/lib/community_history_platform:$PYTHONPATH

# Create a symlink from .env to config.env, because the app looks for config.env
RUN ln -s .env config.env

RUN python manage.py recreate_db
RUN python manage.py setup_dev

ENTRYPOINT ["honcho", "start", "-f", "Local", "-e", ".env"]
