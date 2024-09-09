"""Class for parsing Lab Guru Report Data Excel file."""

import logging
import sys
from datetime import date
from typing import List

import pandas as pd
from pandas import Timestamp
from pydantic import ValidationError

from previsedx_labguru_file_utils import constants
from previsedx_labguru_file_utils.file_utils import check_infile_status
from previsedx_labguru_file_utils.record import Record
from previsedx_labguru_file_utils.parser import Parser as BaseParser

# Need to install the following package to read Excel files with .xls extension.
# pip install xlrd==2.0.1


class Parser(BaseParser):
    """Class for parsing Lab Guru Report Data Excel file."""

    def get_records(self, infile: str) -> List[Record]:
        """Parser the tab-delimited file and retrieve a list of records.

        Args:
            infile (str): The Lab Guru Report Data Excel file to be parsed.
        Returns:
            List(Record): The parsed records.
        """
        if self.is_parsed:
            return self.rec_list

        if infile is None:
            infile = self.infile
            if infile is None:
                raise Exception("No input file provided to parse")

        logging.info(
            f"Will attempt to parse Lab Guru Report Data Excel file '{infile}'"
        )

        check_infile_status(infile)

        record_ctr = 0

        sheet_name = (
            self.config.get("lab_guru", None)
            .get("report_data", None)
            .get("sheet_name", None)
        )
        if sheet_name is None or sheet_name == "":
            sheet_name = constants.DEFAULT_LAB_GURU_REPORT_DATA_SHEET_NAME
        logging.info(f"sheet_name: {sheet_name}")

        header_row_number = (
            self.config.get("lab_guru", None)
            .get("report_data", None)
            .get("header_row_number", None)
        )
        if header_row_number is None or header_row_number == "":
            header_row_number = constants.DEFAULT_LAB_GURU_REPORT_DATA_HEADER_ROW_NUMBER
        logging.info(f"header_row_number: {header_row_number}")

        engine = (
            self.config.get("lab_guru", None)
            .get("report_data", None)
            .get("engine", None)
        )
        if engine is None or engine == "":
            engine = constants.DEFAULT_LAB_GURU_REPORT_DATA_ENGINE
        logging.info(f"engine: {engine}")

        expected_column_headers = (
            self.config.get("lab_guru", None)
            .get("report_data", None)
            .get("expected_column_headers", None)
        )
        if expected_column_headers is None or expected_column_headers == "":
            raise Exception(
                f"Expected column headers not found in configuration file '{self.config_file}'"
            )

        logging.info(f"Here are the expected column headers: {expected_column_headers}")
        # Read the Excel file
        df = pd.read_excel(
            infile,
            sheet_name=sheet_name,
            header=int(header_row_number),
            engine=engine,  # Need to install the following package to read Excel files with .xls extension: pip install xlrd==2.0.1
        )
        # print(df)
        # print("DataFrame shape:", df.shape)
        # print("DataFrame columns:", df.columns)

        logging.info("Will check for missing expected column headers")
        # Check if the expected columns are present
        missing_columns = [
            col for col in expected_column_headers if col not in df.columns
        ]
        if missing_columns:
            raise Exception(f"Missing columns in the DataFrame: {missing_columns}")

        # Extract the relevant rows and columns
        df = df.loc[0:, expected_column_headers]

        # print(f"head: {df.head()}")
        # sys.exit(1)

        # Drop rows with any missing values to ensure data integrity
        # df = df.dropna()

        # print(df)

        record_number = 0

        logging.info("Will process the records now")
        for index, row in df.iterrows():
            record_number += 1
            row_dict = row.to_dict()

            # Convert "Collection Date" to string if it's a Timestamp
            if isinstance(row_dict.get("Collection Date"), (Timestamp, date)):
                row_dict["Collection Date"] = row_dict["Collection Date"].strftime(
                    "%Y-%m-%d"
                )

            logging.info(f"Here is the row_dict: {row_dict}")

            try:
                record = Record(**row_dict)
                logging.info(f"Labguru report data record {record}")
                # import sys
                # sys.exit(1)
                self.rec_list.append(record)
                self.rec_ctr += 1

            except ValidationError as exc:
                print(f"Encountered some ValidationError exception: {repr(exc.errors()[0]['type'])}")
                # missing_fields = [error['loc'][0] for error in exc.errors() if error['msg'] == "field required"]
                print(f"Here are the errors: {exc.errors()}")
                raise exc

            except Exception as e:
                logging.error(
                    f"Encountered some exception with record number '{record_number}': {e}"
                )
                self.error_ctr += 1
                self.error_list.append(e)

            record_ctr += 1

        logging.info(
            f"Processed '{record_ctr}' records in Labguru data file '{infile}'"
        )

        if self.error_ctr > 0:

            self._write_validation_report(infile)
            sys.exit(1)
        else:
            logging.info("No errors encountered")

        self.is_parsed = True

        logging.info("Will accumulate the records in the sample_id_to_record_lookup")
        for record in self.rec_list:
            self.sample_id_to_record_lookup[str(record.previse_lab_id)] = record
        return self.rec_list

    def get_record(self, sample_id: str) -> Record:
        if not self.is_parsed:
            self.get_records(self.infile)
        logging.info(
            f"Labguru report data sample_id_to_record_lookup: {self.sample_id_to_record_lookup}"
        )
        # import sys
        # sys.exit(1)
        return self.sample_id_to_record_lookup.get(sample_id, None)
