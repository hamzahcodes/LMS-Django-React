from usersauth.models import Profile, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from api import models as api_models

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username

        return token
    
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password2']

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({ 'password': "Passwords field didn't match"})
        
        return attr
        
    def create(self, validated_data):
        user = User.objects.create(
            full_name = validated_data['full_name'],
            email = validated_data['email']
        )
        print(user)
        email_username = user.email.split('@')[0]
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Category
        fields = ['id', 'title', 'image', 'slug', 'course_count']

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [ "user", "image", "full_name", "bio", "twitter", "linkedin", "about", "country", "students", "courses", "review",]
        model = api_models.Teacher

class LectureSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = api_models.Lecture
    
    def __init__(self, *args, **kwargs):
        super(LectureSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class SectionSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = api_models.Section

    def __init__(self, instance=None, data=..., **kwargs):
        super(SectionSerializer, self).__init__(instance, data, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class CompletedLectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.CompletedLecture
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Note
        fields = '__all__'


class QuestionAnswerResponseSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.QuestionAnswerResponse
        fields = '__all__'


class QuestionAnswerSerializer(serializers.ModelSerializer):
    messages = QuestionAnswerResponseSerializer(many=True)
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.QuestionAnswer
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Review
        fields = '__all__'


class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True)
    completed_lesson = CompletedLectureSerializer(many=True)
    curriculum = SectionSerializer(many=True)
    note = NoteSerializer(many=True)
    question_answer = QuestionAnswerSerializer(many=True)
    review = ReviewSerializer(many=True)

    class Meta:
        model = api_models.EnrolledCourse
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    students = EnrolledCourseSerializer(many=True)
    curriculum = SectionSerializer(many=True)
    lectures = LectureSerializer(many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = api_models.Course
        fields = [ 'category','teacher','file','image','title','description','price','language','level','platform_status','featured','course_id','slug','date','students','curriculum','lectures','average_rating','rating_count','reviews']


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Cart
        fields = '__all__'


class CartOrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = api_models.CartOrderItem
        fields = '__all__'


class CartOrderSerializer(serializers.ModelSerializer):
    order_items = CartOrderItemSerializer(many=True)
    class Meta:
        model = api_models.CartOrder
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Certificate
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Certificate
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Notification
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Coupon
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Wishlist
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Country
        fields = '__all__'