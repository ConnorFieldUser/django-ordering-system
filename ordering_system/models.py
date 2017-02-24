from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

ACCESS_LEVELS = [
    ('s', 'Server'),
    ('o', 'Owner'),
    ('c', 'Chef'),
]


class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    access_level = models.CharField(max_length=1, choices=ACCESS_LEVELS, default='s')

    def __str__(self):
        return str(self.user)

    @property
    def is_owner(self):
        return self.access_level == 'o'

    @property
    def is_chef(self):
        return self.access_level == 'c'

    @property
    def is_server(self):
        return self.access_level == 's'


@receiver(post_save, sender="auth.User")
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Profile.objects.create(user=instance)


class MenuItem(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=90)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    ref_id = models.IntegerField

    def __str__(self):
        return "{}".format(self.name)


TABLE_NUMBERS = [
    ('a1', 'a1'),
    ('a2', 'a2'),
    ('a3', 'a3'),
    ('a4', 'a4'),
    ('b1', 'b1'),
    ('b2', 'b2'),
    ('b3', 'b3'),
    ('b4', 'b4'),
    ('c1', 'c1'),
    ('c2', 'c2'),
    ('c3', 'c3'),
    ('c4', 'c4'),
    ('d1', 'd1'),
    ('d2', 'd2'),
    ('d3', 'd3'),
    ('d4', 'd4')
]


class Order(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    menuitems = models.ManyToManyField(MenuItem, through='OrderItem')
    paid = models.BooleanField(default=False)
    # physical table location
    table_number = models.CharField(max_length=2, choices=TABLE_NUMBERS)

    def __str__(self):
        return "Order#{}".format(self.id)

    @property
    def is_paid(self):
        return self.paid

    @property
    def total(self):
        total = 00
        for i in self.orderitem_set.all():
            total += i.menuitem.price
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    menuitem = models.ForeignKey(MenuItem)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{}: {}".format(self.order, self.menuitem)


class DailySpecial(models.Model):
    name = models.ForeignKey(MenuItem)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{}".format(self.name)
