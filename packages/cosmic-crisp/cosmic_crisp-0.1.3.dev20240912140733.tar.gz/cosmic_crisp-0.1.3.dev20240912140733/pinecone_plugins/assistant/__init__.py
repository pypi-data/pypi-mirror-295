from pinecone_plugin_interface import PluginMetadata
from .assistant import Assistant
from .assistant import Evaluation


__installables__ = [
    PluginMetadata(
        target_object="Pinecone",
        namespace="assistant",
        implementation_class=Assistant
    ),
    PluginMetadata(
        target_object="Pinecone",
        namespace="evaluation",
        implementation_class=Evaluation
    )
]

