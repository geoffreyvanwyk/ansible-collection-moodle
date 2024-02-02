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
# Ansible lookup plugin that retrieves the path to a Moodle plugin's
# installation directory relative to the Moodle instance's directory root,
# based on the frankenstyle name of the plugin.
#
# @copyright  2024 Geoffrey Bernardo van Wyk {@link https://geoffreyvanwyk.dev}
##

DOCUMENTATION = """
name: plugin_directory
author: Geoffrey Bernardo van Wyk (https://geoffreyvanwyk.dev)
version_added: 1.0.0
short_description: Path to plugin installation directory 
description:
  - This lookup plugin retrieves the path to a Moodle plugin's installation
    directory relative to the Moodle instance's directory root, based on the
    frankenstyle name of the plugin.
options:
  frankenstyle_name:
    description: 
      - The plugin's frankenstyle name, e.g. V('block_xp'). 
    type: str
    required: true
"""

EXAMPLES = """
- name: Find plugin's installation directory 
  ansible.builtin.debug:
    msg: {{ lookup('geoffreyvanwyk.moodle.plugin_directory', frankenstyle_name='block_xp') }}
"""

RETURN = """
  _raw:
    description:
      - A single-element list containing the path to the plugin's installation
        directory, e.g. V(['blocks/xp']). 
    type: list
    elements: str
"""

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        directory_per_plugin_type = {
            "antivirus": "lib/antivirus",
            "assignfeedback": "mod/assign/feedback",
            "assignsubmission": "mod/assign/submission",
            "atto": "lib/editor/atto/plugins",
            "availability": "availability/condition",
            "block": "blocks",
            "booktool": "mod/book/tool",
            "customfield": "customfield/field",
            "datafield": "mod/data/field",
            "enrol": "enrol",
            "fileconverter": "files/converter",
            "filter": "filter",
            "format": "course/format",
            "local": "local",
            "logstore": "admin/tool/log/store",
            "mlbackend": "lib/mlbackend",
            "mod": "mod",
            "profilefield": "user/profile/field",
            "qbank": "question/bank",
            "qbehaviour": "question/behaviour",
            "qformat": "question/format",
            "qtype": "question/type",
            "repository": "repository",
            "theme": "theme",
            "tiny": "lib/editor/tiny/plugins",
            "tool": "admin/tool",
        }

        self.set_options(var_options=variables, direct=kwargs)

        frankenstyle_name = str(self.get_option("frankenstyle_name"))
        plugin_type, plugin_name = frankenstyle_name.split("_", maxsplit=1)

        plugin_type = plugin_type.strip()
        if plugin_type not in directory_per_plugin_type.keys():
            raise AnsibleLookupError("Invalid plugin type")

        plugin_name = plugin_name.strip()
        if len(plugin_name) == 0:
            raise AnsibleLookupError("Invalid plugin name")

        return [directory_per_plugin_type[plugin_type] + "/" + plugin_name]
