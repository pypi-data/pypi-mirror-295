import logging
from typing import Any, Iterator, List, Optional, Tuple

from regscale.core.app.utils.app_utils import epoch_to_datetime, extract_vuln_id_from_strings
from regscale.integrations.scanner_integration import IntegrationAsset, IntegrationFinding, ScannerIntegration
from regscale.integrations.variables import ScannerVariables
from regscale.models import ControlTestResultStatus, regscale_models
from regscale.models.integration_models.tenable_models.models import TenableAsset

logger = logging.getLogger(__name__)


class SCIntegration(ScannerIntegration):
    finding_severity_map = {
        "Info": regscale_models.IssueSeverity.Low,
        "Low": regscale_models.IssueSeverity.Low,
        "Medium": regscale_models.IssueSeverity.Moderate,
        "High": regscale_models.IssueSeverity.High,
        "Critical": regscale_models.IssueSeverity.High,
    }
    # Required fields from ScannerIntegration
    title = "Tenable SC"
    asset_identifier_field = "tenableId"

    def fetch_assets(self, *args: Any, **kwargs: Any) -> Iterator[IntegrationAsset]:
        """
        Fetches assets from SCIntegration

        :param Tuple args: Additional arguments
        :param dict kwargs: Additional keyword arguments
        :yields: Iterator[IntegrationAsset]
        """
        integration_assets = kwargs.get("integration_assets")
        for asset in integration_assets:
            yield asset

    def fetch_findings(self, *args: Tuple, **kwargs: dict) -> Iterator[IntegrationFinding]:
        """
        Fetches findings from the SCIntegration

        :param Tuple args: Additional arguments
        :param dict kwargs: Additional keyword arguments
        :yields: Iterator[IntegrationFinding]

        """
        integration_findings = kwargs.get("integration_findings")
        for vuln in integration_findings:
            yield vuln

    def parse_findings(self, vuln: TenableAsset) -> List[IntegrationFinding]:
        """
        Parses a TenableAsset into an IntegrationFinding object

        :param TenableAsset vuln: The Tenable SC finding
        :return: An IntegrationFinding object
        :rtype: List[IntegrationFinding]
        """
        findings = []
        try:
            severity = self.finding_severity_map.get(vuln.severity.name, regscale_models.IssueSeverity.Low)
            cve_list = vuln.cve.split(",") if vuln.cve else []
            for cve in set(cve_list):
                if severity != regscale_models.IssueSeverity.Low:
                    findings.append(
                        IntegrationFinding(
                            control_labels=[],  # Add an empty list for control_labels
                            category="Tenable SC Vulnerability",  # Add a default category
                            dns=vuln.dnsName,
                            title=vuln.pluginName.split(":")[0] if vuln.pluginName else vuln.pluginName,
                            description=vuln.description,
                            severity=severity,
                            status=regscale_models.IssueStatus.Open,  # Findings of > Low are considered as FAIL
                            asset_identifier=vuln.dnsName,
                            external_id=vuln.pluginID,
                            first_seen=epoch_to_datetime(vuln.firstSeen),
                            last_seen=epoch_to_datetime(vuln.lastSeen),
                            recommendation_for_mitigation=vuln.solution,
                            cve=cve,
                            cvss_v3_score=float(vuln.cvssV3BaseScore) if vuln.cvssV3BaseScore else 0.0,
                            plugin_id=vuln.pluginID,
                            plugin_name=vuln.pluginName,
                            rule_id=vuln.pluginID,
                            rule_version=vuln.pluginName,
                            basis_for_adjustment="Tenable SC import",
                            vulnerability_type="Tenable SC Vulnerability",
                            vulnerable_asset=vuln.dnsName,
                        )
                    )
        except (KeyError, TypeError, ValueError) as e:
            self.logger.error("Error parsing Tenable SC finding: %s", str(e), exc_info=True)
        return findings

    def to_integration_asset(self, asset: TenableAsset, **kwargs: dict) -> IntegrationAsset:
        """Converts a TenableAsset object to an IntegrationAsset object

        :param TenableAsset asset: The Tenable SC asset
        :param dict **kwargs: Additional keyword arguments
        :return: An IntegrationAsset object
        :rtype: IntegrationAsset
        """
        app = kwargs.get("app")
        config = app.config
        name = asset.dnsName if asset.dnsName else asset.ip
        return IntegrationAsset(
            name=name,
            identifier=asset.dnsName,
            ip_address=asset.ip,
            mac_address=asset.macAddress,
            asset_owner_id=config["userId"],
            status="Active (On Network)" if asset.family.type else "Off-Network",
            asset_type="Other",
            asset_category="Hardware",
        )
