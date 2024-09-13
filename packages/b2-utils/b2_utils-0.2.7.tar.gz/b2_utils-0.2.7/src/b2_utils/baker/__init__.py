import random as _random

from model_bakery import baker

from b2_utils.faker import faker as _faker
from b2_utils.helpers import random_hex_color as _random_hex_color


def document_generator():
    return _random.choice([_faker.unique.cpf(), _faker.unique.cnpj()])  # noqa: S311


baker.generators.add("b2_utils.fields.CICharField", _faker.text)
baker.generators.add("b2_utils.fields.CIEmailField", _faker.unique.ascii_email)
baker.generators.add("b2_utils.fields.CIText", _faker.text)
baker.generators.add("b2_utils.fields.CnpjField", _faker.unique.cnpj)
baker.generators.add("b2_utils.fields.CpfField", _faker.unique.cpf)
baker.generators.add("b2_utils.fields.PISField", _faker.unique.pis)
baker.generators.add("b2_utils.fields.DocumentField", document_generator)
baker.generators.add("b2_utils.fields.HexColorField", _random_hex_color)
