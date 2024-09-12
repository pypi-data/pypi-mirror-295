from __future__ import annotations

from functools import partial
from secrets import randbelow, token_hex
from unittest import TestCase

import jsonrpc.openrpc as openrpc

string: partial[str] = partial(token_hex, 8)
number: partial[int] = partial(randbelow, 1000)


class TestContact(TestCase):
    def setUp(self) -> None:
        self.contact: openrpc.Contact = openrpc.Contact()

    def test_name(self) -> None:
        self.assertNotIn("name", self.contact.json)

        self.contact.name = string()
        self.assertEqual(self.contact.json["name"], self.contact.name)

    def test_url(self) -> None:
        self.assertNotIn("url", self.contact.json)

        self.contact.url = string()
        self.assertEqual(self.contact.json["url"], self.contact.url)

    def test_email(self) -> None:
        self.assertNotIn("email", self.contact.json)

        self.contact.email = string()
        self.assertEqual(self.contact.json["email"], self.contact.email)


class TestLicense(TestCase):
    def setUp(self) -> None:
        self.license: openrpc.License = openrpc.License(name=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.license.json["name"], self.license.name)

    def test_url(self) -> None:
        self.assertNotIn("url", self.license.json)

        self.license.url = string()
        self.assertEqual(self.license.json["url"], self.license.url)


class TestInfo(TestCase):
    def setUp(self) -> None:
        self.info: openrpc.Info = openrpc.Info(title=string(), version=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.info.json["title"], self.info.title)
        self.assertEqual(self.info.json["version"], self.info.version)

    def test_description(self) -> None:
        self.assertNotIn("description", self.info.json)

        self.info.description = string()
        self.assertEqual(self.info.json["description"], self.info.description)

    def test_terms_of_service(self) -> None:
        self.assertNotIn("termsOfService", self.info.json)

        self.info.terms_of_service = string()
        self.assertEqual(self.info.json["termsOfService"], self.info.terms_of_service)

    def test_contact(self) -> None:
        self.assertNotIn("contact", self.info.json)

        self.info.contact = openrpc.Contact(name=string())
        self.assertEqual(self.info.json["contact"], self.info.contact.json)

    def test_license(self) -> None:
        self.assertNotIn("license", self.info.json)

        self.info.license = openrpc.License(name=string())
        self.assertEqual(self.info.json["license"], self.info.license.json)


class TestServerVariable(TestCase):
    def setUp(self) -> None:
        self.server_variable: openrpc.ServerVariable = openrpc.ServerVariable(default=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.server_variable.json["default"], self.server_variable.default)

    def test_enum(self) -> None:
        self.assertNotIn("enum", self.server_variable.json)

        self.server_variable.enum.extend(string() for _ in range(3))
        self.assertCountEqual(self.server_variable.json["enum"], self.server_variable.enum)

    def test_description(self) -> None:
        self.assertNotIn("description", self.server_variable.json)

        self.server_variable.description = string()
        self.assertEqual(self.server_variable.json["description"], self.server_variable.description)


class TestServer(TestCase):
    def setUp(self) -> None:
        self.server: openrpc.Server = openrpc.Server(name=string(), url=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.server.json["name"], self.server.name)
        self.assertEqual(self.server.json["url"], self.server.url)

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.server.json)

        self.server.summary = string()
        self.assertEqual(self.server.json["summary"], self.server.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.server.json)

        self.server.description = string()
        self.assertEqual(self.server.json["description"], self.server.description)

    def test_variables(self) -> None:
        self.assertNotIn("variables", self.server.json)

        self.server.variables |= {string(): openrpc.ServerVariable(default=string())}
        self.assertDictEqual(self.server.json["variables"], {key: value.json for key, value in self.server.variables.items()})


class TestExternalDocumentation(TestCase):
    def setUp(self) -> None:
        self.external_docs: openrpc.ExternalDocumentation = openrpc.ExternalDocumentation(url=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.external_docs.json["url"], self.external_docs.url)

    def test_description(self) -> None:
        self.assertNotIn("description", self.external_docs.json)

        self.external_docs.description = string()
        self.assertEqual(self.external_docs.json["description"], self.external_docs.description)


