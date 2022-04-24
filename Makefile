## -----------------getREST-Makefile-----------------------
## List of supported commands:
## - build    - Build docker image
## - run      - Run docker image
## - rund     - Run docker image detached
## - help     - Show help message
## --------------------------------------------------------

all: help

help:
	@sed --quiet --expression 's/^## //p' $(MAKEFILE_LIST)

build:
	docker build --file docker/Dockerfile --tag get-rest .

run:
	docker run --rm --publish 7777:8000 --detach --name get-rest get-rest

