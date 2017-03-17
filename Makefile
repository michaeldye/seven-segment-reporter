SHELL = /bin/bash -e

all: package

clean:
	tools/py-clean CLEAN ./python/
	- rm -Rf ./python/ve
	- rm -Rf ./python/build
	- rm -Rf ./python/dist

deep-clean:
	tools/deep-clean CLEAN

sys-deps:
ifneq (,$(shell which apt 2> /dev/null))
	sudo apt install -y python3-dbus
else ifneq (,$(shell which pacman 2> /dev/null))
	sudo pacman -Sy --noconfirm python-dbus
else
	@echo "The package python3-dbus is required by this program but could not be automatically installed. Please ensure it is installed."
endif

package: python/ve
	tools/py-in-venv ./python "python ./setup.py bdist_wheel"

# install all requirements, std tools for packaging and publishing
python/ve: sys-deps
	tools/py-in-venv ./python "pip install -U pip pbr wheel"
	tools/py-in-venv ./python "pip install -r ./requirements.txt"

repo-fork-sync:
	tools/repo-fork-sync

.PHONY: clean sys-deps deep-clean package python/ve repo-fork-sync
