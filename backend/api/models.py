from django.db import models
from usersauth.models import User, Profile
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
import uuid

RATING = (
    (1, '1 Star'),
    (2, '2 Star'),
    (3, '3 Star'),
    (4, '4 Star'),
    (5, '5 Star'),
)

NOTI_TYPE = (
    ('New Order', 'New Order'),
    ('New Review', 'New Review'),
    ('New QandA', 'New Q&A'),
    ('Draft', 'Draft'),
    ('Course Published', 'Course Published'),
    ('Course Enrollment Completed', 'Course Enrollment Completed')
)

PAYMENT_STATUS = (
    ('Paid', 'Paid'),
    ('Processing', 'Processing'),
    ('Failed', 'Failed')
)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='/teachers', blank=True, null=True, default='default.jpg')
    full_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.full_name
    
    def students(self):
        '''Returns all students that have been enrolled with courses of this teacher'''
        pass

    def courses(self):
        '''Returns all courses created by a particular teacher'''
        return Course.objects.filter(teacher=self)
    
    def review(self):
        '''Returns count of reviews made on courses by this teacher'''
        return Course.objects.filter(teacher=self).count()

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='course-file', default='category.jpg', null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def course_count(self):
        '''Returns count of courses in this category'''
        return Course.objects.filter(category=self).count()
    
    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

