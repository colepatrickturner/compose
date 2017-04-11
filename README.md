Docker Compose for Docker Cloud
==============
![Docker Compose](https://raw.githubusercontent.com/salanki/compose/master/logo.png "Docker Compose Logo")
![Docker Cloud](https://tutumcloud.files.wordpress.com/2014/04/cropped-logo-200x49.png "Tutm Logo")

[Docker Cloud](https://cloud.docker.com/) stackfiles are currently rather limited. No support
for env-file, extends or layering multiple compose .ymls over each
other. Using docker-compose to generate a Docker Cloud Tutum compatible YML bridges
the gap.

- Docker Cloud attributes such as target_num_containers, tags, auto destroy,
autoredeploy are supported.
- The output of `config` has been modified to just return the config.
- Links are allowed to be extended.

Use directly via pre built docker image:
```
docker run --rm -it -v `pwd`:/code/shared salanki/compose-tutum config > docker-cloud.yml
```
Create a stack on Docker Cloud: `docker-cloud stack create -f docker-cloud.yml -n mystack`
Update a stack on Docker Cloud: `docker-cloud stack update -f docker-cloud.yml mystack`