class TestTag(TestCase):
    def setUp(self) -> None:
        self.tag: openrpc.Tag = openrpc.Tag(name=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.tag.json["name"], self.tag.name)

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.tag.json)

        self.tag.summary = string()
        self.assertEqual(self.tag.json["summary"], self.tag.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.tag.json)

        self.tag.description = string()
        self.assertEqual(self.tag.json["description"], self.tag.description)

    def test_external_docs(self) -> None:
        self.assertNotIn("externalDocs", self.tag.json)

        self.tag.external_docs = openrpc.ExternalDocumentation(url=string())
        self.assertDictEqual(self.tag.json["externalDocs"], self.tag.external_docs.json)


class TestContentDescriptor(TestCase):
    def setUp(self) -> None:
        self.content_descriptor: openrpc.ContentDescriptor = openrpc.ContentDescriptor(name=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.content_descriptor.json["name"], self.content_descriptor.name)
        self.assertDictEqual(self.content_descriptor.json["schema"], {})

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.content_descriptor.json)

        self.content_descriptor.summary = string()
        self.assertEqual(self.content_descriptor.json["summary"], self.content_descriptor.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.content_descriptor.json)

        self.content_descriptor.description = string()
        self.assertEqual(self.content_descriptor.json["description"], self.content_descriptor.description)

    def test_required(self) -> None:
        self.assertFalse(self.content_descriptor.json["required"])

        self.content_descriptor.required = True
        self.assertTrue(self.content_descriptor.json["required"])

    def test_deprecated(self) -> None:
        self.assertFalse(self.content_descriptor.json["deprecated"])

        self.content_descriptor.deprecated = True
        self.assertTrue(self.content_descriptor.json["deprecated"])


class TestError(TestCase):
    def setUp(self) -> None:
        self.error: openrpc.Error = openrpc.Error(code=number(), message=string())  # noqa: S311

    def test_required_fields(self) -> None:
        self.assertEqual(self.error.json["code"], self.error.code)
        self.assertEqual(self.error.json["message"], self.error.message)

    def test_data(self) -> None:
        self.assertNotIn("data", self.error.json)

        self.error.data = string()
        self.assertEqual(self.error.json["data"], self.error.data)


class TestLink(TestCase):
    def setUp(self) -> None:
        self.link: openrpc.Link = openrpc.Link(name=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.link.json["name"], self.link.name)

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.link.json)

        self.link.summary = string()
        self.assertEqual(self.link.json["summary"], self.link.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.link.json)

        self.link.description = string()
        self.assertEqual(self.link.json["description"], self.link.description)

    def test_method(self) -> None:
        self.assertNotIn("method", self.link.json)

        self.link.method = string()
        self.assertEqual(self.link.json["method"], self.link.method)

    def test_params(self) -> None:
        self.assertDictEqual(self.link.json["params"], {})

        self.link.params |= {string(): None}
        self.assertDictEqual(self.link.json["params"], self.link.params)

    def test_server(self) -> None:
        self.assertNotIn("server", self.link.json)

        self.link.server = openrpc.Server(name=string(), url=string())
        self.assertDictEqual(self.link.json["server"], self.link.server.json)


class TestExample(TestCase):
    def setUp(self) -> None:
        self.example: openrpc.Example = openrpc.Example()

    def test_mutually_exclusive_fields(self) -> None:
        with self.assertRaises(TypeError) as context:
            openrpc.Example(value=string(), external_value=string())

        self.assertEqual(str(context.exception), "The 'value' field and 'external_value' field are mutually exclusive")

    def test_name(self) -> None:
        self.assertNotIn("name", self.example.json)

        self.example.name = string()
        self.assertEqual(self.example.json["name"], self.example.name)

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.example.json)

        self.example.summary = string()
        self.assertEqual(self.example.json["summary"], self.example.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.example.json)

        self.example.description = string()
        self.assertEqual(self.example.json["description"], self.example.description)

    def test_value(self) -> None:
        self.assertNotIn("value", self.example.json)

        self.example.value = string()
        self.assertEqual(self.example.json["value"], self.example.value)

    def test_external_value(self) -> None:
        self.assertNotIn("externalValue", self.example.json)

        self.example.external_value = string()
        self.assertEqual(self.example.json["externalValue"], self.example.external_value)


