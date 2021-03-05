from graphene import relay, ObjectType, Mutation, Boolean, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .api.serializers import BookSerializer, AuthorSerializer
from graphene_django.rest_framework.mutation import SerializerMutation
from .filters import BookFilter
from .models import Book, Author, BookImage
from graphene_file_upload.scalars import Upload
import boto3
import uuid

#AWS S3 BUCKET
S3_BASE_URL = "s3.amazonaws.com"
BUCKET = 'libby-app'

class BookImageNode(DjangoObjectType):
    class Meta:
        model = BookImage   

class BookNode(DjangoObjectType):
    class Meta:
        model = Book
        interfaces = (relay.Node, )

class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = []
        interfaces = (relay.Node, )

class BookMutation(SerializerMutation):
    class Meta:
        serializer_class = BookSerializer

class BooktImageMutation(Mutation):
    class Arguments:
        file = Upload(required=True)
        id = ID(required=True)

    success = Boolean()

    def mutate(self, info, file, **data):
        photo_file = file
        book_id = data.get('id')

        if photo_file and book_id:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                url = f"https://{BUCKET}.{S3_BASE_URL}/{key}"
                photo = BookImage(url=url, book_id=book_id)
                photo.save()
            except Exception as err:
                print('Oops! Tivemos um problema em fazer o upload de sua imagem: %s' % err)
                return BooktImageMutation(success=False)

        else:
            print('Falta do id do livro ou url da imagem')
            return BooktImageMutation(success = False)

        return BooktImageMutation(success=True)

class Query(ObjectType):
    book = relay.Node.Field(BookNode)
    books = DjangoFilterConnectionField(BookNode, filterset_class=BookFilter)
    author = relay.Node.Field(AuthorNode)
    authors = DjangoFilterConnectionField(AuthorNode)

class Mutation(ObjectType):
    book_mutation = BookMutation.Field()
    book_image_mutation = BooktImageMutation.Field()
