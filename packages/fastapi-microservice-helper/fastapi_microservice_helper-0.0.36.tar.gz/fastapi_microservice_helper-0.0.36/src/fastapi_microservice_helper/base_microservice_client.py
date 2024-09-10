import uuid
from dataclasses import dataclass
from datetime import datetime

import httpx
from fastapi import HTTPException
from pydantic import BaseModel, TypeAdapter
from pydantic.fields import FieldInfo
from typing_extensions import Any
from pydantic._internal._model_construction import ModelMetaclass
from types import GenericAlias, UnionType
from faker import Faker


@dataclass
class MicroserviceOption:
  is_json: bool = True
  headers: dict = None


@dataclass
class ReplaceMicroserviceConfig:
  url: str


class Normailization:
  @staticmethod
  def serialize_uuid_to_str(data: Any = None):
    if data is None:
      return None

    if isinstance(data, dict):
      return {key: Normailization.serialize_uuid_to_str(value) for key, value in data.items()}

    if isinstance(data, list):
      return [Normailization.serialize_uuid_to_str(item) for item in data]

    if isinstance(data, uuid.UUID):
      return str(data)

    return data

  @staticmethod
  def strftime(data):
    if isinstance(data, dict):
      return {key: Normailization.strftime(value) for key, value in data.items()}
    elif isinstance(data, list):
      return [Normailization.strftime(item) for item in data]
    elif isinstance(data, datetime):
      return datetime.strftime(data, '%Y-%m-%d %H:%M:%S')
    else:
      return data

  @staticmethod
  def dump_pydantic_model_value(data):
    if data is None:
      return None

    if isinstance(data, dict):
      return {key: Normailization.dump_pydantic_model_value(value) for key, value in data.items()}

    elif isinstance(data, list):
      return [Normailization.dump_pydantic_model_value(item) for item in data]

    if isinstance(data, BaseModel):
      return data.model_dump()

    return data

  @staticmethod
  def normalize(data: Any):
    data = Normailization.dump_pydantic_model_value(data)
    data = Normailization.serialize_uuid_to_str(data)
    return Normailization.strftime(data)

class BaseMicroserviceClient:
  def filter_none_values(self, query_params: dict | None):
    return {key: value for key, value in query_params.items() if value is not None} if query_params else None

  async def send(
    self, url: str, query_params: dict, body_params: any, response_type: any, option: MicroserviceOption = None
  ):
    if not ReplaceMicroserviceConfig.url:
      raise Exception('Please config microservice url')

    url = ReplaceMicroserviceConfig.url + url
    if not option:
      option = MicroserviceOption()

    async with httpx.AsyncClient() as client:
      response = await client.post(
        url=url,
        headers=option.headers,
        params=self.filter_none_values(query_params),
        data=body_params if not option.is_json else None,
        json=Normailization.normalize(body_params) if option.is_json else None,
      )
      data = response.json()
      if response.status_code < 200 or response.status_code > 299:
        raise HTTPException(status_code=response.status_code, detail=data)
      if not response_type:
        return data

      return TypeAdapter(response_type).validate_python(data)
class MockHelper:
  @staticmethod
  def sample(response_class: Any):
    if response_class is None:
      return

    mock_data = {}
    if type(response_class) is ModelMetaclass:
      for key in response_class.__fields__.keys():
        property = response_class.__fields__[key]
        examples = property.examples
        mock_data[key] = examples or MockHelper.gen_mock_data(property)
    elif type(response_class) is GenericAlias:
      return MockHelper.gen_mock_generic_type(response_class)
    else:
      raise Exception(f"Need to implement this type {type(response_class)}")

    return TypeAdapter(response_class).validate_python(mock_data)

  @staticmethod
  def gen_mock_data(property: FieldInfo):
    if type(property.annotation) is UnionType:
      return MockHelper.gen_mock_union_type(property.annotation)
    elif isinstance(property.annotation, GenericAlias):
      return MockHelper.gen_mock_generic_type(property.annotation)

    return MockHelper.gen_mock_by_normal_type(property.annotation)


  @staticmethod
  def gen_mock_by_normal_type(type_data: Any):
    faker = Faker()
    if type(type_data) is ModelMetaclass:
      return MockHelper.sample(type_data)
    type_name = type_data.__name__
    match type_name:
      case 'UUID':
        return faker.uuid4()
      case 'str':
        return faker.pystr()
      case 'int':
        return faker.pyint()
      case 'bool':
        return False
      case 'datetime':
        return faker.date()
      case _:
        raise Exception(f'Type {type_name} not implemented')

  @staticmethod
  def gen_mock_generic_type(ref_type: type(GenericAlias)):
    if ref_type.__name__ == 'list':
      return [MockHelper.gen_mock_by_normal_type(ref_type.__args__[0])]
    raise Exception(f'Type {ref_type.__name__} not implemented')

  @staticmethod
  def gen_mock_union_type(ref_type: type(UnionType)):
    first_type = ref_type.__args__[0]
    if isinstance(first_type, GenericAlias):
      return MockHelper.gen_mock_generic_type(first_type)
    return MockHelper.gen_mock_by_normal_type(first_type)
