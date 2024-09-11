"""
Aqua Scan information
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import groupby
from operator import attrgetter
from typing import Any, List, Optional

from dateutil.parser import ParserError, parse

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime, is_valid_fqdn
from regscale.models.app_models.mapping import Mapping
from regscale.models.integration_models.flat_file_importer import FlatFileImporter
from regscale.models.regscale_models import SoftwareInventory
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.vulnerability import Vulnerability


class Aqua(FlatFileImporter):
    """Aqua Scan information"""

    def __init__(self, **kwargs: dict):
        self.name = kwargs.get("name")
        regscale_ssp_id = kwargs.get("regscale_ssp_id")
        self.vuln_title = "Vulnerability Name"
        self.fmt = "%m/%d/%Y"
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        self.image_name = "Image Name"
        self.ffi = "First Found on Image"
        self.last_image_scan = "Last Image Scan"
        self.installed_version = "Installed Version"
        self.vendor_cvss_v2_severity = "Vendor CVSS v2 Severity"
        self.vendor_cvss_v3_severity = "Vendor CVSS v3 Severity"
        self.vendor_cvss_v3_score = "Vendor CVSS v3 Score"
        self.nvd_cvss_v2_severity = "NVD CVSS v2 Severity"
        self.nvd_cvss_v3_severity = "NVD CVSS v3 Severity"
        self.headers = [
            "Registry",
            self.image_name,
            "Image Build Date",
            "Image Digest",
            "OS",
            "Resource",
            "Resource Type",
            self.installed_version,
            self.vuln_title,
            "Publish Date",
            "Referenced By",
            self.vendor_cvss_v2_severity,
            "Vendor CVSS v2 Score",
            "Vendor CVSS v2 Vectors",
            self.vendor_cvss_v3_severity,
            self.vendor_cvss_v3_score,
            "Vendor CVSS v3 Vectors",
            "Vendor URL",
            self.nvd_cvss_v2_severity,
            "NVD CVSS v2 Score",
            "NVD CVSS v2 Vectors",
            self.nvd_cvss_v3_severity,
            "NVD CVSS v3 Score",
            "NVD CVSS v3 Vectors",
            "NVD URL",
            "Fix Version",
            "Solution",
            "Qualys IDs",
            "Description",
            "Applied By",
            "Applied On",
            "Reverted By",
            "Reverted On",
            "Enforced By",
            "Enforced On",
            "vShield Status",
            "Suppression Date",
            "Base Image Vulnerability",
            "Base Image Name",
            "Aqua score",
            "Aqua severity",
            "Aqua Vectors",
            "Aqua custom severity",
            "Aqua custom notes",
            self.ffi,
            self.last_image_scan,
            "Exploit Availability",
            "Temporal Vector",
            "Exploit Type",
            "Namespace",
            "Resource Path",
        ]
        logger = create_logger()
        kwargs, mapping = self.update_mapping(kwargs)
        self.mapping = mapping
        super().__init__(
            logger=logger,
            headers=mapping.to_header(),
            parent_id=regscale_ssp_id,
            parent_module="securityplans",
            asset_func=self.create_asset,
            vuln_func=self.create_vuln,
            app=Application(),
            ignore_validation=True,
            **kwargs,
        )
        self.create_software_inventory()

    def create_asset(self, dat: Optional[dict] = None) -> Optional[Asset]:
        """
        Create an asset from a row in the Aqua file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Asset object or None
        :rtype: Optional[Asset]
        """
        name = dat[self.image_name]
        if not name:
            return None
        return Asset(
            **{
                "id": 0,
                "name": name,
                "description": "",
                "operatingSystem": Asset.find_os(dat["OS"]),
                "operatingSystemVersion": dat["OS"],
                "ipAddress": "0.0.0.0",
                "isPublic": True,
                "status": "Active (On Network)",
                "assetCategory": "Hardware",
                "bLatestScan": True,
                "bAuthenticatedScan": True,
                "scanningTool": self.name,
                "assetOwnerId": self.config["userId"],
                "assetType": "Other",
                "fqdn": name if is_valid_fqdn(name) else None,
                "systemAdministratorId": self.config["userId"],
                "parentId": self.attributes.parent_id,
                "parentModule": self.attributes.parent_module,
            }
        )

    def create_software_inventory(self) -> List[SoftwareInventory]:
        """
        Create and post a list of software inventory for a given asset

        :return: List of software inventory
        :rtype: List[SoftwareInventory]
        """
        scanned_assets = [
            asset for asset in self.data["assets"] if asset.id in {vuln.parentId for vuln in self.data["vulns"]}
        ]
        self.attributes.logger.info(f"Processing inventory for {len(scanned_assets)} scanned asset(s)...")
        software_inventory = []
        for asset in scanned_assets:
            software_inventory.extend(SoftwareInventory.fetch_by_asset(self.attributes.app, asset.id))
        hardware = sorted(
            [asset for asset in scanned_assets if asset.assetCategory == "Hardware"],
            key=attrgetter("name"),
        )
        grouping = {key: list(group) for key, group in groupby(hardware, key=attrgetter("name"))}

        def process_group(key: Any, group: list) -> None:
            """
            Process a group of assets and create a software inventory for each asset

            :param Any key: Key for the group
            :param list group: Group of assets
            :rtype: None
            """
            # Do something
            group_rows = [row for row in self.file_data if row[self.image_name] == key]
            for software in group_rows:
                inv = SoftwareInventory(
                    name=software["Resource"],
                    version=str(software[self.installed_version]),
                    createdById=self.config["userId"],
                    dateCreated=get_current_datetime(),
                    lastUpdatedById=self.config["userId"],
                    isPublic=True,
                )
                inv.parentHardwareAssetId = group[0].id
                if inv not in software_inventory:
                    software_inventory.append(SoftwareInventory.insert(self.attributes.app, inv))

        with ThreadPoolExecutor() as executor:
            for key, group in grouping.items():
                executor.submit(process_group, key, group)
        self.attributes.logger.info(f"Successfully processed {len(software_inventory)} software item(s).")
        return software_inventory

    def determine_date(self, dat: dict, key: str) -> Optional[str]:
        """
        Determine the date of the vulnerability

        :param dict dat: Data row from CSV file
        :param str key: Key for the date
        :return: Date of the vulnerability
        :rtype: Optional[str]
        """
        res = None
        try:
            return datetime.strptime(dat[key], self.fmt).strftime(self.dt_format)
        except (ValueError, TypeError):
            if isinstance(dat[key], str):
                try:
                    return parse(dat[key]).strftime(self.dt_format)
                except ParserError:
                    self.attributes.logger.warning(f"Unable to parse date: {dat[key]}")
        return res

    def create_vuln(self, dat: Optional[dict] = None) -> Optional[Vulnerability]:
        """
        Create a vulnerability from a row in the Aqua csv file

        :param Optional[dict] dat: Data row from CSV file, defaults to None
        :return: RegScale Vulnerability object or None
        :rtype: Optional[Vulnerability]
        """
        regscale_vuln = None
        severity = self.determine_cvss_severity(dat)
        hostname = dat[self.image_name]
        description = dat["Description"]
        solution = dat["Solution"] if dat.get("Solution") else "Upgrade affected package"
        config = self.attributes.app.config
        asset_match = [asset for asset in self.data["assets"] if asset.name == hostname]
        asset = asset_match[0] if asset_match else None
        if asset_match:
            first_seen = self.determine_date(dat, self.ffi)
            last_seen = self.determine_date(dat, self.last_image_scan)
            regscale_vuln = Vulnerability(
                id=0,
                scanId=0,
                parentId=asset.id,
                parentModule="assets",
                ipAddress="0.0.0.0",
                lastSeen=last_seen if first_seen else get_current_datetime(),
                firstSeen=first_seen if first_seen else get_current_datetime(),
                daysOpen=None,
                dns=hostname,
                mitigated=None,
                operatingSystem=asset.operatingSystem,
                severity=severity,
                plugInName=description,
                cve=dat[self.vuln_title],
                cvsSv3BaseScore=dat[self.vendor_cvss_v3_score],
                tenantsId=0,
                title=description[:255],
                description=description,
                plugInText=dat[self.vuln_title],
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateCreated=get_current_datetime(),
                extra_data={"solution": solution},
            )
        return regscale_vuln

    def determine_cvss_severity(self, dat: dict) -> str:
        """
        Determine the CVSS severity of the vulnerability

        :param dict dat: Data row from CSV file
        :return: A severity derived from the CVSS scores
        :rtype: str
        """
        precedence_order = [
            self.nvd_cvss_v3_severity,
            self.nvd_cvss_v2_severity,
            self.vendor_cvss_v3_severity,
            # This field may or may not be available in the file (Coalfire has it, BMC does not.)
            self.vendor_cvss_v2_severity if dat.get(self.vendor_cvss_v2_severity) else None,
        ]
        severity = "info"
        for key in precedence_order:
            if key and dat.get(key):
                severity = dat[key].lower()
                break
        # remap crits to highs
        if severity == "critical":
            severity = "high"
        return severity

    def default_mapping(self) -> Mapping:
        """
        Default mapping for the Nexpose csv file if one is not provided
        """
        headers = [
            "Registry",
            self.image_name,
            "Image Build Date",
            "Image Digest",
            "OS",
            "Resource",
            "Resource Type",
            self.installed_version,
            self.vuln_title,
            "Publish Date",
            "Referenced By",
            self.vendor_cvss_v2_severity,
            "Vendor CVSS v2 Score",
            "Vendor CVSS v2 Vectors",
            self.vendor_cvss_v3_severity,
            self.vendor_cvss_v3_score,
            "Vendor CVSS v3 Vectors",
            "Vendor URL",
            self.nvd_cvss_v2_severity,
            "NVD CVSS v2 Score",
            "NVD CVSS v2 Vectors",
            self.nvd_cvss_v3_severity,
            "NVD CVSS v3 Score",
            "NVD CVSS v3 Vectors",
            "NVD URL",
            "Fix Version",
            "Solution",
            "Qualys IDs",
            "Description",
            "Applied By",
            "Applied On",
            "Reverted By",
            "Reverted On",
            "Enforced By",
            "Enforced On",
            "vShield Status",
            "Suppression Date",
            "Base Image Vulnerability",
            "Base Image Name",
            "Aqua score",
            "Aqua severity",
            "Aqua Vectors",
            "Aqua custom severity",
            "Aqua custom notes",
            self.ffi,
            self.last_image_scan,
            "Exploit Availability",
            "Temporal Vector",
            "Exploit Type",
            "Namespace",
            "Resource Path",
        ]
        expected = [
            self.image_name,
            "OS",
            self.last_image_scan,
            self.ffi,
            self.vuln_title,
            self.vendor_cvss_v3_score,
            "Description",
            "Solution",
            self.nvd_cvss_v3_severity,
            self.nvd_cvss_v2_severity,
            self.vendor_cvss_v3_severity,
        ]
        mapping_dict = {"mapping": {header: header for header in headers}, "expected_field_names": expected}
        return Mapping(**mapping_dict)
