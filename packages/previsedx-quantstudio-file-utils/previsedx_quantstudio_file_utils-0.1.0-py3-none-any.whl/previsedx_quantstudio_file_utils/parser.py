"""Class for parsing Thermo Fisher Scientific QuantStudio qPCR Result Excel
files."""
import logging
import os
import pandas as pd

from datetime import datetime

from previsedx_quantstudio_file_utils import constants


# Need to install the following package to read Excel files with .xls extension.
# pip install xlrd==2.0.1


class Parser:
    """Class for parsing Thermo Fisher Scientific QuantStudio qPCR Result Excel
    files."""

    def __init__(self, **kwargs):
        """Constructor for Parser."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.is_parsed = False
        self.rec_ctr = 0
        self.rec_list = []

        self.error_ctr = 0
        self.error_list = []

        logging.info(f"Instantiated Parser in file '{os.path.abspath(__file__)}'")

    def _write_validation_report(self, infile: str) -> None:
        """Write the validation report file.

        Args:
            infile (str): The input QuantStudio qPCR Results file that was parsed.
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
