from rest_framework import serializers
from .models import Run, User, AthleteInfo


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username' , 'last_name', 'first_name', 'type', 'runs_finished']
        # fields = ['id', 'username' , 'last_name', 'first_name']

    def get_type(self, obj):
        return 'coach' if obj.is_staff else 'athlete'

    def get_runs_finished(self, obj):
        return obj.run_set.filter(status='finished').count()


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'
        # fields = ['athlete_data']


class AthleteInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = AthleteInfo
        fields = ['user_id', 'weight', 'goals']
    def validate_weight(self, value):
        if value and not(0 < value < 900):
            raise serializers.ValidationError('weight должен быть > 0 и < 900')
        return value