class Course(models.Model):
    class CourseLanguage(models.TextChoices):
        ENGLISH = 'EN', 'English'
        HINDI = 'HI', 'Hindi'

    class CourseLevel(models.TextChoices):
        BEGINNER = 'BEG', 'Beginner'
        INTERMEDIATE = 'INT', 'Intermediate'
        ADVANCED = 'Adv', 'Advanced'

    class CourseStatus(models.TextChoices):
        REVIEW = 'Review', 'Review'
        DISABLED = 'Disabled', 'Disabled'
        PUBLISHED = 'Published', 'Published'
        REJECTED = 'Rejected', 'Rejected'

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.FileField(upload_to='course-thumbnail/', blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    language = models.CharField(max_length=2, choices=CourseLanguage.choices, default=CourseLanguage.ENGLISH)
    level = models.CharField(max_length=3, choices=CourseLevel.choices, default=CourseLevel.BEGINNER)
    platform_status = models.CharField(max_length=10, choices=CourseStatus.choices, default=CourseStatus.PUBLISHED)
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(unique=True, prefix='course-', max_length=50, alphabet="abcdefgh12345")
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def students(self):
        '''Returns students enrolled in this course'''
        return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        '''Returns curriculum of the course. This includes all sections of this course'''
        return Section.objects.filter(course=self)
    
    def lectures(self):
        '''Returns all lectures associated with this course'''
        return Lecture.objects.filter(section__course=self)
    
    def average_rating(self):
        '''Returns average rating students gave to this course'''
        average_rating = Review.objects.filter(course=self, active=True).aggregate(avg_rating=models.Avg('rating'))
        return average_rating['avg_rating']
    
    def rating_count(self):
        '''Returns total ratings made on this course'''
        return Review.objects.filter(course=self, active=True).count()
    
    def reviews(self):
        '''Returns all reviews made on this course'''
        return Review.objects.filter(course=self, active=True)

class Section(models.Model):
    """Represents a course section/module (like "Introduction", "Advanced Topics", etc.)"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    section_id = ShortUUIDField(unique=True, max_length=50, prefix='section-', alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.course + self.title
    
    def lectures(self):
        '''Returns lectures associated with this Section of the course'''
        return Lecture.objects.filter(section=self)

class Lecture(models.Model):
    """Represents individual lessons/content within a course section"""
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='Lectures')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='lectures/',blank=True, null=True)
    duration = models.PositiveIntegerField(default=0)
    content_duration = models.CharField(max_length=20, null=True, blank=True)
    preview = models.BooleanField(default=False)
    lecture_id = ShortUUIDField(unique=True, max_length=50, prefix='lecture-', alphabet='12345abcdefgh')
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.section + self.title
    
    @property
    def duration_formatted(self):
        """Return duration in HH:MM:SS format"""
        hours = self.duration_seconds // 3600
        minutes = (self.duration_seconds % 3600) // 60
        seconds = self.duration_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
class QuestionAnswer(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, prefix='qa-',max_length=50, alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.course.title + self.user.full_name
    
    class Meta:
        ordering = ['-date']

    def messages(self):
        return QuestionAnswerResponse.objects.filter(question=self)
    
    def profile(self):
        return Profile.objects.get(user=self.user)

class QuestionAnswerResponse(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    question = models.ForeignKey(to=QuestionAnswer, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, prefix='qam-', alphabet='abcdefgh12345', max_length=50)
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.course.title + '-' + self.user.full_name
    
    class Meta:
        ordering = ['-date']
    
    def profile(self):
        return Profile.objects.get(user=self.user)

class Coupon(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    used_by = models.ManyToManyField(to=User, blank=True)
    code = models.CharField(max_length=50)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.code

class Cart(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    # course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # country = models.CharField(max_length=100, null=True, blank=True)
    # cart_id = ShortUUIDField(unique=True, prefix='cart-', max_length=50, alphabet='abcdefgh12345')
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def total_cart_items(self):
        '''Returns count of items in the cart'''
        return CartOrderItem.objects.filter(cart=self).count()

    def __str__(self):
        return f"{self.user.full_name}'s Cart"

# class CartOrder(models.Model):
#     student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     teachers = models.ManyToManyField(Teacher, blank=True)
#     sub_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
#     tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
#     total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
#     initial_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
#     saved = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
#     payment_status = models.CharField(choices=PAYMENT_STATUS, default='Processing')
#     full_name = models.CharField(max_length=100, null=True, blank=True)
#     email = models.EmailField(null=True, blank=True)
#     country = models.CharField(max_length=50, null=True, blank=True)
#     coupons = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
#     stripe_session_id = models.CharField(max_length=1000,null=True, blank=True)
#     cart_order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     date = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ['-date']

#     def order_items(self):
#         '''Return all items ordered under this order'''
#         return CartOrderItem.objects.filter(order=self)

#     def __str__(self):
#         return self.oid

class CartOrderItem(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='cart_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        unique_together = ('cart', 'course')
        ordering = ['-added_at']
    # order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, related_name='orderitem', null=True, blank=True)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_item', null=True, blank=True)
    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    # tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # initial_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # saved = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    # coupons = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    # applied_coupon = models.BooleanField(default=False)
    # order_item_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    # date = models.DateTimeField(default=timezone.now)        

    # def order_id(self):
        # return f"Order ID #{self.order.oid}"
    
    # def payment_status(self):
        # return self.order.payment_status
    
    def __str__(self):
        return self.course.title

class Certificate(models.Model):
    """Course completion certificates"""
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    certificate_id = ShortUUIDField(unique=True, max_length=50, prefix='cert-', alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.course.title
    
class CompletedLecture(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(to=Lecture, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.course.title

class EnrolledCourse(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.SET_NULL, null=True)
    order_id = models.ForeignKey(to=CartOrderItem, on_delete=models.CASCADE, null=True)
    enrollment_id = ShortUUIDField(unique=True, prefix='enrol-', max_length=50, alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.course.title

    def lectures(self):
        '''Returns lectures associated with enrolled course'''
        return Lecture.objects.filter(course=self.course)
    
    def completed_lesson(self):
        '''Returns lectures completed by user in this enrolled course'''
        return CompletedLecture.objects.filter(course=self.course, user = self.user)
    
    def curriculum(self):
        '''Returns curriculum of enrolled course'''
        return Section.objects.filter(course=self.course)
    
    def note(self):
        '''Returns notes associated with this course by the enrolled user'''
        return Note.objects.filter(course=self.course, user=self.user)
    
    def question_answer(self):
        '''Returns all Q&A associated with the enrolled course'''
        return QuestionAnswer.objects.filter(course=self.course)
    
    def review(self):
        '''Returns reviews of user for this course'''
        return Review.objects.filter(course=self.course, user=self.user).first()
    
class Note(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    note = models.TextField(max_length=1000)
    note_id = ShortUUIDField(unique=True, prefix='note-', max_length=50, alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True)
    review = models.TextField(max_length=1000)
    rating = models.CharField(choices=RATING, max_length=20)
    reply = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.course.title
    
    def profile(self):
        '''Returns profile of user who gave review'''
        return Profile.objects.get(user=self.user)
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    # order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=50, choices=NOTI_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.type

class Wishlist(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.course.title

class Country(models.Model):
    name = models.CharField(max_length=50)
    tax_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Countries'
        
    def __str__(self):
        return self.name