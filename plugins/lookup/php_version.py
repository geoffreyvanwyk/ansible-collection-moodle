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
# Ansible lookup plugin that retrieves the latest PHP version that is
# compatible with the given Moodle version.
#
# @copyright  2024 Geoffrey Bernardo van Wyk {@link https://geoffreyvanwyk.dev}
# @link       https://moodledev.io/general/releases
##

DOCUMENTATION = """
name: php_version
author: Geoffrey Bernardo van Wyk (https://geoffreyvanwyk.dev)
version_added: "1.0.0"
short_description: Latest PHP version compatible with given Moodle version
description:
  - This lookup plugin retrieves the latest PHP version that is compatible with
    the given Moodle version.
options:
  moodle_version:
    description:
      - The Moodle version for which to retrieve the PHP version.
    type: str
    required: true
    choices: ['3.9', '3.10', '3.11', '4.0', '4.1', '4.2', '4.3']
"""

EXAMPLES = """
- name: Fetch PHP version to use with Moodle version
  ansible.builtin.debug:
    var: {{ lookup('geoffreyvanwyk.moodle.php_version', mooodle_version='3.11') }}
"""

RETURN = """
  _raw:
    description:
      - A single-element list containing a PHP version. 
    type: list
    elements: str
"""

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        php_per_moodle = {
            "3.9": ["7.4"],
            "3.10": ["7.4"],
            "3.11": ["8.0"],
            "4.0": ["8.0"],
            "4.1": ["8.1"],
            "4.2": ["8.2"],
            "4.3": ["8.2"],
        }

        self.set_options(var_options=variables, direct=kwargs)
        moodle_version = self.get_option("moodle_version")

        if moodle_version not in php_per_moodle.keys():
            raise AnsibleLookupError("Unknown Moodle version")

        return php_per_moodle[moodle_version]
