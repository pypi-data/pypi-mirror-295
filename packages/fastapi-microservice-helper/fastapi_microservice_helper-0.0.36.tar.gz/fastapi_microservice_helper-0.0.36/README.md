# FastAPI Microservice Helper

## Introduction
FastAPI Microservice Helper is an SDK designed to facilitate communication between microservices over HTTP.
- It automatically generates the necessary code to build services and can be installed in client applications.
- It automatically mocks the response from the server if you're writing e2e tests.

## How to use

Let's say we have a CoreMicroservice that handles creating and retrieving posts.
Now, we want to call this CoreMicroservice from a UserMicroservice.

### Step 1: Define Microservice Actions on the Server

In the CoreMicroservice, you define actions for handling posts. Here's an example:

```python
# http/microservices/post.py
from uuid import UUID

from fastapi import Depends, Query
from fastapi_microservice_helper import action, microservice
from fastapi_request_helper.decorators.http_method import response, tag

from posts.http.responses.general_post_response import GeneralPostResponse
from posts.services.post import PostService

class GeneralPostResponse(BaseModel):
  id: UUID
  author_id: UUID

class CreatePostDto(BaseDto):
  author_id: UUID

@microservice()
@tag('Microservices Post')
class PostMicroservice:
  def __init__(self, post_service: PostService = Depends()):
    self.post_service = post_service

  @action()
  @response(GeneralPostResponse)
  async def get_post(self, post_id: UUID):
    return await self.post_service.find_general_post_by_id(post_id)

  @action()
  async def create_post(self, dto: CreatePostDto):
    await self.post_service.increment_post_likes(dto)
```

In this example, we define two actions for PostMicroservice:

get_post to retrieve a post by ID
create_post to create a new post.

### Step 2: Step 2: SDK Generation

FastAPI Microservice Helper automatically generates the SDK code based on the server definitions.
Here’s an example of what the generated client SDK might look like:

```python
# sdk/src/core_microservice/sdk.py
...

class BaseMicroserviceClient:
  def filter_none_values(self, query_params: dict | None):
    return {key: value for key, value in query_params.items() if value is not None} if query_params else None

  async def send(
    self, url: str, query_params: dict, body_params: any, response_type: any, option: MicroserviceOption = None
  ):
    if not CoreMicroserviceConfig.url:
      raise Exception('Please config microservice url')

    url = CoreMicroserviceConfig.url + url
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

class PostMicroservice(BaseMicroserviceClient):
    async def decrement_post_likes(self, dto: DecrementPostLikesDto , option: MicroserviceOption = None) -> None:
        return await self.send('/microservices/PostMicroservice/decrement_post_likes', None, dto, None, option )
    
    async def get_post(self, post_id: UUID , option: MicroserviceOption = None) -> GeneralPostResponse:
        return await self.send('/microservices/PostMicroservice/get_post', {'post_id': post_id}, None, GeneralPostResponse, option)

    async def create_post(self, dto: CreatePostDto , option: MicroserviceOption = None) -> None:
        return await self.send('/microservices/PostMicroservice/create_post', None, dto, None, option)
```

### Step 3: Build and Publish the SDK

Increase the *version* in `sdk.toml` file then build and publish it, for example, publish the sdk as `core-microservice==0.0.1`.

### Step 4: Configure the Microservice in the Client

#### Install the SDK

Add the SDK to your project’s dependencies in requirements.txt:

```python
# requirements.txt
core-microservice==0.0.1
```

Then install the required packages:

```bash
pip install -r requirements.txt
```
#### Configure the Microservice URL
Set the base URL for the CoreMicroservice:

```python
# config/microservice.py
from core_microservice import CoreMicroserviceConfig
CoreMicroserviceConfig.url = 'http://127.0.0.1:8000'
```

### Step 5: Use the Microservice in Client Code

In the UserMicroservice, you can now use the SDK to call actions from CoreMicroservice:

```python
# services/user.py
class UserService:
    def __init__(self, post_microservice: PostMicroservice = Depends()):
        self.post_microservice = post_microservice

    async def create_post(self, dto: CreatePostDto):
        await self.post_microservice.create_post(dto)

    async def get_post(self, post_id: UUID):
        return await self.post_microservice.get_post(post_id)
```
