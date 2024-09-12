from typing import Iterator, Optional, AsyncIterator, Tuple, Literal, List
from unlok_next.rath import UnlokRath
from unlok_next.funcs import aexecute, subscribe, execute, asubscribe
from pydantic import BaseModel, Field
from rath.scalars import ID
from enum import Enum


class StructureInput(BaseModel):
    object: ID
    identifier: str

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class DevelopmentClientInput(BaseModel):
    manifest: "ManifestInput"
    composition: Optional[ID] = None
    requirements: Tuple["Requirement", ...]

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class ManifestInput(BaseModel):
    identifier: str
    version: str
    logo: Optional[str] = None
    scopes: Tuple[str, ...]

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class Requirement(BaseModel):
    service: str
    optional: bool
    description: Optional[str] = None
    key: str

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class CreateStreamInput(BaseModel):
    room: ID
    title: Optional[str] = None
    agent_id: Optional[str] = Field(alias="agentId", default=None)

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class MessageAgentRoom(BaseModel):
    """Room(id, title, description, creator)"""

    typename: Optional[Literal["Room"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class MessageAgent(BaseModel):
    """Agent(id, room, name, app, user)"""

    typename: Optional[Literal["Agent"]] = Field(alias="__typename", exclude=True)
    id: ID
    room: MessageAgentRoom

    class Config:
        """A config class"""

        frozen = True


class Message(BaseModel):
    typename: Optional[Literal["Message"]] = Field(alias="__typename", exclude=True)
    id: ID
    text: str
    "A clear text representation of the rich comment"
    agent: MessageAgent
    "The user that created this comment"

    class Config:
        """A config class"""

        frozen = True


class ListMessageAgent(BaseModel):
    """Agent(id, room, name, app, user)"""

    typename: Optional[Literal["Agent"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class ListMessage(BaseModel):
    typename: Optional[Literal["Message"]] = Field(alias="__typename", exclude=True)
    id: ID
    text: str
    "A clear text representation of the rich comment"
    agent: ListMessageAgent
    "The user that created this comment"

    class Config:
        """A config class"""

        frozen = True


class StreamAgentRoom(BaseModel):
    """Room(id, title, description, creator)"""

    typename: Optional[Literal["Room"]] = Field(alias="__typename", exclude=True)
    id: ID

    class Config:
        """A config class"""

        frozen = True


class StreamAgent(BaseModel):
    """Agent(id, room, name, app, user)"""

    typename: Optional[Literal["Agent"]] = Field(alias="__typename", exclude=True)
    id: ID
    room: StreamAgentRoom

    class Config:
        """A config class"""

        frozen = True


class Stream(BaseModel):
    typename: Optional[Literal["Stream"]] = Field(alias="__typename", exclude=True)
    id: ID
    title: str
    "The Title of the Stream"
    token: str
    agent: StreamAgent
    "The agent that created this stream"

    class Config:
        """A config class"""

        frozen = True


class Room(BaseModel):
    typename: Optional[Literal["Room"]] = Field(alias="__typename", exclude=True)
    id: ID
    title: str
    "The Title of the Room"
    description: str

    class Config:
        """A config class"""

        frozen = True


class SendMutation(BaseModel):
    send: Message

    class Arguments(BaseModel):
        text: str
        room: ID
        agent_id: str = Field(alias="agentId")
        attach_structures: Optional[List[StructureInput]] = Field(
            alias="attachStructures", default=None
        )

    class Meta:
        document = "fragment Message on Message {\n  id\n  text\n  agent {\n    id\n    room {\n      id\n    }\n  }\n}\n\nmutation Send($text: String!, $room: ID!, $agentId: String!, $attachStructures: [StructureInput!]) {\n  send(\n    input: {text: $text, room: $room, agentId: $agentId, attachStructures: $attachStructures}\n  ) {\n    ...Message\n  }\n}"


class CreateClientMutation(BaseModel):
    create_developmental_client: str = Field(alias="createDevelopmentalClient")

    class Arguments(BaseModel):
        input: DevelopmentClientInput

    class Meta:
        document = "mutation CreateClient($input: DevelopmentClientInput!) {\n  createDevelopmentalClient(input: $input)\n}"


class CreateStreamMutation(BaseModel):
    create_stream: Stream = Field(alias="createStream")

    class Arguments(BaseModel):
        input: CreateStreamInput

    class Meta:
        document = "fragment Stream on Stream {\n  id\n  title\n  token\n  agent {\n    id\n    room {\n      id\n    }\n  }\n}\n\nmutation CreateStream($input: CreateStreamInput!) {\n  createStream(input: $input) {\n    ...Stream\n  }\n}"


class CreateRoomMutation(BaseModel):
    create_room: Room = Field(alias="createRoom")

    class Arguments(BaseModel):
        title: Optional[str] = Field(default=None)
        description: Optional[str] = Field(default=None)

    class Meta:
        document = "fragment Room on Room {\n  id\n  title\n  description\n}\n\nmutation CreateRoom($title: String, $description: String) {\n  createRoom(input: {title: $title, description: $description}) {\n    ...Room\n  }\n}"


class GetStreamQuery(BaseModel):
    stream: Stream

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Stream on Stream {\n  id\n  title\n  token\n  agent {\n    id\n    room {\n      id\n    }\n  }\n}\n\nquery GetStream($id: ID!) {\n  stream(id: $id) {\n    ...Stream\n  }\n}"


class GetRoomQuery(BaseModel):
    room: Room

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Room on Room {\n  id\n  title\n  description\n}\n\nquery GetRoom($id: ID!) {\n  room(id: $id) {\n    ...Room\n  }\n}"


class WatchRoomSubscriptionRoom(BaseModel):
    typename: Optional[Literal["RoomEvent"]] = Field(alias="__typename", exclude=True)
    message: Optional[ListMessage]

    class Config:
        """A config class"""

        frozen = True


class WatchRoomSubscription(BaseModel):
    room: WatchRoomSubscriptionRoom

    class Arguments(BaseModel):
        room: ID
        agent_id: ID = Field(alias="agentId")

    class Meta:
        document = "fragment ListMessage on Message {\n  id\n  text\n  agent {\n    id\n  }\n}\n\nsubscription WatchRoom($room: ID!, $agentId: ID!) {\n  room(room: $room, agentId: $agentId) {\n    message {\n      ...ListMessage\n    }\n  }\n}"


async def asend(
    text: str,
    room: ID,
    agent_id: str,
    attach_structures: Optional[List[StructureInput]] = None,
    rath: Optional[UnlokRath] = None,
) -> Message:
    """Send


     send: Message represent the message of an agent on a room


    Arguments:
        text (str): text
        room (ID): room
        agent_id (str): agentId
        attach_structures (Optional[List[StructureInput]], optional): attachStructures.
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Message"""
    return (
        await aexecute(
            SendMutation,
            {
                "text": text,
                "room": room,
                "agentId": agent_id,
                "attachStructures": attach_structures,
            },
            rath=rath,
        )
    ).send


def send(
    text: str,
    room: ID,
    agent_id: str,
    attach_structures: Optional[List[StructureInput]] = None,
    rath: Optional[UnlokRath] = None,
) -> Message:
    """Send


     send: Message represent the message of an agent on a room


    Arguments:
        text (str): text
        room (ID): room
        agent_id (str): agentId
        attach_structures (Optional[List[StructureInput]], optional): attachStructures.
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Message"""
    return execute(
        SendMutation,
        {
            "text": text,
            "room": room,
            "agentId": agent_id,
            "attachStructures": attach_structures,
        },
        rath=rath,
    ).send


async def acreate_client(
    input: DevelopmentClientInput, rath: Optional[UnlokRath] = None
) -> str:
    """CreateClient


     createDevelopmentalClient: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.


    Arguments:
        input (DevelopmentClientInput): input
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        str"""
    return (
        await aexecute(CreateClientMutation, {"input": input}, rath=rath)
    ).create_developmental_client


def create_client(
    input: DevelopmentClientInput, rath: Optional[UnlokRath] = None
) -> str:
    """CreateClient


     createDevelopmentalClient: The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.


    Arguments:
        input (DevelopmentClientInput): input
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        str"""
    return execute(
        CreateClientMutation, {"input": input}, rath=rath
    ).create_developmental_client


async def acreate_stream(
    input: CreateStreamInput, rath: Optional[UnlokRath] = None
) -> Stream:
    """CreateStream


     createStream: Stream(id, agent, title, token)


    Arguments:
        input (CreateStreamInput): input
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Stream"""
    return (
        await aexecute(CreateStreamMutation, {"input": input}, rath=rath)
    ).create_stream


def create_stream(input: CreateStreamInput, rath: Optional[UnlokRath] = None) -> Stream:
    """CreateStream


     createStream: Stream(id, agent, title, token)


    Arguments:
        input (CreateStreamInput): input
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Stream"""
    return execute(CreateStreamMutation, {"input": input}, rath=rath).create_stream


async def acreate_room(
    title: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[UnlokRath] = None,
) -> Room:
    """CreateRoom


     createRoom: Room(id, title, description, creator)


    Arguments:
        title (Optional[str], optional): title.
        description (Optional[str], optional): description.
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Room"""
    return (
        await aexecute(
            CreateRoomMutation, {"title": title, "description": description}, rath=rath
        )
    ).create_room


def create_room(
    title: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[UnlokRath] = None,
) -> Room:
    """CreateRoom


     createRoom: Room(id, title, description, creator)


    Arguments:
        title (Optional[str], optional): title.
        description (Optional[str], optional): description.
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Room"""
    return execute(
        CreateRoomMutation, {"title": title, "description": description}, rath=rath
    ).create_room


async def aget_stream(id: ID, rath: Optional[UnlokRath] = None) -> Stream:
    """GetStream


     stream: Stream(id, agent, title, token)


    Arguments:
        id (ID): id
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Stream"""
    return (await aexecute(GetStreamQuery, {"id": id}, rath=rath)).stream


def get_stream(id: ID, rath: Optional[UnlokRath] = None) -> Stream:
    """GetStream


     stream: Stream(id, agent, title, token)


    Arguments:
        id (ID): id
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Stream"""
    return execute(GetStreamQuery, {"id": id}, rath=rath).stream


async def aget_room(id: ID, rath: Optional[UnlokRath] = None) -> Room:
    """GetRoom


     room: Room(id, title, description, creator)


    Arguments:
        id (ID): id
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Room"""
    return (await aexecute(GetRoomQuery, {"id": id}, rath=rath)).room


def get_room(id: ID, rath: Optional[UnlokRath] = None) -> Room:
    """GetRoom


     room: Room(id, title, description, creator)


    Arguments:
        id (ID): id
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        Room"""
    return execute(GetRoomQuery, {"id": id}, rath=rath).room


async def awatch_room(
    room: ID, agent_id: ID, rath: Optional[UnlokRath] = None
) -> AsyncIterator[WatchRoomSubscriptionRoom]:
    """WatchRoom



    Arguments:
        room (ID): room
        agent_id (ID): agentId
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        WatchRoomSubscriptionRoom"""
    async for event in asubscribe(
        WatchRoomSubscription, {"room": room, "agentId": agent_id}, rath=rath
    ):
        yield event.room


def watch_room(
    room: ID, agent_id: ID, rath: Optional[UnlokRath] = None
) -> Iterator[WatchRoomSubscriptionRoom]:
    """WatchRoom



    Arguments:
        room (ID): room
        agent_id (ID): agentId
        rath (unlok_next.rath.UnlokRath, optional): The client we want to use (defaults to the currently active client)

    Returns:
        WatchRoomSubscriptionRoom"""
    for event in subscribe(
        WatchRoomSubscription, {"room": room, "agentId": agent_id}, rath=rath
    ):
        yield event.room


DevelopmentClientInput.update_forward_refs()
