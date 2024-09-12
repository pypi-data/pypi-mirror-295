"""
Testing e2clab.schemas modules
"""

import jsonschema
import jsonschema.exceptions

import e2clab.schemas as e2cschema
import e2clab.schemas.layers_services_schema as lyr_svc_schema
from e2clab.constants import ConfFiles, Environment
from e2clab.constants.layers_services import (
    CLUSTER,
    IPV,
    PROVENANCE_SVC_DATAFLOW_SPEC,
    PROVENANCE_SVC_PARALLELISM,
    PROVENANCE_SVC_PROVIDER,
    SERVERS,
)
from e2clab.tests.unit import TestE2cLab
from e2clab.utils import load_yaml_file


class TestSchema(TestE2cLab):
    """
    Testing utils functions on valid configuration files
    """

    def test_is_valid_conf(self):
        netconf = load_yaml_file(self.test_folder / ConfFiles.NETWORK)
        invalid_netconf = load_yaml_file(self.test_folder / "invalid_network.yaml")
        # Test correct configuration
        self.assertTrue(e2cschema.is_valid_conf(netconf, "network"))
        # Test an invalid netconf
        self.assertFalse(e2cschema.is_valid_conf(invalid_netconf, "network"))
        # Test an invalid "conference type input"
        self.assertFalse(e2cschema.is_valid_conf(netconf, "not_a_conf_type"))
        # Test an incorrect configuration match
        self.assertFalse(e2cschema.is_valid_conf(netconf, "workflow"))

    def test_network_schema(self):
        netconf = load_yaml_file(self.test_folder / ConfFiles.NETWORK)
        invalid_netconf = load_yaml_file(self.test_folder / "invalid_network.yaml")
        # Test correct configuration
        try:
            result = e2cschema.is_valid_conf(netconf, "network")
        except jsonschema.exceptions.SchemaError as e:
            self.fail(f"Invalid schema definition : {e}")
        self.assertTrue(result)
        self.assertFalse(e2cschema.is_valid_conf(invalid_netconf, "network"))

    def test_workflow_schema(self):
        workconf = load_yaml_file(self.test_folder / ConfFiles.WORKFLOW)
        invalid_workconf = load_yaml_file(self.test_folder / "invalid_workflow.yaml")
        try:
            result = e2cschema.is_valid_conf(workconf, "workflow")
        except jsonschema.exceptions.SchemaError as e:
            self.fail(f"Invalid schema definition : {e}")
        self.assertTrue(result)
        self.assertFalse(e2cschema.is_valid_conf(invalid_workconf, "workflow"))

    def test_layers_services_schema(self):
        layersconf = load_yaml_file(self.test_folder / ConfFiles.LAYERS_SERVICES)
        invalid_kayersconf = load_yaml_file(
            self.test_folder / "invalid_layers_services.yaml"
        )
        try:
            result = e2cschema.is_valid_conf(layersconf, "layers_services")
        except jsonschema.exceptions.SchemaError as e:
            self.fail(f"Invalid schema definition : {e}")
        self.assertTrue(result)
        self.assertFalse(e2cschema.is_valid_conf(invalid_kayersconf, "layers_services"))


class TestLayersServicesSchema(TestE2cLab):
    """
    Testing layers services schema
    """

    def test_walltime_schema(self):
        validator = jsonschema.Draft7Validator(lyr_svc_schema.walltime_schema)

        invalid_values = [
            1,
            True,
            "59:59:23",
            "59:59:23",
            "24:00:00",
            "00:60:00",
            "00:00:60",
            "23 59 59",
            "23-59-59",
        ]
        for v in invalid_values:
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                validator.validate(v)

        validator.validate("00:00:00")
        validator.validate("23:59:59")

    # TODO: Add more detailed testing


class TestProvenanceShema(TestE2cLab):
    """
    Testing provenance schema
    """

    validator = jsonschema.Draft7Validator(lyr_svc_schema.provenance_svc_schema)

    def test_invalid_data(self):

        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.validator.validate({"test": "test"})

    def test_valid_data(self):
        data = {
            PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
            CLUSTER: "paravance",
            PROVENANCE_SVC_DATAFLOW_SPEC: "test",
            IPV: 4,
            PROVENANCE_SVC_PARALLELISM: 1,
        }
        self.validator.validate(data)

        data = {
            PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
            CLUSTER: "paravance",
            PROVENANCE_SVC_DATAFLOW_SPEC: "test",
        }
        self.validator.validate(data)

        data = {
            PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
            SERVERS: ["paravance-5.rennes.grid5000.fr"],
            PROVENANCE_SVC_DATAFLOW_SPEC: "test",
        }
        self.validator.validate(data)

    def test_no_cluster_or_server(self):

        data = {
            PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
            PROVENANCE_SVC_DATAFLOW_SPEC: "test",
        }

        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.validator.validate(data)

    def test_too_many_servers(self):

        data = {
            PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
            SERVERS: ["paravance-5.rennes.grid5000.fr", "TEST"],
            PROVENANCE_SVC_DATAFLOW_SPEC: "test",
        }

        with self.assertRaises(jsonschema.exceptions.ValidationError):
            self.validator.validate(data)
