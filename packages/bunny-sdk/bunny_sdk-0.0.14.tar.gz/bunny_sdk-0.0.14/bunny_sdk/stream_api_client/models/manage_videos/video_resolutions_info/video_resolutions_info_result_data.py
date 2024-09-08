from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .video_resolutions_info_data import VideoResolutionsInfoData

from .video_resolutions_info_data import VideoResolutionsInfoData

@dataclass
class VideoResolutionsInfoResult_data(VideoResolutionsInfoData):
    """
    The resolutions info.
    """
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VideoResolutionsInfoResult_data:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VideoResolutionsInfoResult_data
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VideoResolutionsInfoResult_data()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .video_resolutions_info_data import VideoResolutionsInfoData

        from .video_resolutions_info_data import VideoResolutionsInfoData

        fields: Dict[str, Callable[[Any], None]] = {
        }
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        super().serialize(writer)
    

