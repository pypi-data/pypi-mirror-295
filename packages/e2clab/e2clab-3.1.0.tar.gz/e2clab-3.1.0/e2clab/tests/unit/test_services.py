from unittest.mock import patch

from enoslib import Host, Roles
from enoslib.api import CommandResult, Results

import e2clab.services as e2cserv
from e2clab.constants.layers_services import (
    ENV,
    ID,
    LAYER_ID,
    LAYER_NAME,
    NAME,
    QUANTITY,
    SERVICE_ID,
)
from e2clab.constants.workflow import SELF_PREFIX
from e2clab.services.errors import E2clabServiceImportError
from e2clab.services.plugins.Default import Default
from e2clab.tests.unit import TestE2cLab


class TestServices(TestE2cLab):

    def test_get_available_services(self):
        available_services = e2cserv.get_available_services()
        self.assertIn("Default", available_services)

    def test_load_services(self):
        services_to_load = ["Default"]
        loaded_services = e2cserv.load_services(services_to_load)
        self.assertIn("Default", loaded_services.keys())
        default_service = loaded_services["Default"](
            hosts={},
            service_metadata={
                NAME: "Producer",
                ID: "1_1",
                QUANTITY: 1,
                ENV: {"number": 34},
                LAYER_NAME: "Cloud",
                LAYER_ID: 1,
                SERVICE_ID: 1,
            },
        )
        self.assertIsInstance(default_service, e2cserv.Service)

        with self.assertRaises(E2clabServiceImportError):
            e2cserv.load_services(["notaservice"])

    def test_service_key(self):
        serv = Default(
            hosts=[Host("127.0.0.1")],
            service_metadata={
                NAME: "Producer",
                ID: "1_1",
                QUANTITY: 1,
                ENV: {"number": 34},
                LAYER_NAME: "Cloud",
                LAYER_ID: 1,
                SERVICE_ID: 1,
            },
        )
        service_key = serv._service_key(machine_id=1, sub_service_name="test")
        self.assertEqual(service_key, "cloud.producer.1.test.1")

    def test_get_hosts_from_roles(self):
        host1 = Host("127.0.0.1")
        host2 = Host("127.0.0.2", extra={"gateway": "test"})
        host3 = Host("127.0.0.3")
        serv = Default(
            hosts=[host1, host2, host3],
            service_metadata={
                NAME: "Producer",
                ID: "1_1",
                QUANTITY: 1,
                ENV: {"number": 34},
                LAYER_NAME: "Cloud",
                LAYER_ID: 1,
                SERVICE_ID: 1,
            },
        )
        iterable_hosts = serv._get_hosts_from_roles(
            roles=Roles({"A": [host1], "B": [host2, host3]})
        )
        # for host in iterable_hosts:
        self.assertCountEqual(iterable_hosts, [host1, host2, host3])
        self.assertEqual(iterable_hosts[0], host1)
        self.assertEqual(iterable_hosts[1], host2)
        self.assertEqual(iterable_hosts[2], host3)

        iterable_hosts = serv._get_hosts_from_roles(roles=Roles({"A": [host1, host2]}))
        self.assertEqual(iterable_hosts[0], host1)
        self.assertEqual(iterable_hosts[1], host2)

    def test_register_service(self):
        host1 = Host("1.1.1.1", extra={"gateway": "127.0.0.0"})
        host2 = Host("9.9.9.9", extra={"gateway": "127.0.0.0"})
        serv = Default(
            hosts=[
                host1,
                host2,
            ],
            service_metadata={
                NAME: "Producer",
                ID: "1_1",
                QUANTITY: 1,
                ENV: {"number": 34},
                LAYER_NAME: "Cloud",
                LAYER_ID: 1,
                SERVICE_ID: 1,
            },
        )
        extra = [{"version": 3}, {"version": 1}]

        with patch.object(
            serv, "_Service__get_host_ip", return_value="1.2.3.4"
        ) as patch_ip:
            extra_info, roles = serv.register_service(extra=extra)
            patch_ip.assert_called_with(host2, 4)

        service_key_1 = "cloud.producer.1.1"
        service_key_2 = "cloud.producer.1.2"
        self.assertIn(service_key_1, extra_info.keys())
        self.assertIn(service_key_2, extra_info.keys())

        serv_info_1 = extra_info[service_key_1]
        serv_info_2 = extra_info[service_key_2]

        self.assertEqual(roles[service_key_1][0], host1)
        self.assertEqual(len(roles[service_key_1]), 1)
        self.assertEqual(roles[service_key_2][0], host2)
        self.assertEqual(len(roles[service_key_2]), 1)

        self.assertEqual(serv_info_1, host1.extra["_self"])
        self.assertEqual(serv_info_2, host2.extra["_self"])

        self.assertAlmostEqual(serv_info_1["_id"], "1_1_1")
        self.assertAlmostEqual(serv_info_1["__address6__"], "1.2.3.4")
        self.assertAlmostEqual(serv_info_1["__address4__"], "1.2.3.4")
        self.assertAlmostEqual(serv_info_1["gateway"], "127.0.0.0")
        self.assertAlmostEqual(serv_info_1["version"], 3)

        self.assertAlmostEqual(serv_info_2["_id"], "1_1_2")
        self.assertAlmostEqual(serv_info_2["__address6__"], "1.2.3.4")
        self.assertAlmostEqual(serv_info_2["__address4__"], "1.2.3.4")
        self.assertAlmostEqual(serv_info_2["gateway"], "127.0.0.0")
        self.assertAlmostEqual(serv_info_2["version"], 1)

    def test_register_subservice(self):
        host1 = Host("1.1.1.1", extra={"gateway": "127.0.0.0"})
        host2 = Host("9.9.9.9", extra={"gateway": "127.0.0.0"})
        host3 = Host("8.8.8.8", extra={"gateway": "127.0.0.0"})
        serv = Default(
            hosts=[
                host1,
                host2,
                host3,
            ],
            service_metadata={
                NAME: "Producer",
                ID: "1_1",
                QUANTITY: 1,
                ENV: {"number": 34},
                LAYER_NAME: "Cloud",
                LAYER_ID: 1,
                SERVICE_ID: 1,
            },
        )
        extra = [{"version": 3}, {"version": 1}]

        test_roles = Roles({"A": [host1, host3], "B": [host2]})

        # With hosts supplied
        with patch.object(serv, "_Service__get_host_ip", return_value="1.2.3.4"):
            extra_info, roles = serv.register_service(
                hosts=test_roles["A"],
                sub_service="cctv_producer",
                service_port="8888",
                extra=extra,
            )

        service_key_1 = "cloud.producer.1.cctv_producer.1"
        service_key_2 = "cloud.producer.1.cctv_producer.2"

        # Checking correctly created roles, info and hosts
        self.assertIn(service_key_1, extra_info.keys())
        self.assertIn(service_key_2, extra_info.keys())

        self.assertEqual(len(roles[service_key_1]), 1)
        self.assertEqual(len(roles[service_key_2]), 1)

        subserv_host1 = roles[service_key_1][0]
        subserv_host2 = roles[service_key_2][0]

        self.assertEqual(extra_info[service_key_1], subserv_host1.extra["_self"])
        self.assertEqual(extra_info[service_key_2], subserv_host2.extra["_self"])

        self.assertEqual(subserv_host1.extra["_self"]["version"], 3)
        self.assertEqual(subserv_host2.extra["_self"]["version"], 1)

        # With roles supplied
        with patch.object(serv, "_Service__get_host_ip", return_value="1.2.3.4"):
            extra_info, roles = serv.register_service(
                roles=test_roles,
                sub_service="cctv_producer",
                service_port="8888",
                extra=extra,
            )

        service_key_1 = "cloud.producer.1.cctv_producer.1"
        service_key_2 = "cloud.producer.1.cctv_producer.2"

        # Checking correctly created roles, info and hosts
        self.assertIn(service_key_1, extra_info.keys())
        self.assertIn(service_key_2, extra_info.keys())

        self.assertEqual(len(roles[service_key_1]), 1)
        self.assertEqual(len(roles[service_key_2]), 1)

        subserv_host1 = roles[service_key_1][0]
        subserv_host2 = roles[service_key_2][0]

        self.assertEqual(extra_info[service_key_1], subserv_host1.extra["_self"])
        self.assertEqual(extra_info[service_key_2], subserv_host2.extra["_self"])

        self.assertEqual(subserv_host1.extra["_self"]["version"], 3)
        self.assertEqual(subserv_host2.extra["_self"]["version"], 1)

    def test_get_host_ip(self):
        host = Host("9.9.9.9")
        serv = Default(
            hosts=[
                host,
            ],
            service_metadata={
                NAME: "Producer",
                ID: "1_1",
                QUANTITY: 1,
                ENV: {"number": 34},
                LAYER_NAME: "Cloud",
                LAYER_ID: 1,
                SERVICE_ID: 1,
            },
        )

        with patch("enoslib.run") as run_patch:
            run_patch.return_value = Results(
                [
                    CommandResult(
                        host="host",
                        task="task",
                        status="OK",
                        payload={"stdout": "1.1.1.1/24"},
                    )
                ]
            )
            ip = serv._Service__get_host_ip(host=host, version=4)
            self.assertEqual(ip, "1.1.1.1")
            ip = serv._Service__get_host_ip(host=host, version=6)
            self.assertEqual(ip, "1.1.1.1")
            with self.assertRaises(AssertionError):
                ip = serv._Service__get_host_ip(host=host, version=3)

    def test_populate_self_extra(self):
        serv = Default(
            hosts=[
                Host("1.1.1.1", extra={"gateway": "127.0.0.0"}),
                Host("9.9.9.9", extra={"gateway": "127.0.0.0"}),
            ],
            service_metadata={
                NAME: "Producer",
                ID: "1_1",
                QUANTITY: 1,
                ENV: {"number": 34},
                LAYER_NAME: "Cloud",
                LAYER_ID: 1,
                SERVICE_ID: 1,
            },
        )

        serv.service_extra_info = {
            "service1": {"addr": "1.1.1.1"},
            "service2": {"addr": "9.9.9.9"},
        }
        serv._populate_self_extra(serv.hosts[0], "service1")
        serv._populate_self_extra(serv.hosts[1], "service2")

        self.assertIn("addr", serv.hosts[0].extra[SELF_PREFIX])
        self.assertIn("gateway", serv.hosts[0].extra[SELF_PREFIX])
        self.assertIn("addr", serv.hosts[1].extra[SELF_PREFIX])
        self.assertIn("gateway", serv.hosts[1].extra[SELF_PREFIX])

        self.assertEqual("1.1.1.1", serv.hosts[0].extra[SELF_PREFIX]["addr"])
        self.assertEqual("127.0.0.0", serv.hosts[0].extra[SELF_PREFIX]["gateway"])
        self.assertEqual("9.9.9.9", serv.hosts[1].extra[SELF_PREFIX]["addr"])
        self.assertEqual("127.0.0.0", serv.hosts[1].extra[SELF_PREFIX]["gateway"])


class TestDefaultService(TestE2cLab):

    def testDeploy(self):
        host1 = Host("1.1.1.1", extra={"gateway": "127.0.0.0"})
        host2 = Host("9.9.9.9", extra={"gateway": "127.0.0.0"})
        serv = Default(
            hosts=[
                host1,
                host2,
            ],
            service_metadata={
                NAME: "Producer",
                ID: "1_1",
                QUANTITY: 1,
                ENV: {"number": 34},
                LAYER_NAME: "Cloud",
                LAYER_ID: 1,
                SERVICE_ID: 1,
            },
        )
        with patch.object(serv, "_Service__get_host_ip", return_value="1.1.1.1"):
            extra_info, roles = serv.deploy()

        self.assertIn("cloud.producer.1.1", roles.keys())
        self.assertIn("cloud.producer.1.1", extra_info.keys())
        self.assertIn("_self", host1.extra.keys())
        self.assertIn("_self", host2.extra.keys())
