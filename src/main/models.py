from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
import datetime


# Create your models here.

# NOTE: since we can't make variables private and still have Django work, we don't need to add getters and setters


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Player'),
        (2, 'Sponsor'),
        (3, 'Drinkmeister'),
        (4, 'Manager'),
    )

    user_type = models.PositiveSmallIntegerField(default=1, choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=300)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    email = models.EmailField(max_length=80)
    date_joined = models.DateTimeField(auto_now_add=True)  # This only evaluates when User instance is first made!
    balance = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def orderDrink(self, name, qty, instructions):
        for i in range(qty):
            order = Order()
            order.timeOrdered = models.TimeField(auto_now=True)
            order.drink = name
            order.specificInstructions = instructions
            order.served = False
            order.user = self
            order.save()


class Manager(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name='manager')
    yearsWorked = models.IntegerField()
    mostMoneyHeld = models.IntegerField()
    drinksSold = models.IntegerField()
    totalTournamentsMade = models.IntegerField()
    communityPosts = models.TextField(max_length=2000, default="")

    @staticmethod
    def createTournament(name, startTime, endTime, sponsor, approved, completed):
        tournament = Tournament(name, startTime, endTime, sponsor, approved, completed)
        tournament.save()

    @staticmethod
    def editTournament(tournament, name, startTime, endTime, sponsor, approved, completed):
        tournament.name = name
        tournament.startTime = startTime
        tournament.endTime = endTime
        tournament.sponsor = sponsor
        tournament.approved = approved
        tournament.completed = completed
        tournament.save()

    @staticmethod
    def verifySponsor(sponsor):
        sponsor.canSponsorTournament = True
        sponsor.save()

    @staticmethod
    def verifyDrinkmeister(drinkmeister):
        drinkmeister.isAllowedToServeDrinks = True
        drinkmeister.save()

    @staticmethod
    def editDrink(drink, name, price, instructions):
        drink.name = name
        drink.price = price
        drink.instructions = instructions
        drink.save()

    @staticmethod
    def addDrink(name, price, instructions):
        drink = Drink(name, price, instructions)
        drink.save()


class Player(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name='player')

    def joinTournament(self, tournament):
        tournament.players.add(self)
        tournament.save()
        for hole in tournament.holes.filter():
            newScore = Score(hole=hole, player=self, tournament=tournament)
            newScore.save()


class Sponsor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name='sponsor')
    companyName = models.CharField(max_length=300)
    canSponsorTournament = models.BooleanField(default=False)

    def sponsorTournament(self, tournament):
        if self.canSponsorTournament:
            tournament.sponsor.add(self)
            tournament.save()
        else:
            return "You do not have authorization to sponsor tournaments"


class Drinkmeister(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='drinkmeister')
    employeeID = models.AutoField(primary_key=True)
    isAllowedToServeDrinks = models.BooleanField(default=False)

    def makeAndDeliverOrder(self, order):
        if self.isAllowedToServeDrinks:
            order.served = True
            order.save()
        else:
            return "You do not have authorization to serve drinks."

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.employeeID)


class Drink(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    price = models.IntegerField()
    instructions = models.CharField(max_length=300)


class Order(models.Model):
    timeOrdered = models.TimeField(auto_now=True)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE)
    specificInstructions = models.CharField(max_length=300)
    served = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    location = models.IntegerField(default=0)


class TransactionManager(models.Manager):
    def create_transaction(self, amount, toAccount, fromAccount):
        transaction = self.create(amount=amount, account=toAccount, from_account=fromAccount)
        transaction.save()
        return transaction


class Transaction(models.Model):
    date = models.DateField(auto_now=True)
    from_account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.FloatField()
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user')
    objects = TransactionManager()


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, unique=True)
    date = models.DateField(unique=True)
    startTime = models.TimeField(default=datetime.time(9, 00))
    endTime = models.TimeField(default=datetime.time(14, 30))
    players = models.ManyToManyField('Player', blank=True)
    sponsor = models.ForeignKey('Sponsor', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    holes = models.ManyToManyField('Hole')

    def addHoles(self, holeList):
        self.holes.add(holeList)
        self.save()

    def __str__(self):
        return str(self.name) + " tournament - " + str(self.date)


class Hole(models.Model):
    holeNumber = models.IntegerField(primary_key=True)
    par = models.SmallIntegerField(default=3)

    def __str__(self):
        return str(self.holeNumber)


class Score(models.Model):
    hole = models.ForeignKey('Hole', on_delete=models.CASCADE)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['hole', 'tournament', "player"], name="tournament_hole"),
        ]

    def __str__(self):
        return str(self.tournament) + ", " + str(self.hole) + ", " + str(self.player)


class Prize(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
    amount = models.IntegerField()
