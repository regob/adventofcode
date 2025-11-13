# https://gist.github.com/mauriciopoppe/de8908f67923091982c8c8136a063ea6
# https://www.partow.net/programming/makefile/index.html
# https://github.com/mbcrawfo/GenericMakefile/blob/master/cpp/Makefile

#### PROJECT SETTINGS ####
CXX ?= g++
COMPILE_FLAGS := -O2 -Wall -std=c++17 -Wextra
DCOMPILE_FLAGS := -D DEBUG -g
LINK_FLAGS :=
LIBS :=
SRC_EXT := cpp
SRC_PATH := .
BIN_NAME := aoc
#### END PROJECT SETTINGS ####

#### VARIABLES ####
BUILD_PATH := build
BIN_PATH := $(BUILD_PATH)/bin
CXXFLAGS := $(CXXFLAGS) $(COMPILE_FLAGS)
LDFLAGS := $(LDFLAGS) $(LINK_FLAGS)

SOURCES = $(shell find $(SRC_PATH) -name '*.$(SRC_EXT)' -printf '%T@\t%p\n' \
						| sort -k 1nr | cut -f2-)

# Set the object file names, with the source directory stripped
# from the path, and the build path prepended in its place
OBJECTS = $(SOURCES:$(SRC_PATH)/%.$(SRC_EXT)=$(BUILD_PATH)/%.o)
# Set the dependency files that will be used to add header dependencies
DEPS = $(OBJECTS:.o=.d)

#### TARGETS ####

# Main rule, checks the executable and symlinks to the output
all: dirs $(BIN_PATH)/$(BIN_NAME)
	@echo "Making symlink: $(BIN_NAME) -> $<"
	@$(RM) $(BIN_NAME)
	@ln -s $(BIN_PATH)/$(BIN_NAME) $(BIN_NAME)

.PHONY: debug
debug: CXXFLAGS += $(DCOMPILE_FLAGS)
debug: all

# Create the directories used in the build
.PHONY: dirs
dirs:
	@echo "Creating directories"
	@mkdir -p $(dir $(OBJECTS))
	@mkdir -p $(BIN_PATH)


# Source file rules
# After the first compilation they will be joined with the rules from the
# dependency files to provide header dependencies
$(BUILD_PATH)/%.o: $(SRC_PATH)/%.$(SRC_EXT)
	@echo "Compiling: $< -> $@"
	@$(START_TIME)
	$(CMD_PREFIX)$(CXX) $(CXXFLAGS) $(INCLUDES) -MP -MMD -c $< -o $@
	@echo -en "\t Compile time: "
	@$(END_TIME)

# Link the executable
$(BIN_PATH)/$(BIN_NAME): $(OBJECTS)
	@echo "Linking: $@"
	$(CXX) $(OBJECTS) $(LDFLAGS) -o $@
