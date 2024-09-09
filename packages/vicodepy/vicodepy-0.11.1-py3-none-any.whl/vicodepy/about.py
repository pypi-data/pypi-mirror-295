# ViCodePy - A video coder for Experimental Psychology
#
# Copyright (C) 2024 Esteban Milleret
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

import importlib.metadata
from pathlib import Path
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from .format import FORMAT
from .constants import (
    APP_NAME,
    REPOSITORY_URL,
    PYPI_URL,
)


def open_repository_url():
    open_url(REPOSITORY_URL)


def open_pypi_url():
    open_url(PYPI_URL)


def open_url(url):
    qurl = QUrl(url)
    if not QDesktopServices.openUrl(qurl):
        QMessageBox.warning("Open Url", f"Could not open url '{url}'")


class About:

    def get_pkg_version(self) -> str:
        """Find the version of this package."""
        try:

            pyproject_toml_file = (
                Path(__file__).parent.parent / "pyproject.toml"
            )

            with open(pyproject_toml_file) as fid:
                import tomlkit

                toml_content = tomlkit.parse(fid.read())
                version = f"{toml_content['project']['version']} (dev)"

        except FileNotFoundError:

            try:

                version = importlib.metadata.version(APP_NAME)

            except importlib.metadata.PackageNotFoundError:

                version = "not found"

        return version

    def get_fmt_version(self) -> str:
        """Find the version of the format of the project file"""
        try:

            with open(Path(__file__).parent.joinpath("format.py")) as f:
                exec(f.read())

        except FileNotFoundError:
            pass

        return FORMAT

    def exec(self):
        msg = QMessageBox()
        msg.setWindowTitle("About")
        msg.setText(
            "<center><font size='+1'><b>ViCodePy</b></font></center><br/><br/>"
            "Copyright © 2024 Rafael Laboissière<br/>"
            "Copyright © 2024 Esteban Milleret<br/>"
            "Licensed under the terms of the <a href='https://www.gnu.org/"
            "licenses/gpl-3.0.en.html'>GPL v3 or later</a><br/>"
            f"<a href='{PYPI_URL}'>PyPI project</a><br/>"
            f"<a href='{REPOSITORY_URL}'>Git repository</a><br/>"
        )
        msg.setInformativeText(
            f"Version {self.get_pkg_version()}\n"
            f"Project file format version {self.get_fmt_version()}"
        )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
