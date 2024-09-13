#!/usr/bin/env python3
# SPDX-License-Identifier: GTDGmbH
# Copyright 2020-2022 by GTD GmbH.

"""
The Main module of this application.
"""

import argparse
import os
import json
import hashlib
from typing import Any, Optional, Mapping
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import NullSection
from elftools.elf.constants import SH_FLAGS


class SectionNotFoundException(Exception):
    """
    Exception raised when a specified section isn't found
    """


def shorten_text_left(text: str, max_length: int):
    """
    Shorten a given text to be at most max_length characters,
    inserting '...' at the beginning when the text was shortened.

    :param text: Text which shall be shortened
    :param max_length: Maximum lenght of resulting text
    :returns: Shortened text

    >>> shorten_text_left("123456789", 7)
    '...6789'
    >>> shorten_text_left("123456789", 6)
    '...789'
    >>> shorten_text_left("123456789", 15)
    '123456789'
    """
    if len(text) <= max_length:
        return text

    return "..." + text[-max_length + 3 :]


def shorten_text_right(text: str, max_length: int):
    """
    Shorten a given text to be at most max_length characters,
    inserting '...' at the end when the text was shortened.

    :param text: Text which shall be shortened
    :param max_length: Maximum lenght of resulting text
    :returns: Shortened text

    >>> shorten_text_right("123456789", 7)
    '1234...'
    >>> shorten_text_right("123456789", 6)
    '123...'
    >>> shorten_text_right("123456789", 15)
    '123456789'
    """
    if len(text) <= max_length:
        return text

    return text[0 : max_length - 3] + "..."


def compare_list_items(items: list[Any]):
    """
    Compare all items in a list for equality.

    :param items: The list of items to compare
    :returns: True when all items are equal, False otherwise
    """
    for i in range(len(items) - 1):
        if items[i] != items[i + 1]:
            return False
    return True


def all_data_is_zero(data: bytes):
    """
    Check that all given data is zero.

    :param data: Data block to be checked.
    :returns: True when all bytes are zero, False otherwise.
    """
    for byte in data:
        if byte != 0:
            return False
    return True


def create_first_header(bin_path: str, elf_info):
    """
    Create first header line of the report table
    """
    header = f"| {'Section Name':22} || "
    for path, _ in elf_info.items():
        header += f"{shorten_text_left(path, 36):36} || "
    header += f"{'Type':18} | "
    header += f"{'Flags':20} || "
    if bin_path is not None:
        header += f"{shorten_text_left(bin_path, 36):36} || "
    header += f"{'Errors':14} |\n"

    return header


def create_second_header(bin_path, elf_info):
    """
    Create second header line of the report table
    """
    header = f"| {'':22} || "
    for _, _ in elf_info.items():
        header += f"{'Address':10} | "
        header += f"{'Length':10} | "
        header += f"{'Alignment':10} || "
    header += f"{'':18} | "
    header += f"{'':20} || "
    if bin_path is not None:
        header += f"{'Offset':10} | "
        header += f"{'Length':10} | "
        header += f"{'Alignment':10} || "
    header += f"{'':>14} |\n"

    return header


def create_divider(bin_path, elf_info):
    """
    Create divider line between header and body of report table
    """
    # fmt: off
    return (
        "| "
        + "-" * 22 + " || "
        + (2 * ("-" * 10 + " | ") + ("-" * 10 + " || ")) * len(elf_info.items())
        + "-" * 18 + " | "
        + "-" * 20 + " || "
        + (2 * ("-" * 10 + " | ") + ("-" * 10 + " || ")) * (bin_path is not None)
        + "-" * 14 + " |\n"
    )
    # fmt: on


