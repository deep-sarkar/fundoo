from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Note


@registry.register_document
class NoteDocument(Document):
    user = fields.ObjectField(
        properties={
            'username':fields.TextField()
        }
    )

    label = fields.NestedField()

    class Index:
        name = 'notes'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Note
        fields = [
            'id',
            'title',
            'note',
            'urls',
        ]

