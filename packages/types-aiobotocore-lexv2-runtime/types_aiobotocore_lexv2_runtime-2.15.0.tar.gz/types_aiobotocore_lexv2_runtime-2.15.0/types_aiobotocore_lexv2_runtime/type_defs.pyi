"""
Type annotations for lexv2-runtime service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_runtime/type_defs/)

Usage::

    ```python
    from types_aiobotocore_lexv2_runtime.type_defs import ActiveContextTimeToLiveTypeDef

    data: ActiveContextTimeToLiveTypeDef = ...
    ```
"""

import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    ConfirmationStateType,
    DialogActionTypeType,
    IntentStateType,
    InterpretationSourceType,
    MessageContentTypeType,
    SentimentTypeType,
    ShapeType,
    StyleTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ActiveContextTimeToLiveTypeDef",
    "BlobTypeDef",
    "ButtonTypeDef",
    "ConfidenceScoreTypeDef",
    "DeleteSessionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DialogActionTypeDef",
    "ElicitSubSlotTypeDef",
    "GetSessionRequestRequestTypeDef",
    "IntentOutputTypeDef",
    "IntentTypeDef",
    "RecognizedBotMemberTypeDef",
    "RuntimeHintValueTypeDef",
    "RuntimeHintsOutputTypeDef",
    "RuntimeHintsTypeDef",
    "SentimentScoreTypeDef",
    "ValueOutputTypeDef",
    "ValueTypeDef",
    "ActiveContextOutputTypeDef",
    "ActiveContextTypeDef",
    "RecognizeUtteranceRequestRequestTypeDef",
    "ImageResponseCardOutputTypeDef",
    "ImageResponseCardTypeDef",
    "DeleteSessionResponseTypeDef",
    "PutSessionResponseTypeDef",
    "RecognizeUtteranceResponseTypeDef",
    "RuntimeHintDetailsOutputTypeDef",
    "RuntimeHintDetailsTypeDef",
    "SentimentResponseTypeDef",
    "SlotOutputTypeDef",
    "SlotTypeDef",
    "SessionStateOutputTypeDef",
    "SessionStateTypeDef",
    "MessageOutputTypeDef",
    "MessageTypeDef",
    "InterpretationTypeDef",
    "RecognizeTextRequestRequestTypeDef",
    "MessageUnionTypeDef",
    "GetSessionResponseTypeDef",
    "RecognizeTextResponseTypeDef",
    "PutSessionRequestRequestTypeDef",
)