class ELFChecker:
    """
    Main class implementing the ELF Checker
    """

    def __init__(self, elf_paths: list[str], bin_path: str | None):
        """
        Create a new ELF Checker instance and register the given files.

        :param elf_paths: List of paths to ELF files
        :param bin_path: Path to bin file
        :param bin_sections: List of sections included in the bin file
        """
        self.elf_info: dict[str, dict[str, Any]] = {path: {} for path in elf_paths}
        self.bin_path = bin_path
        self.bin_info: Mapping[str, Optional[list[str]]] = {"sections": None}
        self.open_elf_files()
        self.read_elf_sections()
        self.info: dict[str, Any] = {
            "file_info": {path: [] for path in elf_paths + [bin_path]},
            "errors": {"padding": []},
        }
        self.report = ""
        self.bin_file_start_offset = 0

    def register_bin_sections(self, bin_sections: list[str]):
        """
        Register list of sections expected to be in the binary file
        """
        self.bin_info = {"sections": bin_sections}
        self.calc_bin_file_start_offsets()

    def open_elf_files(self):
        """
        Open all registered ELF files.
        """
        for path, info in self.elf_info.items():
            info["fd"] = open(path, "rb")
            info["elf"] = ELFFile(info["fd"])

    def to_json(self):
        """
        Generate JSON report
        """
        return json.dumps(self.info, indent=2)

    def read_elf_sections(self):
        """
        Read all section headers of all registered ELF files.
        """
        for _, info in self.elf_info.items():
            info["sections"] = {}
            for section in info["elf"].iter_sections():
                if not isinstance(section, NullSection):
                    info["sections"][section.name] = section

    def calc_bin_file_start_offsets(self):
        """
        Calculate the load offset of the given binary, using the section
        with the lowest address.
        """
        if self.bin_info["sections"] is not None:
            self.bin_file_start_offset = self.get_section_header_by_name(
                sorted(self.bin_info["sections"], key=self.get_sort_key_of_section)[0]
            ).sh_addr

    def get_section_header_by_name(self, section: str):
        """
        Get the the section header by name from the first registered ELF
        file which has this section.

        Raises an Exception when no ELF file with such a section is
        found.

        :param section: The name of the section
        :returns: The section header
        """
        for _, info in self.elf_info.items():
            if section in info["sections"]:
                return info["sections"][section].header
        raise SectionNotFoundException(section)

    def get_bin_file_section(self, address: int, length: int):
        """
        Get the data of section from the bin file.

        :param address: address in the bin file
        :param length: length of the requested data
        :returns: Length bytes at address in bin file
        """
        assert self.bin_path

        with open(self.bin_path, "rb") as bin_file:
            bin_file.seek(address)
            return bin_file.read(length)

    def get_sort_key_of_section(self, section: str):
        """
        Create a key based on the section address and its name for
        sorting.

        :param section: Section name
        :returns: Sorting key
        """
        return f"{self.get_section_header_by_name(section).sh_addr:08X}{section}"

    def readable_flags(self, flags: int):
        """
        Parse the ELF section header flags into a nice readable string.

        :param flags: The flags value from a section header
        :returns: String of section flags
        """
        known_flags = {
            "ALLOC": SH_FLAGS.SHF_ALLOC,
            "WRITE": SH_FLAGS.SHF_WRITE,
            "EXECINSTR": SH_FLAGS.SHF_EXECINSTR,
            "MERGE": SH_FLAGS.SHF_MERGE,
            "STRINGS": SH_FLAGS.SHF_STRINGS,
            "INFO_LINK": SH_FLAGS.SHF_INFO_LINK,
            "LINK_ORDER": SH_FLAGS.SHF_LINK_ORDER,
            "OS_NONCONFORMING": SH_FLAGS.SHF_OS_NONCONFORMING,
            "GROUP": SH_FLAGS.SHF_GROUP,
            "TLS": SH_FLAGS.SHF_TLS,
            "COMPRESSED": SH_FLAGS.SHF_COMPRESSED,
            "MASKOS": SH_FLAGS.SHF_MASKOS,
            "EXCLUDE": SH_FLAGS.SHF_EXCLUDE,
            "MASKPROC": SH_FLAGS.SHF_MASKPROC,
        }
        set_flags = []

        for flag, value in known_flags.items():
            if flags & value != 0:
                set_flags.append(flag)

        if len(set_flags) > 0:
            return ", ".join(set_flags)
        return "-"

    def readable_errors(self, errors: list[str]):
        """
        Create a readable string from a list of errors.

        :param errors: List of errors
        :returns: String of errors
        """
        if len(errors) > 0:
            return ", ".join(errors)
        return "-"

    def check_elf_sections(self):
        """
        Print a table listing relevant information for each ELF section
        and paddings in the bin file
        """
        # Get list of all available sections
        sections = []
        for _, info in self.elf_info.items():
            sections += info["sections"]

        report = create_first_header(self.bin_path, self.elf_info)
        report += create_second_header(self.bin_path, self.elf_info)
        report += create_divider(self.bin_path, self.elf_info)

        last_bin_file_header = None
        last_last_bin_file_header = None

        for section in sorted(set(sections), key=self.get_sort_key_of_section):
            errors = []
            self.info["errors"][section] = []

            # Check if the bin file has padding before the currently iterated section
            # Padding is not relevant for the very first section (i.e. at the beginning
            # of the bin file) as the bin file always starts with the first section
            # by definition
            if last_bin_file_header is not None and section in self.bin_info["sections"]:
                next_bin_file_offset = last_bin_file_header.sh_addr + last_bin_file_header.sh_size
                next_section_offset = self.get_section_header_by_name(section).sh_addr
                if next_bin_file_offset != next_section_offset:
                    padding_length = next_section_offset - next_bin_file_offset
                    report += f"| {'padding':>22} || "
                    report += f"{'-':>10} | {'-':>10} | {'-':>10} || " * len(self.elf_info)
                    report += f"{'-':18} | "
                    report += f"{'-':20} || "
                    report += (
                        f"{f'0x{next_bin_file_offset - self.bin_file_start_offset:08X}':>10} | "
                    )
                    report += f"{f'0x{padding_length:08X}':>10} | "
                    report += f"{f'-':>10} || "
                    section_data = self.get_bin_file_section(next_bin_file_offset, padding_length)
                    if not all_data_is_zero(section_data):
                        errors.append("Not Zero")
                    report += f"{shorten_text_left(self.readable_errors(errors), 14):14} |\n"
                    self.info["errors"]["padding"] += errors

                    self.info["file_info"][self.bin_path].append(
                        {
                            "data_type": "padding",
                            "address": next_bin_file_offset,
                            "size": padding_length,
                            "alignment": 0,
                            "data_sha256": hashlib.sha256(section_data).hexdigest(),
                        }
                    )
                last_bin_file_header = None

            errors = []

            # Print section name
            report += f"| {section:22} || "

            # Init temporary variables
            section_type = []
            section_flags = []
            section_addrs = []
            section_data = []

            # Print info from ELF files
            for path, info in self.elf_info.items():
                if section in info["sections"]:
                    header = info["sections"][section].header
                    report += f"{f'0x{header.sh_addr:08X}':>10} | "
                    report += f"{f'0x{header.sh_size:08X}':>10} | "
                    report += f"{f'0x{header.sh_addralign:02X}':>10} || "

                    section_addrs.append(header.sh_addr)
                    section_type.append(header.sh_type)
                    section_flags.append(header.sh_flags)
                    section_data.append(info["sections"][section].data())

                    self.info["file_info"][path].append(
                        {
                            "data_type": "elf_section",
                            "name": section,
                            "address": header.sh_addr,
                            "size": header.sh_size,
                            "alignment": header.sh_addralign,
                            "type": header.sh_type,
                            "flags": self.readable_flags(header.sh_flags),
                            "data_sha256": hashlib.sha256(
                                info["sections"][section].data()
                            ).hexdigest(),
                        }
                    )
                else:
                    report += f"{'-':>10} | "
                    report += f"{'-':>10} | "
                    report += f"{'-':>10} || "

            report += f"{shorten_text_left(section_type[0], 18):18} | "
            report += f"{shorten_text_right(self.readable_flags(section_flags[0]), 20):20} || "

            # Print info from bin file
            if self.bin_info["sections"] is not None and section in self.bin_info["sections"]:
                header = self.get_section_header_by_name(section)
                addr = header.sh_addr - self.bin_file_start_offset
                report += f"{f'0x{addr:08X}':>10} | "
                report += f"{f'0x{header.sh_size:08X}':>10} | "
                report += f"{f'0x{header.sh_addralign:02X}':>10} || "

                section_data.append(self.get_bin_file_section(addr, header.sh_size))

                self.info["file_info"][self.bin_path].append(
                    {
                        "data_type": "binary",
                        "name": section,
                        "address": addr,
                        "size": header.sh_size,
                        "alignment": header.sh_addralign,
                        "data_sha256": hashlib.sha256(
                            self.get_bin_file_section(addr, header.sh_size)
                        ).hexdigest(),
                    }
                )

                last_last_bin_file_header = last_bin_file_header = header
            elif self.bin_path is not None:
                report += f"{'-':>10} | "
                report += f"{'-':>10} | "
                report += f"{'-':>10} || "

            # Check and print errors
            if not compare_list_items(section_addrs):
                errors.append("Addr mismatch")
            if not compare_list_items(section_type):
                errors.append("Type mismatch")
            if not compare_list_items(section_flags):
                errors.append("Flags mismatch")
            if not compare_list_items(section_data):
                errors.append("Data mismatch")

            report += f"{shorten_text_left(self.readable_errors(errors), 14):14} |\n"

            self.info["errors"][section] += errors

        # Check that there is nothing after the last section in the bin file
        if last_last_bin_file_header is not None:
            errors = []

            next_bin_file_offset = (
                last_last_bin_file_header.sh_addr
                - self.bin_file_start_offset
                + last_last_bin_file_header.sh_size
            )
            file_length = os.stat(self.bin_path).st_size
            if next_bin_file_offset < file_length:
                padding_length = file_length - next_bin_file_offset
                report += f"| {'padding':>22} || "
                report += f"{'-':>10} | {'-':>10} | {'-':>10} || " * len(self.elf_info)
                report += f"{'-':18} | "
                report += f"{'-':20} || "
                report += f"{f'0x{next_bin_file_offset:08X}':>10} | "
                report += f"{f'0x{padding_length:08X}':>10} | "
                report += f"{f'-':>10} || "
                section_data = self.get_bin_file_section(next_bin_file_offset, padding_length)
                if not all_data_is_zero(section_data):
                    errors.append("Not Zero")
                report += f"{shorten_text_left(self.readable_errors(errors), 14):14} |\n"

                self.info["errors"]["padding"] += errors

                self.info["file_info"][self.bin_path].append(
                    {
                        "data_type": "padding",
                        "name": "",
                        "address": next_bin_file_offset,
                        "size": padding_length,
                        "data_sha256": hashlib.sha256(section_data).hexdigest(),
                    }
                )
            last_last_bin_file_header = None

        self.report = report


def main():  # pragma: no cover
    """
    The main function of the GTD ELF Checker. It parses the commandline
    arguments and creates an instance of the ELFChecker.
    """
    parser = argparse.ArgumentParser(description="GTD ELF Checker")
    parser.add_argument(
        "-e",
        "--elffile",
        type=str,
        required=True,
        nargs="+",
        help="List of paths to ELF files for inspection",
    )
    parser.add_argument(
        "-b",
        "--binfile",
        type=str,
        required=False,
        help="Path to a binary file for inspection",
    )
    parser.add_argument(
        "-j",
        "--only-section",
        type=str,
        required=False,
        nargs="+",
        help="List of sections which are part of the binary file for inspection",
    )
    args = parser.parse_args()

    e = ELFChecker(args.elffile, args.binfile)
    e.register_bin_sections(args.only_section)
    e.check_elf_sections()
    with open("report.json", "w", encoding="utf-8") as report:
        report.write(e.to_json())
    print(e.report, end="")


if __name__ == "__main__":  # pragma: no cover
    main()
