"""
Stig Mapper module
"""

import json
import logging
import os
from typing import List, Dict
from rich.progress import Progress

from regscale.models import SecurityPlan
from regscale.models.regscale_models import Asset, AssetMapping, Component


logger = logging.getLogger(__name__)


def equals(a: str, b: str) -> bool:
    """
    Compare two strings for equality.
    :param str a: The first string
    :param str b: The second string
    :return bool: True if the strings are equal, False otherwise
    :rtype: bool
    """
    return a == b


def contains(a: str, b: str) -> bool:
    """
    Check if string a contains string b.
    :param str a: The string to search
    :param str b: The string to find
    :return bool: True if a contains b, False otherwise
    :rtype: bool
    """
    return b in a


def startswith(a: str, b: str) -> bool:
    """
    Check if string a starts with string b.
    :param str a: The string to search
    :param str b: The string to find
    :return bool: True if a starts with b, False otherwise
    :rtype: bool
    """
    return a.startswith(b)


def notin(a: str, b: str) -> bool:
    """
    Check if string a does not contain string b.
    :param str a: The string to search
    :param str b: The string to find
    :return bool: True if a does not contain b, False otherwise
    :rtype: bool
    """
    return b not in a


def endswith(a: str, b: str) -> bool:
    """
    Check if string a ends with string b.
    :param str a: The string to search
    :param str b: The string to find
    :return bool: True if a ends with b, False otherwise
    :rtype: bool
    """
    return a.endswith(b)


# You can add more comparators if needed
comparator_functions = {
    "equals": equals,
    "contains": contains,
    "startswith": startswith,
    "notin": notin,
    "endswith": endswith,
}


