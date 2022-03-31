from rest_framework.serializers import ModelSerializer
from webpush.models import SubscriptionInfo
from notifications.models import UserSubscription


class SubscriptionSerializer(ModelSerializer):

    def create(self):
        return SubscriptionInfo(**self.validated_data)

    class Meta:
        model = SubscriptionInfo
        fields = "__all__"


class UserSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = "__all__"
