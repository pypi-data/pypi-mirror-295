# from distutils.errors import LibError
import logging

# from re import template

# from pyparsing import col
import xml.etree.ElementTree as ET
import rich.console
import json


import pandas as pd


import sys
import os

import ftplib
import relecov_tools.utils
from relecov_tools.config_json import ConfigJson

from ena_upload.ena_upload import extract_targets

# from ena_upload.ena_upload import submit_data
from ena_upload.ena_upload import run_construct
from ena_upload.ena_upload import construct_submission
from ena_upload.ena_upload import send_schemas
from ena_upload.ena_upload import process_receipt
from ena_upload.ena_upload import update_table
from ena_upload.ena_upload import construct_xml

# from ena_upload.ena_upload import make_update
# from ena_upload.ena_upload import process_receipt

# from ena_upload.ena_upload import save_update
import site

pd.options.mode.chained_assignment = None

template_path = os.path.join(site.getsitepackages()[0], "ena_upload", "templates")
template_path = os.path.join(os.getcwd(), "/home/pmata/git_repositories/relecov-tools/relecov_tools/templates")

log = logging.getLogger(__name__)
stderr = rich.console.Console(
    stderr=True,
    style="dim",
    highlight=False,
    force_terminal=relecov_tools.utils.rich_force_colors(),
)


class EnaUpload:
    def __init__(
        self,
        user=None,
        passwd=None,
        center=None,
        source_json=None,
        dev=None,
        customized_project=None,
        action=None,
        output_path=None,
    ):
        if user is None:
            self.user = relecov_tools.utils.prompt_text(
                msg="Enter your username defined in ENA"
            )
        else:
            self.user = user
        if passwd is None:
            self.passwd = relecov_tools.utils.prompt_password(
                msg="Enter your password to ENA"
            )
        else:
            self.passwd = passwd
        if center is None:
            self.center = relecov_tools.utils.prompt_text(msg="Enter your center name")
        else:
            self.center = center
        if source_json is None:
            self.source_json_file = relecov_tools.utils.prompt_path(
                msg="Select the ENA json file to upload"
            )
        else:
            self.source_json_file = source_json
        if dev is None:
            self.dev = relecov_tools.utils.prompt_yn_question(
                msg="Do you want to test upload data?"
            )
        else:
            self.dev = dev

        if customized_project is None:
            self.customized_project = None
        else:
            self.customized_project = customized_project
        if action is None:
            self.action = relecov_tools.utils.prompt_selection(
                msg="Select the action to upload to ENA",
                choices=["add", "modify", "cancel", "release"],
            )
        else:
            self.action = action.upper()
        if output_path is None:
            self.output_path = relecov_tools.utils.prompt_path(
                msg="Select the folder to store the xml files"
            )
        else:
            self.output_path = output_path

        if not os.path.isfile(self.source_json_file):
            log.error("json data file %s does not exist ", self.source_json_file)
            stderr.print(f"[red]json data file {self.source_json_file} does not exist")
            sys.exit(1)
        with open(self.source_json_file, "r") as fh:
            self.json_data = json.loads(fh.read())

        if self.dev:
            self.url = "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/?auth=ENA"
        else:
            self.url = "https://www.ebi.ac.uk/ena/submit/drop-box/submit/?auth=ENA"

    def schema_dataframe(self):
        config_json = ConfigJson()


        return

    def schemas_from_json(self):
        with open(self.source_json_file, "r") as f:
            json_data = json.load(f)

        config_json = ConfigJson()
        source_options = ["study", "samples", "run", "experiment"]
        schemas_dataframe = {}

        for source in source_options:
            source_topic = "_".join(["df",source,"fields"])
            source_fields = config_json.get_topic_data("ENA_fields", source_topic)

            source_dict = {field: [sample[field] for sample in json_data]
                            for field in source_fields}
            schemas_dataframe[source] = pd.DataFrame.from_dict(source_dict)

        """Esto se puede meter dentro del bucle de arriba seguro"""    
        schemas_dataframe["study"].rename(
            columns = {"study_alias":"alias", "study_title":"title"},
            inplace = True
            )
        schemas_dataframe["samples"].rename(
            columns = {"sample_alias":"alias", "sample_title":"title"},
            inplace = True
            )
        
        "BOrrar una vez incorporado al modulo de map"
        schemas_dataframe["run"].rename(
            columns = {"study_alias":"alias", "study_title":"title"},
            inplace = True
            )
        schemas_dataframe["experiment"]["alias"]

        return schemas_dataframe

    def upload(self):
        """Create the required files and upload to ENA"""
        self.schemas_from_json()
        self.convert_input_json_to_ena()
        self.create_structure_to_ena()