class TestExamplePairing(TestCase):
    def setUp(self) -> None:
        self.example_pairing: openrpc.ExamplePairing = openrpc.ExamplePairing(name=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.example_pairing.json["name"], self.example_pairing.name)
        self.assertListEqual(self.example_pairing.json["params"], [])

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.example_pairing.json)

        self.example_pairing.summary = string()
        self.assertEqual(self.example_pairing.json["summary"], self.example_pairing.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.example_pairing.json)

        self.example_pairing.description = string()
        self.assertEqual(self.example_pairing.json["description"], self.example_pairing.description)

    def test_params(self) -> None:
        self.assertListEqual(self.example_pairing.json["params"], [])

        self.example_pairing.params.extend(openrpc.Example(name=string()) for _ in range(3))
        self.assertCountEqual(self.example_pairing.json["params"], [value.json for value in self.example_pairing.params])

    def test_result(self) -> None:
        self.assertNotIn("result", self.example_pairing.json)

        self.example_pairing.result = openrpc.Example(name=string())
        self.assertEqual(self.example_pairing.json["result"], self.example_pairing.result.json)


class TestMethod(TestCase):
    def setUp(self) -> None:
        self.method: openrpc.Method = openrpc.Method(name=string())

    def test_required_fields(self) -> None:
        self.assertEqual(self.method.json["name"], self.method.name)
        self.assertListEqual(self.method.json["params"], [])

    def test_tags(self) -> None:
        self.assertNotIn("tags", self.method.json)

        self.method.tags.extend(openrpc.Tag(name=string()) for _ in range(3))
        self.assertCountEqual(self.method.json["tags"], [value.json for value in self.method.tags])

    def test_summary(self) -> None:
        self.assertNotIn("summary", self.method.json)

        self.method.summary = string()
        self.assertEqual(self.method.json["summary"], self.method.summary)

    def test_description(self) -> None:
        self.assertNotIn("description", self.method.json)

        self.method.description = string()
        self.assertEqual(self.method.json["description"], self.method.description)

    def test_external_docs(self) -> None:
        self.assertNotIn("externalDocs", self.method.json)

        self.method.external_docs = openrpc.ExternalDocumentation(url=string())
        self.assertDictEqual(self.method.json["externalDocs"], self.method.external_docs.json)

    def test_params(self) -> None:
        self.assertListEqual(self.method.json["params"], [])

        self.method.params.extend(openrpc.ContentDescriptor(name=string()) for _ in range(3))
        self.assertCountEqual(self.method.json["params"], [value.json for value in self.method.params])

    def test_result(self) -> None:
        self.assertNotIn("result", self.method.json)

        self.method.result = openrpc.ContentDescriptor(name=string())
        self.assertDictEqual(self.method.json["result"], self.method.result.json)

    def test_deprecated(self) -> None:
        self.assertFalse(self.method.json["deprecated"])

        self.method.deprecated = True
        self.assertTrue(self.method.json["deprecated"])

    def test_servers(self) -> None:
        self.assertNotIn("servers", self.method.json)

        self.method.servers.extend(openrpc.Server(name=string(), url=string()) for _ in range(3))
        self.assertCountEqual(self.method.json["servers"], [value.json for value in self.method.servers])

    def test_errors(self) -> None:
        self.assertNotIn("errors", self.method.json)

        self.method.errors.extend(openrpc.Error(code=number(), message=string()) for _ in range(3))  # noqa: S311
        self.assertCountEqual(self.method.json["errors"], [value.json for value in self.method.errors])

    def test_links(self) -> None:
        self.assertNotIn("links", self.method.json)

        self.method.links.extend(openrpc.Link(name=string()) for _ in range(3))
        self.assertCountEqual(self.method.json["links"], [value.json for value in self.method.links])

    def test_param_structure(self) -> None:
        self.assertEqual(self.method.json["paramStructure"], openrpc.ParamStructure.EITHER)

        for param_structure in openrpc.ParamStructure:
            with self.subTest(param_structure=param_structure):
                self.method.param_structure = param_structure
                self.assertEqual(self.method.json["paramStructure"], param_structure)

    def test_examples(self) -> None:
        self.assertNotIn("examples", self.method.json)

        self.method.examples.extend(openrpc.ExamplePairing(name=string()) for _ in range(3))
        self.assertCountEqual(self.method.json["examples"], [value.json for value in self.method.examples])


