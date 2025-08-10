from django.db import models
from usersauth.models import User, Profile

from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone


LANGUAGE = (
    ('English', 'English'),
    ('Roman English', 'Roman English'),
    ('Hindi', 'Hindi')
)

LEVEL = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced')
)

PLATFORM_STATUS = (
    ('Review', 'Review'),
    ('Disabled', 'Disabled'),
    ('Rejected', 'Rejected'),
    ('Published', 'Published')
)

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

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='course-file', blank=True, null=True, default='default.jpg')
    full_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, blank=True, null=True)
    language = models.CharField(choices=LANGUAGE, default='English', max_length=20, blank=True, null=True)
    level = models.CharField(choices=LEVEL, default='Beginner', null=True, blank=True)
    platform_status = models.CharField(choices=PLATFORM_STATUS, default='Published', null=True, blank=True)
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(unique=True, prefix='course-', max_length=50, alphabet="abcdefgh12345")
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title) + str(self.pk)
        super(Course, self).save(*args, **kwargs)

    def students(self):
        '''Returns students enrolled in this course'''
        return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        '''Returns curriculum of the course. This includes all sections of this course'''
        return Section.objects.filter(course=self)
    
    def lectures(self):
        '''Returns all lectures associated with this course'''
        return Lecture.objects.filter(course=self)
    
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    section_id = ShortUUIDField(unique=True, max_length=50, prefix='section-', alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course + self.title
    
    def lessons(self):
        '''Returns lectures associated with this Section of the course'''
        return Lecture.objects.filter(section=self)
    

class Lecture(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='Lectures')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    file = models.CharField(max_length=200)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=20, null=True, blank=True)
    preview = models.BooleanField(default=False)
    lecture_id = ShortUUIDField(unique=True, max_length=50, prefix='lecture-', alphabet='12345abcdefgh')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.section + self.title


class QuestionAnswer(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, prefix='qa-',max_length=50, alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now)

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
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title + '-' + self.user.full_name
    
    class Meta:
        ordering = ['-date']
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    

class Cart(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    country = models.CharField(max_length=100, null=True, blank=True)
    cart_id = ShortUUIDField(unique=True, prefix='cart-', max_length=50, alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.cart_id
    

class CartOrder(models.Model):
    pass

class CartOrderItem(models.Model):
    pass

class Certificate(models.Model):
    """Course completion certificates"""
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    certificate_id = ShortUUIDField(unique=True, max_length=50, prefix='cert-', alphabet='abcdefgh12345')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.course.title
    
class CompletedLecture(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(to=Lecture, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title

class EnrolledCourse(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.SET_NULL, null=True)
    order_id = models.ForeignKey(to=CartOrderItem, on_delete=models.CASCADE)
    enrollment_id = ShortUUIDField(unique=True, prefix='enrol-', max_length=50, alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now)

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
    

class Note(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, prefix='note-', max_length=50, alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.CharField(choices=RATING, max_length=20)
    reply = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title
    
    def profile(self):
        '''Returns profile of user who gave review'''
        return Profile.objects.get(user=self.user)
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=50, choices=NOTI_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.type


class Coupon(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    used_by = models.ManyToManyField(to=User, blank=True)
    code = models.CharField(max_length=50)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code
    
class Wishlist(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.course.title
    

class Country(models.Model):
    name = models.CharField(max_length=50)
    tax_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name