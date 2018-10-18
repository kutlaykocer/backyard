GOBUILD=go build
GOTEST=go test
GOCLEAN=go clean

BIN_DIR=bin
BUILD_FLAGS=-ldflags="-s -w"

.PHONY: all
all: frontend analyzer scanner-theharvester scanner-spiderfoot

.PHONY: clean
clean:
	$(GOCLEAN)
	rm -f $(BIN_DIR)/*

.PHONY: test
test:
	$(GOTEST) ./...

.PHONY: frontend
frontend: test
	$(GOBUILD) $(BUILD_FLAGS) -o $(BIN_DIR)/frontend cmd/frontend.go

.PHONY: analyzer
analyzer: test
	 $(GOBUILD) $(BUILD_FLAGS) -o $(BIN_DIR)/analyzer cmd/analyzer.go

.PHONY: scanner-theharvester
scanner-theharvester: test
	$(GOBUILD) $(BUILD_FLAGS) -o $(BIN_DIR)/scanner-theharvester cmd/harvester.go

.PHONY: scanner-spiderfoot
scanner-spiderfoot: test
	$(GOBUILD) $(BUILD_FLAGS) -o $(BIN_DIR)/scanner-spiderfoot cmd/spiderfoot.go