class TestComponents(TestCase):
    def setUp(self) -> None:
        self.components: openrpc.Components = openrpc.Components()

    def test_content_descriptors(self) -> None:
        self.assertDictEqual(self.components.json["contentDescriptors"], {})

        self.components.content_descriptors |= {string(): openrpc.ContentDescriptor(name=string())}
        self.assertDictEqual(
            self.components.json["contentDescriptors"],
            {key: value.json for key, value in self.components.content_descriptors.items()},
        )

    def test_schemas(self) -> None:
        self.assertDictEqual(self.components.json["schemas"], {})

        self.components.schemas |= {string(): {"type": "string"}}
        self.assertDictEqual(self.components.json["schemas"], self.components.schemas)

    def test_examples(self) -> None:
        self.assertDictEqual(self.components.json["examples"], {})

        self.components.examples |= {string(): openrpc.Example(name=string())}
        self.assertDictEqual(
            self.components.json["examples"],
            {key: value.json for key, value in self.components.examples.items()},
        )

    def test_links(self) -> None:
        self.assertDictEqual(self.components.json["links"], {})

        self.components.links |= {string(): openrpc.Link(name=string())}
        self.assertDictEqual(
            self.components.json["links"],
            {key: value.json for key, value in self.components.links.items()},
        )

    def test_errors(self) -> None:
        self.assertDictEqual(self.components.json["errors"], {})

        self.components.errors |= {string(): openrpc.Error(code=number(), message=string())}
        self.assertDictEqual(
            self.components.json["errors"],
            {key: value.json for key, value in self.components.errors.items()},
        )

    def test_example_pairing_objects(self) -> None:
        self.assertDictEqual(self.components.json["examplePairingObjects"], {})

        self.components.example_pairing_objects |= {string(): openrpc.ExamplePairing(name=string())}
        self.assertDictEqual(
            self.components.json["examplePairingObjects"],
            {key: value.json for key, value in self.components.example_pairing_objects.items()},
        )

    def test_tags(self) -> None:
        self.assertDictEqual(self.components.json["tags"], {})

        self.components.tags |= {string(): openrpc.Tag(name=string())}
        self.assertDictEqual(
            self.components.json["tags"],
            {key: value.json for key, value in self.components.tags.items()},
        )


class TestOpenRPC(TestCase):
    def setUp(self) -> None:
        self.openrpc: openrpc.OpenRPC = openrpc.OpenRPC(info=openrpc.Info(title=string(), version=string()))

    def test_required_fields(self) -> None:
        self.assertEqual(self.openrpc.json["openrpc"], openrpc.VERSION)
        self.assertDictEqual(self.openrpc.json["info"], self.openrpc.info.json)
        self.assertListEqual(self.openrpc.json["methods"], [])

    def test_servers(self) -> None:
        self.assertNotIn("servers", self.openrpc.json)

        self.openrpc.servers.extend(openrpc.Server(name=string(), url=string()) for _ in range(3))
        self.assertCountEqual(self.openrpc.json["servers"], [value.json for value in self.openrpc.servers])

    def test_methods(self) -> None:
        self.assertListEqual(self.openrpc.json["methods"], [])

        self.openrpc.methods.extend(openrpc.Method(name=string()) for _ in range(3))
        self.assertCountEqual(self.openrpc.json["methods"], [value.json for value in self.openrpc.methods])

    def test_components(self) -> None:
        self.assertNotIn("components", self.openrpc.json)

        self.openrpc.components = openrpc.Components()
        self.assertDictEqual(self.openrpc.json["components"], self.openrpc.components.json)

    def test_external_docs(self) -> None:
        self.assertNotIn("externalDocs", self.openrpc.json)

        self.openrpc.external_docs = openrpc.ExternalDocumentation(url=string())
        self.assertDictEqual(self.openrpc.json["externalDocs"], self.openrpc.external_docs.json)
