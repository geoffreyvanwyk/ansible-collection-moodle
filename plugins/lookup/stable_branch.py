# This file is part of Ansible collection geoffreyvanwyk.moodle.
#
# Ansible collection geoffreyvanwyk.moodle is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible collection geoffreyvanwyk.moodle is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Ansible collection geoffreyvanwyk.moodle. If not, see
# <https://www.gnu.org/licenses/>.

##
# Ansible lookup plugin that retrieves the name of the stable Git branch that
# corresponds to the given Moodle major version.
#
# @copyright  2024 Geoffrey Bernardo van Wyk {@link https://geoffreyvanwyk.dev}
# @link       https://github.com/moodle/moodle
##

DOCUMENTATION = """
name: stable_branch
author: Geoffrey Bernardo van Wyk (https://geoffreyvanwyk.dev)
version_added: 1.1.0
short_description: Stable branch for Moodle version 
description:
  - This lookup plugin retrieves the name of the stable Git branch that
    corresponds to the given Moodle version.
  - The Git branch is in Moodle's repository on GitHub (https://github.com/moodle/moodle).
options:
  moodle_version:
    description: 
      - The human-readable version of Moodle in the format x.y, where x is a
        single-digit number and y is a single or double-digit number.
    type: str
    required: true
"""

EXAMPLE = """
- name: Find stable branch for major Moodle version
  ansible.builtin.debug:
    msg: lookup('geoffreyvanwyk.moodle.stable_branch', moodle_version="3.11")
"""

RETURN = """
  _raw:
    description:
      - A single-element list containing the name of a stable Git branch, e.g. V(['MOODLE_311_STABLE']). 
    type: list
    elements: str
"""

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        moodle_version = str(self.get_option("moodle_version"))
        major_version, minor_version = moodle_version.split(".", maxsplit=1)

        if len(major_version) != 1:
            raise AnsibleLookupError("Invalid moodle_version")

        if len(minor_version) not in [1, 2]:
            raise AnsibleLookupError("Invalid moodle_version")

        branch_number = major_version + (
            minor_version if len(minor_version) == 2 else "0" + minor_version
        )

        return ["MOODLE_" + branch_number + "_STABLE"]