class STIGMapper:
    """
    A class to map STIGs to assets based on rules.
    """

    def __init__(self, json_file: str):
        self.rules = self.load_rules(json_file)
        logger.info(f"Loaded {len(self.rules)} rules from {json_file}")

    @staticmethod
    def load_rules(json_file: str) -> List[Dict[str, str]]:
        """
        Load rules from a JSON file.
        :param str json_file: The path to the JSON file
        :return: A list of rules
        :rtype: List[Dict[str, str]]
        """
        if not os.path.exists(json_file):
            logger.error(f"File not found: {json_file}")
        with open(json_file, "r") as file:
            data = json.load(file)
            return data.get("rules", [])

    def map_stigs_to_assets(
        self,
        asset_list: List["Asset"],
        component_list: List[Component],
    ) -> List["AssetMapping"]:
        """
        Map STIGs to assets based on rules.
        :param List[Asset] asset_list: A list of assets
        :param List[Component] component_list: A list of components
        :return: A list of asset mappings
        :rtype: List[AssetMapping]
        """
        new_asset_mappings = []
        for rule in self.rules:
            stig_name = rule.get("stig")
            comparators = rule.get("comparators", [])
            existing_mappings = []
            component_id = None
            for component in component_list:
                if component.title == stig_name:
                    component_id = component.id
                    existing_mappings.extend(AssetMapping.find_mappings(component_id=component_id))
                    break
            if not component_id:
                continue
            matching_assets = self.find_matching_assets(asset_list=asset_list, comparators=comparators)
            for asset in matching_assets:
                asset_mapping = AssetMapping(
                    assetId=asset.id,
                    componentId=component_id,
                )
                mapping_already_exists = self.mapping_exists(asset_mapping, existing_mappings)
                mapping_in_new_mappings = asset_mapping in new_asset_mappings
                if not mapping_already_exists and not mapping_in_new_mappings:
                    logger.info(f"Mapping -> Asset ID: {asset.id}, Component ID: {component_id}")
                    new_asset_mappings.append(asset_mapping)
                else:
                    logger.info(f"Existing mapping found for Asset ID: {asset.id}, Component ID: {component_id}")
        return new_asset_mappings

    @staticmethod
    def save_all_mappings(mappings: List[AssetMapping]) -> None:
        """
        Save all asset mappings.
        :param List[AssetMapping] mappings: A list of asset mappings
        :rtype: None
        """
        for asset_mapping in mappings:
            asset_mapping.create()

    @staticmethod
    def mapping_exists(asset_mapping: AssetMapping, existing_mappings: List[AssetMapping]) -> bool:
        """
        Check if the asset mapping already exists.
        :param AssetMapping asset_mapping:
        :param List[AssetMapping] existing_mappings:
        :return: True if the mapping exists, False otherwise
        :rtype: bool
        """
        for existing_mapping in existing_mappings:
            if (
                existing_mapping.assetId == asset_mapping.assetId
                and existing_mapping.componentId == asset_mapping.componentId
            ):
                return True
        return False

    @staticmethod
    def find_matching_assets(asset_list: List, comparators: List[Dict[str, str]]) -> List:
        """
        Find matching assets based on multiple comparator rules.

        :param List asset_list: A list of assets
        :param List[Dict[str, str]] comparators: A list of comparators,
            each containing the property, value, and operator
        :return List: A list of matching assets
        :rtype: List
        """
        matching_assets = []

        for asset in asset_list:
            match = True
            # Iterate over the comparators list
            for comparator in comparators:
                property_name = comparator.get("property")
                value = comparator.get("value")
                operator = comparator.get("comparator")

                # Get the comparison function based on the operator
                comparator_func = comparator_functions.get(operator, None)

                # Ensure the asset has the property, and the comparison function exists
                if not hasattr(asset, property_name) or not comparator_func:
                    match = False
                    break

                asset_value = getattr(asset, property_name)

                # Apply the comparator function to determine if the asset matches the rule
                if not comparator_func(asset_value, value):
                    match = False
                    break

            if match:
                matching_assets.append(asset)

        return matching_assets

    @staticmethod
    def find_matching_stigs(asset: Asset, comparators: List[Dict[str, str]]) -> bool:
        """
        Find matching stigs based on multiple comparator rules.
        :param Asset asset: An asset
        :param List[Dict[str, str]] comparators: List of comparators
        :return: A list of matching stigs
        :rtype: List
        """
        match = True
        # Iterate over the comparators list
        for comparator in comparators:
            match = True
            property_name = comparator.get("property")
            value = comparator.get("value")
            operator = comparator.get("comparator")

            # Get the comparison function based on the operator
            comparator_func = comparator_functions.get(operator, None)

            # Ensure the asset has the property, and the comparison function exists
            if not hasattr(asset, property_name) or not comparator_func:
                match = False
                break

            asset_value = getattr(asset, property_name)
            if asset_value == "regml-container" and value == "regml-container":
                logger.debug(f"Asset Value: {asset_value} | Comparator operator {operator} | Comparator Value: {value}")
            # Apply the comparator function to determine if the asset matches the rule
            if not comparator_func(asset_value, value):
                match = False
                break
            logger.debug(f"is match: {match}")
        return match

    def match_asset_to_stigs(self, asset: Asset, ssp_id: int) -> List[Component]:
        """
        Match asset to stig based on rules.
        :param Asset asset: An asset
        :param int ssp_id: The security plan ID
        :return: A list of asset mappings
        :rtype: List[AssetMapping]
        """
        component_list = Component.get_all_by_parent(parent_module=SecurityPlan.get_module_slug(), parent_id=ssp_id)
        associated_stigs = []
        component_name_dict = {component.title: component for component in component_list}
        for rule in self.rules:
            stig_name = rule.get("stig")
            comparators = rule.get("comparators", [])
            if self.find_matching_stigs(asset, comparators):
                if stig_name in component_name_dict:
                    logger.debug(f"Stig Name: {stig_name}")
                    stig_comp = component_name_dict.get(stig_name)
                    associated_stigs.append(stig_comp)
                else:
                    logger.debug(f"Stig Name: {stig_name} not found in component list")
                for component in component_list:
                    if component.title == stig_name:
                        logger.debug(f"Component: {component}")
                        associated_stigs.append(component)
        return associated_stigs

    def map_associated_stigs_to_assets(self, asset: Asset, ssp_id: int) -> List[AssetMapping]:
        """
        Map associated stigs to assets based on rules.
        :param Asset asset: An asset
        :param int ssp_id: The security plan ID
        :return: A list of asset mappings
        :rtype: List[AssetMapping]
        """
        new_asset_mappings = []
        associated_stigs = self.match_asset_to_stigs(asset, ssp_id)
        if asset.name == "regml-container":
            logger.debug(f"{asset.name} Associated STIGs: {associated_stigs}")
        for component in associated_stigs:
            asset_mapping = AssetMapping(
                assetId=asset.id,
                componentId=component.id,
            ).get_or_create()
            new_asset_mappings.append(asset_mapping)
        if new_asset_mappings:
            logger.debug(f"Created/Updated {len(new_asset_mappings)} asset to stig mappings")
            return new_asset_mappings
        return []
