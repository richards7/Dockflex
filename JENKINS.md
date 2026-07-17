# Jenkins pipeline

The root `Jenkinsfile` builds the same Docker image used for deployment,
runs the app smoke tests inside that image, and only then pushes it to Docker
Hub.

## Jenkins prerequisites

- Create a **Pipeline from SCM** job pointing to
  `https://github.com/richards7/Dockflex.git` and select `Jenkinsfile`.
- The Jenkins Docker agent must have Docker CLI access to the host Docker
  daemon (normally by mounting `/var/run/docker.sock`).
- Add a Jenkins **Username with password** credential with ID
  `dockerhub-credentials`. Use the Docker Hub username and a Docker Hub access
  token as the password.

## Pipeline parameters

- `DOCKERHUB_IMAGE`: Docker Hub destination; default `richards7/dockflex`.
- `PUSH_TO_DOCKERHUB`: leave enabled for main/master builds. Disable it for a
  verification-only run.

Successful builds push two tags: the Jenkins build number and `latest`.
