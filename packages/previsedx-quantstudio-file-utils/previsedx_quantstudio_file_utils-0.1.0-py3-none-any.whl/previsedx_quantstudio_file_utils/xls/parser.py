"""Class for parsing Thermo Fisher Scientific QuantStudio qPCR Result Excel
files."""
import logging
import os
import pandas as pd
import sys

from typing import List

from pydantic import ValidationError

from previsedx_quantstudio_file_utils import constants
from previsedx_quantstudio_file_utils.file_utils import check_infile_status
from previsedx_quantstudio_file_utils.record import Record
from previsedx_quantstudio_file_utils.parser import Parser as BaseParser


# Need to install the following package to read Excel files with .xls extension.
# pip install xlrd==2.0.1


class Parser(BaseParser):
    """Class for parsing Thermo Fisher Scientific QuantStudio qPCR Result Excel
    files."""

    def get_records(self, infile: str) -> List[Record]:
        """Parser the tab-delimited file and retrieve a list of records.

        Args:
            infile (str): The Excel .xls results to be parsed.
        Returns:
            List(Record): The parsed records.
        """
        if self.is_parsed:
            return self.rec_list

        if not infile.endswith(".xls"):
            raise Exception(
                f"Invalid file extension for file '{infile}'. Expected '.xlsx' extension."
            )

        logging.info(f"Will attempt to parse gene file '{infile}'")

        check_infile_status(infile)

        record_ctr = 0

        sheet_name = self.config.get("gene_file", None).get("sheet_name", None)
        if sheet_name is None or sheet_name == "":
            sheet_name = constants.DEFAULT_RESULTS_SHEET_NAME
        logging.info(f"sheet_name: {sheet_name}")

        header_row_number = self.config.get("gene_file", None).get(
            "header_row_number", None
        )
        if header_row_number is None or header_row_number == "":
            header_row_number = constants.DEFAULT_HEADER_ROW_NUMBER
        logging.info(f"header_row_number: {header_row_number}")

        # Read the Excel file
        df = pd.read_excel(
            infile,
            sheet_name=sheet_name,
            header=header_row_number,
            engine="xlrd",  # Need to install the following package to read Excel files with .xls extension: pip install xlrd==2.0.1
        )

        # Check if the expected columns are present
        expected_columns = [
            "Well",
            "Well Position",
            "Sample Name",
            "Target Name",
            "Quantity",
            "Quantity Mean",
            "Quantity SD",
            "Y-Intercept",
            "R(superscript 2)",
            "Slope",
            "Efficiency",
            "Amp Status",
        ]

        missing_columns = [col for col in expected_columns if col not in df.columns]

        if missing_columns:
            raise Exception(f"Missing columns in the DataFrame: {missing_columns} while processing file '{os.path.basename(infile)}'")

        # Remove all records where all cells are empty
        df = df.dropna(how="all")

        # Extract the relevant rows and columns
        df = df.loc[0:, expected_columns]

        # Replace NaN values with an empty string
        df.fillna(0.0, inplace=True)

        record_number = 0

        for index, row in df.iterrows():
            record_number += 1

            row_dict = row.to_dict()

            try:
                record = Record(**row_dict)

                self.rec_list.append(record)

                self.rec_ctr += 1

            except ValidationError as exc:
                print(repr(exc.errors()[0]["type"]))
                missing_fields = [
                    error["loc"][0]
                    for error in exc.errors()
                    if error["msg"] == "field required"
                ]
                print("Missing fields:", missing_fields)
                print(exc.errors())
                sys.exit(1)
                # > 'missing'

            except Exception as e:
                if (row["Quantity Mean"] is None or row["Quantity Mean"] == "") and (
                    row["Sample Name"] in ("STD 1", "STD 2", "STD 3", "STD 4", "STD 5")
                    or row["Sample Name"].startswith("NTC - REP")
                    or row["Sample Name"] == "EXTRACT NEG"
                    or row["Sample Name"] == "NTC"
                ):
                    logging.warning(
                        f"Encountered a record with no quantity mean value for sample name '{row['Sample Name']}'"
                    )
                elif (row["Quantity Mean"] is None or row["Quantity Mean"] == "") and (
                    row["Sample Name"] is None or row["Sample Name"] == ""
                ):
                    logging.error(
                        "Encountered a record with no quantity mean value and no sample name"
                    )
                else:
                    logging.error(
                        f"Encountered some exception with record number '{record_number}': {e}"
                    )
                    raise e
                    self.error_ctr += 1
                    self.error_list.append(e)

                sys.exit(1)
            record_ctr += 1

        logging.info(f"Processed '{record_ctr}' records in data file '{infile}'")

        if self.error_ctr > 0:
            self._write_validation_report(infile)
            sys.exit(1)

        self.is_parsed = True
        return self.rec_list
