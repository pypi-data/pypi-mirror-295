# Licensed to the Technische Universität Darmstadt under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The Technische Universität Darmstadt
# licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import argparse
from streamlit.web import cli


def main():
    parser = argparse.ArgumentParser(
        description="Generate plots for your INCEpTION project."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-m", "--manager", help="You are managing a single project, or a single location.", action="store_true"
    )
    group.add_argument("-l", "--lead", help="You are leading multiple projects, or multiple locations.", action="store_true")

    args = parser.parse_args()

    if args.manager:
        sys.argv = [
            "streamlit",
            "run",
            f"{os.path.dirname(os.path.realpath(__file__))}/generate_reports_manager.py",
        ]
    elif args.lead:
        sys.argv = [
            "streamlit",
            "run",
            f"{os.path.dirname(os.path.realpath(__file__))}/generate_reports_lead.py",
        ]
    sys.exit(cli.main())
