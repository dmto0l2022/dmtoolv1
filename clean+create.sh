podman stop container_package_1
podman rm container_package_1
podman rmi image_package_1

cd /opt/dmtools/code/dmtoolv1

uid=1001
gid=1002
subuidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range \
   .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

podman build \
-f Dockerfile \
--build-arg=TWINE_PASSWORD=$TWINE_PASSWORD \
-t image_package_1 .

##-v /HOST-DIR:/CONTAINER-DIR

podman run -dt \
--name container_package_1 \
--user $uid:$gid \
localhost/image_package_1:latest

## -v /opt/dmtools/code/dmtoolv1/:/workdir \
#podman build \
#--build-arg=ENV_UID=${ENV_UID} \
#-t image_mariadb_1 .
