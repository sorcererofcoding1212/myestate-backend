from rest_framework import serializers
from .models import Message
from ..accounts.serializers import AccountInformationSerializer


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["content", "phone_number", "message_type", "date", "time"]

    def validate(self, attrs):
        message_type = attrs.get("message_type")

        if message_type == Message.MessageType.CONTACT_MESSAGE:
            content = attrs.get("content")

            if not content or not content.strip():
                raise serializers.ValidationError({
                    "content": "This field is required."
                })

        elif message_type == Message.MessageType.VIEWING_REQUEST:
            date = attrs.get("date")
            time = attrs.get("time")

            if not date:
                raise serializers.ValidationError({
                    "date": "This field is required."
                })

            if not time:
                raise serializers.ValidationError({
                    "time": "This field is required."
                })

        return attrs


class ListMessageSerializer(serializers.ModelSerializer):
    sender = AccountInformationSerializer(read_only=True)
    content = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["sender", "id",
                  "created_at", "message_type", "content"]

    def get_content(self, obj):
        sender = obj.sender
        if obj.message_type == Message.MessageType.VIEWING_REQUEST:
            formatted_date = obj.date.strftime("%d %B")
            formatted_time = obj.time.strftime("%I:%M %p")
            content = f"New viewing request from {sender.first_name} {sender.last_name}, scheduled for {formatted_date} at {formatted_time}."
            return content

        return obj.content


class GetMessageSerializer(serializers.ModelSerializer):
    sender = AccountInformationSerializer(read_only=True)
    content = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["sender", "id",
                  "created_at", "message_type", "content", "phone_number", "property"]

    def get_content(self, obj):
        sender = obj.sender
        if obj.message_type == Message.MessageType.VIEWING_REQUEST:
            formatted_date = obj.date.strftime("%d %B")
            formatted_time = obj.time.strftime("%I:%M %p")
            content = f"New viewing request from {sender.first_name} {sender.last_name}, scheduled for {formatted_date} at {formatted_time}."
            return content

        return obj.content
