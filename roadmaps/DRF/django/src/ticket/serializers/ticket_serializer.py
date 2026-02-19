from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField
from ..models import Ticket
from ..choices import UserRole


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"  # error es que trae todo los atributos
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]  # error es que hay duplicacion de read_only


class TicketCommentSerializer(ModelSerializer):
    # validar que el auhtor sea admin
    author = SerializerMethodField()

    class Meta:
        model = Ticket
        fields = "__all__"

    def get_author(self, obj):
        if hasattr(obj.author, "profile") and obj.author.profile.role == UserRole.ADMIN:
            return obj.author.username

        return None
