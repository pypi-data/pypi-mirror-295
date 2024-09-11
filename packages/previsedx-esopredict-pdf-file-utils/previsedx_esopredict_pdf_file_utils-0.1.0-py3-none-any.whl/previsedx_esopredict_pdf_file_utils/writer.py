# -*- coding: utf-8 -*-
"""Class for writing the Esopredict final report PDF file."""
import logging
import os

from typing import Dict, Optional, Union

from pdfrw import IndirectPdfDict, PdfReader, PdfWriter

from previsedx_esopredict_pdf_file_utils import constants
from previsedx_esopredict_pdf_file_utils.file_utils import check_infile_status


class Writer:
    """Class for writing the Esopredict final report PDF file."""

    def __init__(self, **kwargs):
        """Constructor for Manager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.template_path = kwargs.get("template_path", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        if self.template_path is None or self.template_path == "":
            self.template_path = self.config.get("report", None).get(
                "template_path", None
            )
            if self.template_path is None or self.template_path == "":
                raise Exception(
                    f"Could not derive the template_path from the configuration file '{self.config_file}'"
                )

        self.map = self.config.get("report", None).get("map", None)
        if self.map is None:
            raise Exception(
                f"Could not derive the map from the configuration file '{self.config_file}'"
            )

        logging.info(f"Instantiated Writer in file '{os.path.abspath(__file__)}'")

    def _get_template_field(self, annotation, annotation_type: str) -> Optional[str]:
        template_field = annotation[annotation_type]
        if template_field.startswith("(") and template_field.endswith(")"):
            template_field = template_field[1:-1]
            logging.info("Derived template_field from the annotation object")
            return template_field
        else:
            logging.info("The template field is not wrapped in parentheses for the current annotation object")
            return None

    def _get_field_map_key(
        self,
        template_field: str
    ) -> Optional[str]:

        if template_field not in self.map:
            logging.info(
                f"Ignoring template field '{template_field}' because does not exist in the map"
            )
            return None
        else:
            field_map_key = self.map[template_field]
            logging.info(f"Derived field_map_key '{field_map_key}' for template_field '{template_field}'")
            return field_map_key

    def _get_value(self, field_map_key, kwargs) -> Union[str, int]:
        """Retrieve the value for the specified field.

        Args:
            field_map_key (str): The field map key.
            kwargs (Dict[str, Any]): The keyword arguments.

        Returns:
            Union[str,int]: The value for the field map key.
        """
        if field_map_key not in kwargs:
            raise Exception(
                f"'{field_map_key=}' was not found in the kwargs"
            )

        val = kwargs[field_map_key]
        logging.info(f"Derived value '{val}' for field_map_key '{field_map_key}'")
        return val

    def write_file(self, **kwargs) -> None:
        #     patient_name: str,
        #     provider_name: str,
        #     date_of_birth: str,
        #     gender: str,
        #     medical_record_id: str,
        #     previse_lab_id: str,
        #     specimen_id: str,
        #     collection_date: str,
        #     date_received: str,
        #     date_reported: str,
        #     clinic: str,
        #     address: str,
        #     city_state_zip: str,
        #     treating_provider: str,
        #     barretts_diagnosis: str,
        #     segment_length: str,
        #     risk_level: str,
        #     range_score: str,
        #     five_year_probability_of_progression: str,
        # ) -> None:
        """Write the final report PDF file.

        Args:
            patient_name (str): The patient name.
            provider_name (str): The provider name.
            date_of_birth (str): The date of birth.
            gender (str): The patient gender.
            medical_record_id (str): The medical record ID.
            previse_lab_id (str): The Previse Lab ID.
            specimen_id (str): The specimen ID.
            collection_date (str): The collection date.
            date_received (str): The date received.
            date_reported (str): The date reported.
            clinic (str): The clinic.
            address (str): The address.
            city_state_zip (str): The city, state, and ZIP.
            treating_provider (str): The treating provider.
            barretts_diagnosis (str): The Barrett's diagnosis.
            segment_length (str): The segment length.
            risk_level (str): The risk level.
            range_score (str): The range score.
            five_year_probability_of_progression (str): The five-year probability of progression.
        """

        template_path = self.template_path
        check_infile_status(template_path)

        reader = PdfReader(template_path)

        logging.info(f"{kwargs=}")
        logging.info(f"{self.map=}")

        for page in reader.pages:
            if page.Annots:
                found_lookup = {}
                found_ctr = 0

                is_patient_name_found = False
                is_provider_name_found = False

                for annotation in page.Annots:
                    # logging.info(annotation['/T'])
                    if annotation.update and "/T" in annotation:

                        template_field = self._get_template_field(annotation, "/T")
                        if template_field is None:
                            continue

                        if template_field == "I interval":
                            template_field = "C.I interval"

                        field_map_key = self._get_field_map_key(template_field)
                        if field_map_key is None:
                            continue

                        val = self._get_value(field_map_key, kwargs)

                        if field_map_key == "interval":
                            print(f"Here is the interval: {val}")

                            # Debugging statements
                            # print(f"Updating annotation for field: {template_field}")
                            print(f"Annotation before update: {annotation}")
                            print(f"Value to update: {val}")
                        annotation.update(IndirectPdfDict(V=str(val)))

                        if field_map_key == "interval":
                            # Verify if the update was successful
                            print(f"Annotation after update: {annotation}")

                        if self.verbose:
                            print(
                                f"Updated '{annotation['/T']}' with value '{val}'"
                            )
                        logging.info(
                            f"Updated '{annotation['/T']}' with value '{val}'"
                        )
                        found_lookup[template_field] = True
                        found_ctr += 1
                    elif annotation.update and "/TU" in annotation:
                        template_field = self._get_template_field(annotation, "/TU")
                        if template_field is None:
                            continue

                        field_map_key = self._get_field_map_key(template_field)
                        if field_map_key is None:
                            continue

                        val = self._get_value(field_map_key, kwargs)

                        print(f"TU || Annotation before update: {annotation}")
                        print(f"TU || Value to update: {val}")
                        annotation.update(IndirectPdfDict(V=str(val)))

                        # Verify if the update was successful
                        print(f"TU || Annotation after update: {annotation}")
                        found_lookup[template_field] = True
                        found_ctr += 1

                # Check whether all fields were found
                self._check_missing_fields(
                    found_lookup,
                    is_patient_name_found,
                    is_provider_name_found
                )

        self.outfile = self.outfile.replace(" ", "_")

        PdfWriter().write(self.outfile, reader)

        if self.verbose:
            print(f"Wrote PDF final report file '{self.outfile}'")
        logging.info(f"Wrote PDF final report file '{self.outfile}'")

    def _check_missing_fields(
        self,
        found_lookup: Dict[str, bool],
        is_patient_name_found: bool,
        is_provider_name_found: bool
    ) -> None:
        missing_list = []
        missing_ctr = 0
        for field in self.map:
            if field not in found_lookup:
                if self.verbose:
                    print(f"Field '{field}' not found")
                logging.error(f"Field '{field}' not found")
                missing_list.append(field)
                missing_ctr += 1

        if missing_ctr > 0:
            if self.verbose:
                print(
                    f"Did not find the following '{len(missing_list)}' fields:"
                )
            logging.error(
                f"Did not find the following '{len(missing_list)}' fields:"
            )
            for missing_field in missing_list:
                logging.error(f"\t{missing_field}")

        if not is_patient_name_found:
            logging.error("Patient name not inserted")

        if not is_provider_name_found:
            logging.error("Provider name not inserted")
