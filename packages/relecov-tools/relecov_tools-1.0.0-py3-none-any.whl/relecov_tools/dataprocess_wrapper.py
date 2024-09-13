#!/usr/bin/env python
import logging
import re
import yaml
import os
import sys
import json
import inspect
import rich.console
from relecov_tools.download_manager import DownloadManager
from relecov_tools.read_lab_metadata import RelecovMetadata
from relecov_tools.json_validation import SchemaValidation
import relecov_tools.log_summary
import relecov_tools.utils

log = logging.getLogger(__name__)
stderr = rich.console.Console(
    stderr=True,
    style="dim",
    highlight=False,
    force_terminal=relecov_tools.utils.rich_force_colors(),
)


class ProcessWrapper:
    def __init__(
        self,
        config_file: str = None,
        output_folder: str = None
    ):
        if not os.path.isfolder(str(output_folder)):
            sys.exit(FileNotFoundError(f"Output folder {output_folder} is not valid"))
        else:
            self.output_folder = output_folder
        if not os.path.isfile(str(config_file)):
            sys.exit(FileNotFoundError(f"Config file {config_file} is not a file"))
        else:
            try:
                self.config_data = relecov_tools.utils.read_yml_file(config_file)
                # Config file should include a key
            except yaml.YAMLError as e:
                sys.exit(yaml.YAMLError(f"Invalid config file: {e}"))
        output_regex = ("out_folder", "output_folder", "output_location")
        for key, val in self.config_data.items():
            if any(x for x in output_regex in val):
                self.config_data[key] = self.output_folder
        self.wrapper_logsum = relecov_tools.log_summary.LogSum(
            output_folder=self.output_folder
        )
        return
    
    def exec_process(self, module, class_name, func_name, process_params):
        import_statement = f"import {module}"
        exec(import_statement)
        class_args = inspect.getfullargspec(module + "." + class_name.__init__)[0]
        valid_params = {x:y for x,y in process_params if x in class_args}
        if not valid_params:
            stderr.print(f"[red]Invalid params for {module} in {self.config_file}")
            sys.exit(1)
        init_class = eval(module + "." + class_name + "(**valid_params)")
        eval(init_class + "." + func_name + "()")
        try:
            process_logs = init_class.logsum.logs
        except AttributeError:
            process_logs = None
        return process_logs

    def exec_download(self, download_params):
        download_args = inspect.getfullargspec(RelecovMetadata.__init__)[0]
        download_valid_params = {x:y for x,y in download_params if x in download_args}
        if not download_valid_params:
            stderr.print(f"[red]Invalid params for download in {self.config_file}")
            sys.exit(1)
        download_manager = DownloadManager(**download_valid_params)
        download_manager.execute_process()
        local_folders = download_manager.local_processed_folders
        download_logs = download_manager.logsum.logs
        return local_folders, download_logs

    def exec_read_metadata(self, readmeta_params):
        readmeta_args = inspect.getfullargspec(RelecovMetadata.__init__)[0]
        readmeta_valid_params = {x:y for x,y in readmeta_params if x in readmeta_args}
        if not readmeta_valid_params:
            stderr.print(f"[red]Invalid params for read-lab-metadata in {self.config_file}")
            sys.exit(1)
        read_metadata = RelecovMetadata(**readmeta_valid_params)
        read_metadata.create_metadata_json()
        read_meta_logs = read_metadata.logsum.logs
        return read_meta_logs


    def exec_validation(self, validate_params):
        validation_args = inspect.getfullargspec(SchemaValidation.__init__)[0]
        validate_valid_params = {x:y for x,y in validate_params if x in validation_args}
        if not validate_valid_params:
            stderr.print(f"[red]Invalid params for validate in {self.config_file}")
            sys.exit(1)
        validate = relecov_tools.json_validation.SchemaValidation(**validate_valid_params)
        validate.validate()
        validate_logs = validate.logsum.logs
        return validate_logs


    def run_wrapper(self):
        """Execute each given process in config file sequentially
        """
        download_params = self.config_data["download"]
        readmeta_params = self.config_data["read-lab-metadata"]
        readmeta_params.update({"output_folder": self.output_folder})
        validate_params = self.config_data["validate"]
        validate_params.update({"out_folder": self.output_folder})
        import pdb; pdb.set_trace()
        download_logs = self.exec_download(download_params)
        folders_processed = {
            k:k.get("path") for k in download_logs if k.get("valid") is True
        }
        for key, folder in folders_processed.items():
            metadata_file = [
                x for x in os.listdir(folder) if re.search("lab_metadata.*.xlsx", x)
            ]
            samples_file = [
                x for x in os.listdir(folder) if re.search("samples_data.*.json", x)
            ]
            readmeta_params.update({"metadata_file": metadata_file})
            readmeta_params.update({"sample_list_file": samples_file})
            read_meta_logs = self.exec_read_metadata(readmeta_params)
            validate_logs = self.exec_validate(validate_params)
            merged_logs = self.wrapper_logsum.merge_logs(
                key_name=key, logs_list=[download_logs, read_meta_logs, validate_logs]
            )
        self.wrapper_logsum.create_error_summary(
            called_module="process-wrapper",
            logs=merged_logs,
            to_excel=True
        )
        return
    
    def generic_wrapper(self):
        for process, params in self.config_data.items():
            module = params.get("module")
            class_name = params.get("class_name")
            func_name = params.get("func_name")
            class_params = params.get("class_args")
            if not all(x for x in (module, class_name, func_name)):
                stderr.print(f"[red]Not all fields in config were valid for {process}")
                sys.exit(1)
            process_logs = self.exec_process(module, class_name, func_name, class_params)
            self.wrapper_logsummary.logs.update(process_logs)
        self.wrapper_logsummary.create_error_summary(
            called_module="process-wrapper", logs=self.wrapper_logsummary.logs
        )
        self.wrapper_logsummary.create_logs_excel(
            logs=self.wrapper_logsummary.logs
        )
