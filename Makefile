.PHONY: run setup
include .env

export STREAMABLE_EMAIL
export STREAMABLE_PASSWORD
export REDDIT_CLIENT_ID
export REDDIT_CLIENT_SECRET
export REDDIT_USERNAME
export REDDIT_PASSWORD
export MEGA_USERNAME
export MEGA_PASSWORD

run:
	python3 main.py

setup:
	pip3 install -r requirements.txt