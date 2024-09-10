#!/usr/bin/env python3
""" Convert Python code modules to JSON and CSV for publication.

When adding new modules:

- Import module
- Add new module to for loop in __main__
"""
import json
import csv
from pathlib import Path

from fhir.resources.bundle import Bundle, BundleEntry

from open_ortho_terminology.terminology import hl7, open_ortho, snomed, dentaleyepad, vendors
from open_ortho_terminology.terminology import Code

import logging
logger = logging.getLogger(__name__)

build_path = Path('.', 'build')


def save_to_fhir(module, filename):
    codes = {name: getattr(module, name) for name in dir(module)
               if isinstance(getattr(module, name), Code)}

    data = None
    if codes:
        b = Bundle(type='collection')
        b.entry = []
        for name, code in codes.items():
            be = BundleEntry()
            be.resource = code.to_fhir()
            b.entry.append(be)

        data = b.dict()

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'System', 'Code', 'Display'])
        for key, value in data.items():
            writer.writerow(
                [key, value['system'], value['code'], value['display']])


def module_to_dict(module):
    """ Convert module to dict.

    Handles both Code modules and fhir.resource.coding.Coding modules.
    """
    Codes = {name: getattr(module, name) for name in dir(module)
             if isinstance(getattr(module, name), Code)}

    if Codes:
        # Convert Code instances to dictionaries for JSON and CSV
        return {
            name: {
                'system': code.system,
                'code': code.code,
                'full_code': code.full_code,
                'display': code.display,
                'synonyms': code.synonyms,
                'contexts': code.contexts
            } for name, code in Codes.items()}


if __name__ == "__main__":
    for module in (snomed, hl7, vendors, open_ortho, dentaleyepad):
        dict_module = module_to_dict(module)
        save_to_fhir(module, build_path / f'{module.__name__}_fhir.json')
        save_to_json(dict_module, build_path / f'{module.__name__}.json')
        try:
            save_to_csv(dict_module, build_path / f'{module.__name__}.csv')
        except Exception as e:
            # logger.exception(e)
            logger.warning(
                f"Error while trying to save {module.__name__} to CSV.")
