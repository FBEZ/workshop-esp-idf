# Variables
HUGO := hugo
PUBLIC_DIR := public
GH_BRANCH := gh-pages
COMMIT_MSG := "Publish site from source commit"

# Default target
all: deploy

# Build Hugo site
build:
	$(HUGO) --cleanDestinationDir

# Deploy to gh-pages
deploy: build
	@echo "Deploying to $(GH_BRANCH) branch..."
	CURRENT_BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	git checkout $(GH_BRANCH); \
	rm -rf *; \
	cp -r $(PUBLIC_DIR)/* .; \
	git add .; \
	git commit -m "$(COMMIT_MSG) ($$CURRENT_BRANCH)"; \
	git push origin $(GH_BRANCH); \
	git checkout $$CURRENT_BRANCH

# Clean build
clean:
	rm -rf $(PUBLIC_DIR)/*