ActiveContextTimeToLiveTypeDef = TypedDict(
    "ActiveContextTimeToLiveTypeDef",
    {
        "timeToLiveInSeconds": int,
        "turnsToLive": int,
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ButtonTypeDef = TypedDict(
    "ButtonTypeDef",
    {
        "text": str,
        "value": str,
    },
)
ConfidenceScoreTypeDef = TypedDict(
    "ConfidenceScoreTypeDef",
    {
        "score": NotRequired[float],
    },
)
DeleteSessionRequestRequestTypeDef = TypedDict(
    "DeleteSessionRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
DialogActionTypeDef = TypedDict(
    "DialogActionTypeDef",
    {
        "type": DialogActionTypeType,
        "slotToElicit": NotRequired[str],
        "slotElicitationStyle": NotRequired[StyleTypeType],
        "subSlotToElicit": NotRequired["ElicitSubSlotTypeDef"],
    },
)
ElicitSubSlotTypeDef = TypedDict(
    "ElicitSubSlotTypeDef",
    {
        "name": str,
        "subSlotToElicit": NotRequired[Dict[str, Any]],
    },
)
GetSessionRequestRequestTypeDef = TypedDict(
    "GetSessionRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
    },
)
IntentOutputTypeDef = TypedDict(
    "IntentOutputTypeDef",
    {
        "name": str,
        "slots": NotRequired[Dict[str, "SlotOutputTypeDef"]],
        "state": NotRequired[IntentStateType],
        "confirmationState": NotRequired[ConfirmationStateType],
    },
)
IntentTypeDef = TypedDict(
    "IntentTypeDef",
    {
        "name": str,
        "slots": NotRequired[Mapping[str, "SlotTypeDef"]],
        "state": NotRequired[IntentStateType],
        "confirmationState": NotRequired[ConfirmationStateType],
    },
)
RecognizedBotMemberTypeDef = TypedDict(
    "RecognizedBotMemberTypeDef",
    {
        "botId": str,
        "botName": NotRequired[str],
    },
)
RuntimeHintValueTypeDef = TypedDict(
    "RuntimeHintValueTypeDef",
    {
        "phrase": str,
    },
)
RuntimeHintsOutputTypeDef = TypedDict(
    "RuntimeHintsOutputTypeDef",
    {
        "slotHints": NotRequired[Dict[str, Dict[str, "RuntimeHintDetailsOutputTypeDef"]]],
    },
)
RuntimeHintsTypeDef = TypedDict(
    "RuntimeHintsTypeDef",
    {
        "slotHints": NotRequired[Mapping[str, Mapping[str, "RuntimeHintDetailsTypeDef"]]],
    },
)
SentimentScoreTypeDef = TypedDict(
    "SentimentScoreTypeDef",
    {
        "positive": NotRequired[float],
        "negative": NotRequired[float],
        "neutral": NotRequired[float],
        "mixed": NotRequired[float],
    },
)
ValueOutputTypeDef = TypedDict(
    "ValueOutputTypeDef",
    {
        "interpretedValue": str,
        "originalValue": NotRequired[str],
        "resolvedValues": NotRequired[List[str]],
    },
)
ValueTypeDef = TypedDict(
    "ValueTypeDef",
    {
        "interpretedValue": str,
        "originalValue": NotRequired[str],
        "resolvedValues": NotRequired[Sequence[str]],
    },
)
ActiveContextOutputTypeDef = TypedDict(
    "ActiveContextOutputTypeDef",
    {
        "name": str,
        "timeToLive": ActiveContextTimeToLiveTypeDef,
        "contextAttributes": Dict[str, str],
    },
)
ActiveContextTypeDef = TypedDict(
    "ActiveContextTypeDef",
    {
        "name": str,
        "timeToLive": ActiveContextTimeToLiveTypeDef,
        "contextAttributes": Mapping[str, str],
    },
)
RecognizeUtteranceRequestRequestTypeDef = TypedDict(
    "RecognizeUtteranceRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
        "requestContentType": str,
        "sessionState": NotRequired[str],
        "requestAttributes": NotRequired[str],
        "responseContentType": NotRequired[str],
        "inputStream": NotRequired[BlobTypeDef],
    },
)
ImageResponseCardOutputTypeDef = TypedDict(
    "ImageResponseCardOutputTypeDef",
    {
        "title": str,
        "subtitle": NotRequired[str],
        "imageUrl": NotRequired[str],
        "buttons": NotRequired[List[ButtonTypeDef]],
    },
)
ImageResponseCardTypeDef = TypedDict(
    "ImageResponseCardTypeDef",
    {
        "title": str,
        "subtitle": NotRequired[str],
        "imageUrl": NotRequired[str],
        "buttons": NotRequired[Sequence[ButtonTypeDef]],
    },
)
DeleteSessionResponseTypeDef = TypedDict(
    "DeleteSessionResponseTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutSessionResponseTypeDef = TypedDict(
    "PutSessionResponseTypeDef",
    {
        "contentType": str,
        "messages": str,
        "sessionState": str,
        "requestAttributes": str,
        "sessionId": str,
        "audioStream": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RecognizeUtteranceResponseTypeDef = TypedDict(
    "RecognizeUtteranceResponseTypeDef",
    {
        "inputMode": str,
        "contentType": str,
        "messages": str,
        "interpretations": str,
        "sessionState": str,
        "requestAttributes": str,
        "sessionId": str,
        "inputTranscript": str,
        "audioStream": StreamingBody,
        "recognizedBotMember": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RuntimeHintDetailsOutputTypeDef = TypedDict(
    "RuntimeHintDetailsOutputTypeDef",
    {
        "runtimeHintValues": NotRequired[List[RuntimeHintValueTypeDef]],
        "subSlotHints": NotRequired[Dict[str, Dict[str, Any]]],
    },
)
RuntimeHintDetailsTypeDef = TypedDict(
    "RuntimeHintDetailsTypeDef",
    {
        "runtimeHintValues": NotRequired[Sequence[RuntimeHintValueTypeDef]],
        "subSlotHints": NotRequired[Mapping[str, Dict[str, Any]]],
    },
)
SentimentResponseTypeDef = TypedDict(
    "SentimentResponseTypeDef",
    {
        "sentiment": NotRequired[SentimentTypeType],
        "sentimentScore": NotRequired[SentimentScoreTypeDef],
    },
)
SlotOutputTypeDef = TypedDict(
    "SlotOutputTypeDef",
    {
        "value": NotRequired[ValueOutputTypeDef],
        "shape": NotRequired[ShapeType],
        "values": NotRequired[List[Dict[str, Any]]],
        "subSlots": NotRequired[Dict[str, Dict[str, Any]]],
    },
)
SlotTypeDef = TypedDict(
    "SlotTypeDef",
    {
        "value": NotRequired[ValueTypeDef],
        "shape": NotRequired[ShapeType],
        "values": NotRequired[Sequence[Dict[str, Any]]],
        "subSlots": NotRequired[Mapping[str, Dict[str, Any]]],
    },
)
SessionStateOutputTypeDef = TypedDict(
    "SessionStateOutputTypeDef",
    {
        "dialogAction": NotRequired[DialogActionTypeDef],
        "intent": NotRequired[IntentOutputTypeDef],
        "activeContexts": NotRequired[List[ActiveContextOutputTypeDef]],
        "sessionAttributes": NotRequired[Dict[str, str]],
        "originatingRequestId": NotRequired[str],
        "runtimeHints": NotRequired[RuntimeHintsOutputTypeDef],
    },
)
SessionStateTypeDef = TypedDict(
    "SessionStateTypeDef",
    {
        "dialogAction": NotRequired[DialogActionTypeDef],
        "intent": NotRequired[IntentTypeDef],
        "activeContexts": NotRequired[Sequence[ActiveContextTypeDef]],
        "sessionAttributes": NotRequired[Mapping[str, str]],
        "originatingRequestId": NotRequired[str],
        "runtimeHints": NotRequired[RuntimeHintsTypeDef],
    },
)
MessageOutputTypeDef = TypedDict(
    "MessageOutputTypeDef",
    {
        "contentType": MessageContentTypeType,
        "content": NotRequired[str],
        "imageResponseCard": NotRequired[ImageResponseCardOutputTypeDef],
    },
)
MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "contentType": MessageContentTypeType,
        "content": NotRequired[str],
        "imageResponseCard": NotRequired[ImageResponseCardTypeDef],
    },
)
InterpretationTypeDef = TypedDict(
    "InterpretationTypeDef",
    {
        "nluConfidence": NotRequired[ConfidenceScoreTypeDef],
        "sentimentResponse": NotRequired[SentimentResponseTypeDef],
        "intent": NotRequired[IntentOutputTypeDef],
        "interpretationSource": NotRequired[InterpretationSourceType],
    },
)
RecognizeTextRequestRequestTypeDef = TypedDict(
    "RecognizeTextRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
        "text": str,
        "sessionState": NotRequired[SessionStateTypeDef],
        "requestAttributes": NotRequired[Mapping[str, str]],
    },
)
MessageUnionTypeDef = Union[MessageTypeDef, MessageOutputTypeDef]
GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "sessionId": str,
        "messages": List[MessageOutputTypeDef],
        "interpretations": List[InterpretationTypeDef],
        "sessionState": SessionStateOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RecognizeTextResponseTypeDef = TypedDict(
    "RecognizeTextResponseTypeDef",
    {
        "messages": List[MessageOutputTypeDef],
        "sessionState": SessionStateOutputTypeDef,
        "interpretations": List[InterpretationTypeDef],
        "requestAttributes": Dict[str, str],
        "sessionId": str,
        "recognizedBotMember": RecognizedBotMemberTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutSessionRequestRequestTypeDef = TypedDict(
    "PutSessionRequestRequestTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "sessionId": str,
        "sessionState": SessionStateTypeDef,
        "messages": NotRequired[Sequence[MessageUnionTypeDef]],
        "requestAttributes": NotRequired[Mapping[str, str]],
        "responseContentType": NotRequired[str],
    },
)
