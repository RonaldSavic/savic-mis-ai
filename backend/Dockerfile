# The project's backend image: the platform's backend image plus this
# project's package. Nothing here rebuilds the platform, and no GitHub
# access is needed: the platform image comes from the platform's release ZIP
# (`docker load`) or from your registry.
#
#   dev  — docker-compose.yml: editable install; the compose file mounts
#          ./backend over /project, and uvicorn reloads on every save.
#   prod — docker-compose.prod.yml: the package installed normally.
#
# --no-deps: the platform image already has savic-common and its
# dependencies. If this project needs more packages, list them in
# requirements.txt (hash-pinned for production) and install them here.

ARG PLATFORM_IMAGE=savic-platform-backend:1.1.0

FROM ${PLATFORM_IMAGE} AS dev
USER root
COPY . /project
RUN pip install --no-deps -e /project
USER savic
ENV SAVIC_EXTENSIONS='["mis_ai.extension"]'
CMD ["uvicorn", "savic_common.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--reload", "--reload-dir", "/project"]


FROM ${PLATFORM_IMAGE} AS prod
USER root
COPY pyproject.toml /project/
COPY mis_ai /project/mis_ai
RUN pip install --no-deps /project && rm -rf /project
USER savic
ENV SAVIC_EXTENSIONS='["mis_ai.extension"]'
