NAME=generate_certificate

all: build run

build:
	@docker build -t $(NAME) .

run:
	@docker run --rm -v .:/app $(NAME)

.PHONY: all build run
