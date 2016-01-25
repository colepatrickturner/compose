Docker Compose for Tutum
==============
![Docker Compose](https://raw.githubusercontent.com/salanki/compose/master/logo.png "Docker Compose Logo")
![Tutum](https://tutumcloud.files.wordpress.com/2014/04/cropped-logo-200x49.png "Tutm Logo")

[Tutum](https://www.tutum.co/) stackfiles are currently rather limited. No support
for env-file, extends or layering multiple compose .ymls over each
other. Using docker-compose to generate a Tutum compatible YML bridges
the gap.

- Tutum attributes such as target_num_containers, tags, auto destroy,
autoredeploy are supported.
- The output of `config` has been modified to just return the config.
- Links are allowed to be extended.

Use directly via pre built docker image:
```
docker run --rm -it -v `pwd`:/code/shared salanki/compose-tutum config > tutum.yml
```
Create a stack on Tutum: `tutum stack create -f tutum.yml -n mystack`
Update a stack on Tutum: `tutum stack update -f tutum.yml mystack`
