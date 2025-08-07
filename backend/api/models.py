from django.db import models
from usersauth.models import User

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
    

    '''
        Returns all students that have been enrolled with courses of this teacher
    '''
    def students(self):
        pass


    '''
    Returns all courses created by a particular teacher
    '''
    def courses(self):
        return Courses.objects.filter(teacher=self)
    

    '''
        Returns count of reviews made on courses by this teacher
    '''
    def review(self):
        return Courses.objects.filter(teacher=self).count()
    

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
    
    '''
        Returns count of courses in this category
    '''
    def course_count(self):
        return Courses.objects.filter(category=self).count()
    
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
    course_id = ShortUUIDField(unique=True, max_length=20, alphabet="abcdefgh12345")
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.title) + str(self.pk)
        super(Course, self).save(*args, **kwargs)

    '''Returns students enrolled in this course'''
    def students(self):
        return EnrolledCourse.objects.filter(course=self)
    
    '''Returns curriculum of the course. This includes all sections of this course'''
    def curriculum(self):
        return Section.objects.filter(course=self)
    
    '''Returns all lectures associated with this course'''
    def lectures(self):
        return Lecture.objects.filter(course=self)
    
    '''Returns average rating students gave to this course'''
    def average_rating(self):
        average_rating = Review.objects.filter(course=self, active=True).aggregate(avg_rating=models.Avg('rating'))
        return average_rating['avg_rating']
    
    '''Returns total ratings made on this course'''
    def rating_count(self):
        return Review.objects.filter(course=self, active=True).count()
    
    '''Returns all reviews made on this course'''
    def reviews(self):
        return Review.objects.filter(course=self, active=True)
    

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    section_id = ShortUUIDField(unique=True, max_length=20, alphabet='abcdefgh12345')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course + self.title
    
    '''Returns lectures associated with this Section of the course'''
    def lessons(self):
        return Lecture.objects.filter(section=self)
    

class Lecture(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='Lectures')
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    file = models.CharField(max_length=200)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=20, null=True, blank=True)
    preview = models.BooleanField(default=False)
    lecture_id = ShortUUIDField(unique=True, max_length=20, alphabet='12345abcdefgh')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.section + self.title


