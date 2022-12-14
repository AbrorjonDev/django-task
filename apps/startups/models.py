from django.db import models
from django.conf import settings
from apps.user.models import User
class BaseModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE, related_name="+")
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    
class Startups(BaseModel):
    name = models.CharField("Biznes nomi", max_length=150, unique=True)

    class Meta:
        verbose_name = "Startup"
        verbose_name_plural = "Startups"
        ordering = ("id", )
    def __str__(self):
        return self.name

    @property
    def get_revenues(self):
        return self.revenues.all()

    @property
    def curr_month_revenue(self):
        return self.get_revenues.last()


    @property
    def curr_month_outgoing(self):
        return self.outgoings.all().last()

    @property
    def all_users_revenues(self):
        if self.author.is_superuser:
            users = User.objects.all()
            revenues = []
            for user in users:
                try:
                    revenues.append(self.get_revenues.filter(startup=self, author=user).first().id)
                except:
                    pass
            return self.get_revenues.filter(id__in=revenues)
            
        return []
        

class Revenues(BaseModel):
    startup = models.ForeignKey("Startups", models.CASCADE, related_name="revenues")
    income = models.IntegerField("Joriy oyda olingan daromad", default=0)
    clients = models.IntegerField("Joriy oydagi mijozlar soni", default=0)

    is_rising = models.BooleanField(default=True)
    percentage = models.IntegerField("Process on Percentage", default=0)

    client_rising = models.BooleanField(default=True)
    client_percentage = models.IntegerField("Process on Percentage", default=0)
    
    class Meta:
        verbose_name = "Revenue"
        verbose_name_plural = "Revenues"
        ordering = ("-date_created", )

    def __str__(self):
        return str(self.id)

    @property
    def get_last_outgoing(self):
        res = self.startup.outgoings.filter(author=self.author).first()
        print("OUTGOING: ", res)
        return res

class Outgoings(BaseModel):
    startup = models.ForeignKey("Startups", models.CASCADE, related_name="outgoings")
    salary = models.IntegerField("Joriy oyda olingan daromad", default=0)
    marketing = models.IntegerField("Joriy oydagi mijozlar soni", default=0)

    is_rising = models.BooleanField(default=True)
    percentage = models.IntegerField("Process on Percentage", default=0)

    marketing_rising = models.BooleanField(default=True)
    marketing_percentage = models.IntegerField("Process on Percentage", default=0)

    class Meta:
        verbose_name = "Outgoing"
        verbose_name_plural = "Outgoings"
        ordering = ("-date_created", )

    def __str__(self):
        return f"{self.id} {self.salary} {self.marketing} {self.startup} {self.startup.author} {self.author}"