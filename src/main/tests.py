from django.test import TestCase
from . import models


class PlayerTestCase(TestCase):
    def setUp(self):
        admin = models.User.objects.create_user(username="admin", id=0,
                                                email="admin@admin.com",
                                                password="asdf",
                                                user_type="1",
                                                phone_number="1234567899")
        models.Player.objects.create(user=admin)

    def test_player(self):
        player = models.Player.objects.get(user=0)
        self.assertEqual(player.user.username, "admin")
        self.assertEqual(player.user.phone_number, "1234567899")


class UserTestCase(TestCase):
    def setUp(self):
        models.User.objects.create_user(username="admin", id=0,
                                        email="admin@admin.com",
                                        password="asdf",
                                        user_type="1",
                                        phone_number="1234567899")

    def test_user(self):
        user = models.User.objects.get(id=0)
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.user_type, 1)
        self.assertEqual(user.email, "admin@admin.com")
        self.assertNotEqual(user.phone_number, "12345")


class ManagerTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create_user(username="admin", id=0,
                                               email="admin@admin.com",
                                               password="asdf",
                                               user_type="4",
                                               phone_number="1234567899")

        models.Manager.objects.create(user = user, yearsWorked = 22 , mostMoneyHeld = 2000, drinksSold = 34, totalTournamentsMade = 132)

    def test_manager(self):
        manager = models.Manager.objects.get(user=0)
        self.assertEqual(manager.user.username, "admin")
        self.assertEqual(manager.yearsWorked , 22)
        self.assertEqual(manager.drinksSold, 34)
        self.assertNotEqual(manager.totalTournamentsMade , 12)


class DrinkmeisterTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create_user(username="admin", id=0,
                                               email="admin@admin.com",
                                               password="asdf",
                                               user_type="3",
                                               phone_number="1234567899")
        models.Drinkmeister.objects.create(user = user, isAllowedToServeDrinks = True)

    def test_drinkmeister(self):
        drinkmeister = models.Drinkmeister.objects.get(user=0)
        self.assertEqual(drinkmeister.user.username , "admin")
        self.assertEqual(drinkmeister.isAllowedToServeDrinks, True)
        self.assertEqual(drinkmeister.user.user_type , 3)


class SponsorTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create_user(username="admin", id=0,
                                               email="admin@admin.com",
                                               password="asdf",
                                               user_type="4",
                                               phone_number="1234567899")
        models.Sponsor.objects.create(user = user, companyName = "Coke")

    def test_sponsor(self):
        sponsor = models.Sponsor.objects.get(user=0)
        self.assertEqual(sponsor.user.username, "admin")
        self.assertEqual(sponsor.user.user_type, 4)
        self.assertEqual(sponsor.companyName, "Coke")
        self.assertEqual(sponsor.canSponsorTournament, False)

class DrinksTest(TestCase):
    def setUp(self):
        models.Drink.objects.create(name = "Nuka Cola", price = 12, instructions = "Add coke to a glass and serve")

    def test_drink(self):
        drink = models.Drink.objects.get(name="Nuka Cola")
        self.assertEqual(drink.name, "Nuka Cola")
        self.assertEqual(drink.price, 12)
        self.assertEqual(drink.instructions, "Add coke to a glass and serve")

class OrderTest(TestCase):
    def setUp(self):
        user = models.User.objects.create_user(username="admin", id=0,
                                               email="admin@admin.com",
                                               password="asdf",
                                               user_type="4",
                                               phone_number="1234567899")

        drink = models.Drink.objects.create(name = "Nuka Cola", price = 12, instructions = "Add coke to a glass and serve")

        models.Order.objects.create(drink = drink, specificInstructions = "None", user = user, location = 3)

    def test_order(self):
        order = models.Order.objects.get(user=0)
        self.assertEqual(order.user.username, "admin")
        self.assertEqual(order.user.user_type, 4)
        self.assertEqual(order.drink.name , "Nuka Cola")
        self.assertEqual(order.drink , models.Drink.objects.get(name="Nuka Cola"))
        self.assertEqual(order.specificInstructions, "None")
        self.assertEqual(order.location, 3)
