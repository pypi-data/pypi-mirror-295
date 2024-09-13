from typing import Literal, Union, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class IdSchema(BaseModel):
    id: str


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class FieldSchema(BaseSchema):
    name: str
    value: Union[bool, str, int, float, list[str], list[int], list[float]]


class ItemSchema(BaseSchema):
    id: str
    fields: Optional[list[FieldSchema]] = None
    label: Optional[str] = None


class FeedbackSchema(BaseSchema):
    event: Literal["item", "user", "interaction", "ranking"]
    id: str
    item: Optional[str] = None
    items: Optional[list[ItemSchema]] = None
    fields: Optional[list[FieldSchema]] = None
    user: Optional[str] = None
    ranking: Optional[str] = None
    session: Optional[str] = None
    timestamp: Union[int, str]
    type: Optional[str] = None


class FeedbackResponse(BaseSchema):
    accepted: int
    status: str
    tookMillis: int
    updated: int


class FeatureSchema(BaseSchema):
    name: str
    weight: list[float]
    

class IterationSchema(BaseSchema):
    id: str
    millis: int
    test_metric: float
    train_metric: float


class RankSchema(BaseSchema):
    id: str
    user: Optional[str] = None
    session: Optional[str] = None
    timestamp: Union[int, str]
    fields: Optional[list[FieldSchema]] = None
    items: list[ItemSchema]

    
class ItemResponse(BaseSchema):
    item: str
    score: float
    features: Optional[Union[list[FieldSchema], dict]] = None
    

class RankResponse(BaseSchema):
    took: int
    items: list[ItemResponse]


class RecommendSchema(BaseSchema):
    count: int
    user: str
    items: list[str]
    
    
class RecommendResponse(BaseSchema):
    took: int
    items: list[ItemResponse]


class TrainResponse(BaseSchema):
    features: list[FeatureSchema]
    iterations: list[IterationSchema]
    size_bytes: int


class InferenceEncoderSchema(BaseSchema):
    texts: list[str]


class InferenceEncoderResponse(BaseSchema):
    took: int
    embeddings: list[list[float]]


class QueryDocumentPairSchema(BaseSchema):
    query: str
    text: str


class InferenceCrossSchema(BaseSchema):
    input: list[QueryDocumentPairSchema]


class InferenceCrossResponse(BaseSchema):
    took: int
    scores: list[float]
