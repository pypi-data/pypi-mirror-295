"""Class for parsing Lab Guru Report Data Excel file."""

import logging
import os
from datetime import datetime

from previsedx_labguru_file_utils import constants
from previsedx_labguru_file_utils.record import Record


# Need to install the following package to read Excel files with .xls extension.
# pip install xlrd==2.0.1


class Parser:
    """Class for parsing Lab Guru Report Data Excel file."""

    def __init__(self, **kwargs):
        """Constructor for Parser."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.is_parsed = False
        self.rec_ctr = 0
        self.rec_list = []
        self.sample_id_to_record_lookup = {}

        self.error_ctr = 0
        self.error_list = []

        logging.info(f"Instantiated Parser in file '{os.path.abspath(__file__)}'")

    def get_record(self, sample_id: str) -> Record:
        if not self.is_parsed:
            self.get_records(self.infile)
        logging.info(
            f"Labguru report data sample_id_to_record_lookup: {self.sample_id_to_record_lookup}"
        )

        return self.sample_id_to_record_lookup.get(sample_id, None)

    def _write_validation_report(self, infile: str) -> None:
        """Write the validation report file.

        Args:
            infile (str): The input Lab Guru Report Data Excel file that was parsed.
        """
        logging.info(f"Will attempt to generate validation report for file '{infile}'")
        basename = os.path.basename(infile)
        outfile = os.path.join(self.outdir, f"{basename}.validation-report.txt")

        with open(outfile, "w") as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(
                f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n"
            )
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## infile: {infile}\n")
            of.write(f"## logfile: {self.logfile}\n")

            if self.error_ctr > 0:
                of.write(
                    f"Encountered the following '{self.error_ctr}' validation errors:\n"
                )
                for error in self.error_list:
                    of.write(f"{error}\n")

        logging.info(f"Wrote file validation report file '{outfile}'")
        if self.verbose:
            print(f"Wrote file validation report file '{outfile}'")
