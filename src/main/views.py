from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from .models import *
from .forms import *


# Create your views here.


def tournament(request, tournamentName):
    if request.user.user_type == 1:
        tourney = Tournament.objects.get(name=tournamentName)
        nextHole = 1
        if request.method == "POST":
            if request.POST.get('join'):
                request.user.player.joinTournament(tourney)
            else:
                hole = Hole.objects.get(holeNumber=request.POST.get('hole'))
                nextHole = int(request.POST.get('hole')) + 1
                score = Score.objects.get(tournament=tourney, player=request.user.player, hole=hole)
            if request.POST.get('add_1'):
                score.score = 1
                score.save()
            elif request.POST.get('add_2'):
                score.score = 2
                score.save()
            elif request.POST.get('add_3'):
                score.score = 3
                score.save()
            elif request.POST.get('add_4'):
                score.score = 4
                score.save()
            elif request.POST.get('add_5'):
                score.score = 5
                score.save()
        score_list = Score.objects.filter(tournament=tourney, player=request.user.player)
        total = 0
        for score in score_list:
            total += int(score.score)
        tplayer = tourney.players.filter(user=request.user)
        context = {"tournament": tourney, "tplayer": tplayer, "holes": tourney.holes.filter(),
                   "score_list": score_list, "next_hole": nextHole, "total": total}
        return render(request, 'tournament.html', context)
    else:
        context = {}
        return redirect("tournamentInfo", tournamentName)


def drinks(request):
    if request.method == 'POST':
        newDrink = Drink.objects.get(name=request.POST.get('newDrink'))
        if (newDrink.price * 100) <= request.user.balance:
            request.user.balance = request.user.balance - (newDrink.price * 100)
            request.user.save()
            newOrder = Order()
            newOrder.user = request.user
            newOrder.drink = newDrink
            newOrder.location = request.POST.get('location')
            newOrder.specificInstructions = request.POST.get('instructions')
            newOrder.save()
            Transaction.objects.create_transaction((0 - newDrink.price), request.user, request.user)
            return render(request, 'orderConfirmation.html', {"success": True})
        else:
            return render(request, 'orderConfirmation.html', {"success": False})

    else:
        if request.user.is_anonymous:
            return HttpResponseRedirect('../login')
        holeList = Hole.objects.all()
        orders = Order.objects.filter(served=False)
        drinkList = Drink.objects.all()
        user = request.user
        return render(request, "drinks.html",
                      {"orders": orders, "drinkList": drinkList, "user": user, "holeList": holeList})


def login(request):
    return render(request, "login.html")


def logout(request):
    return render(request, "logout.html")


def error(request):
    return render(request, "error.html")


def accountCreation(request):
    return render(request, "accountCreation.html")


def home(request):
    if request.method == "POST" and request.user.user_type == 4:
        request.user.manager.communityPosts = request.POST.get("communityPosts")
        request.user.manager.save()
    manager_list = Manager.objects.all()

    context = {'manager_list': manager_list}
    return render(request, "index.html", context)


def homeRedirect():
    return redirect('home')


def account(request):
    if request.method == "POST":
        if 50000 <= request.user.balance:
            request.user.balance = request.user.balance - (50000)
            request.user.save()
            Transaction.objects.create_transaction((0 - 500), request.user, request.user)
            if not Hole.objects.all():
                for i in range(12):
                    newHole = Hole()
                    newHole.holeNumber = i+1
                    newHole.par = 3
                    newHole.save()
            if request.user.user_type != 2:
                return HttpResponseForbidden("Only sponsors can sponsor a tournament")
            for t in Tournament.objects.all():
                if str(t.date) == str(request.POST.get('date')) or t.name == request.POST.get('tournamentName'):
                    # Tournaments with almost identical names can still be created
                    # including if the only difference is a space

                    return HttpResponseRedirect('../account')
            newTournament = Tournament()
            newTournament.name = request.POST.get('tournamentName')
            newTournament.date = request.POST.get('date')
            newTournament.sponsor = request.user.sponsor
            newTournament.save()
            for hole in Hole.objects.all():
                newTournament.addHoles(hole.holeNumber)
            newTournament.save()
            return HttpResponseRedirect('../events')
        else:
            return render(request, 'orderConfirmation.html', {"success": False})
    if request.user.is_anonymous:
        return HttpResponseRedirect('../login')
    balance = float(request.user.balance) / 100.0
    context = {'balance': balance}
    if request.user.user_type == 2:
        tournaments_list = Tournament.objects.all()
        context['tournaments_list'] = tournaments_list
    print(context)
    return render(request, "account.html", context)


def bank(request):
    if request.method == 'POST':
        dest = request.user
        if request.POST.get("destAccount"):
            dest = User.objects.get(username=request.POST.get("destAccount"))
        amount = request.POST.get("transAmount")
        print(amount)
        Transaction.objects.create_transaction(amount, dest, request.user)

        dest.balance += float(amount) * 100
        dest.save()
    context = {}
    context['current_balance'] = request.user.balance / 100 if not request.user.is_anonymous else 0.00
    if not request.user.is_anonymous:
        context['transactions'] = Transaction.objects.filter(account=request.user)
    return render(request, 'bank.html', context)


def drinksEdit(request):
    if request.method == 'POST':
        if request.user.user_type != 4:
            return HttpResponse("Only managers can create or edit drinks.")

        addDrinkForm = addDrink(request.POST)
        if addDrinkForm.is_valid() and not request.POST.get('drink'):
            newDrink = Drink()
            newDrink.name = request.POST.get('name')
            newDrink.price = request.POST.get('price')
            newDrink.instructions = request.POST.get('instructions')
            newDrink.save()
        elif request.POST.get('deleteDrink'):
            drink = request.POST.get('deleteDrink')
            deleteDrink = Drink.objects.filter(name=drink)
            deleteDrink.delete()
        elif request.POST.get('drink') and request.POST.get('name') and request.POST.get('price') \
                and request.POST.get('instructions'):
            drink = request.POST.get('drink')
            editDrink = Drink.objects.filter(name=drink)
            editDrink.delete()
            newDrink = Drink()
            newDrink.name = request.POST.get('name')
            newDrink.price = request.POST.get('price')
            newDrink.instructions = request.POST.get('instructions')
            newDrink.save()
        return HttpResponseRedirect('#')

    else:
        if request.user.user_type != 4:
            return HttpResponseRedirect('../drinks')
        drinkList = Drink.objects.all()
        addDrinkForm = addDrink()
        return render(request, 'drinkEdit.html', {'addDrinkForm': addDrinkForm, 'drinkList': drinkList})


def orderConfirmation(request):
    return render(request, 'orderConfirmation.html')


def createAccount(request):
    if request.method == "POST":
        for u in User.objects.all():
            if u.username == request.POST.get('username'):
                return render(request, 'accountCreation.html',
                              {'error_message': "Username taken, Please choose another"})
        newUser = User()
        newUser.username = request.POST.get('username')
        newUser.first_name = request.POST.get('firstName')
        newUser.last_name = request.POST.get('lastName')
        newUser.email = request.POST.get('email')
        newUser.password = request.POST.get('password')
        newUser.phone_number = request.POST.get('phoneNumber')
        newUser.user_type = request.POST.get('userType')
        createUser = User.objects.create_user(newUser.username, newUser.email, newUser.password)
        createUser.first_name = newUser.first_name
        createUser.last_name = newUser.last_name
        createUser.phone_number = newUser.phone_number
        createUser.user_type = newUser.user_type
        createUser.save()

        if createUser.user_type == "1":
            newPlayer = Player()
            newPlayer.user = createUser

            newPlayer.save()

        if createUser.user_type == "2":
            newSponsor = Sponsor()
            newSponsor.user = createUser
            newSponsor.companyName = ""
            newSponsor.canSponsorTournament = False
            newSponsor.companyName = request.POST.get('companyName')
            newSponsor.save()

        if createUser.user_type == "3":
            newDrinkmeister = Drinkmeister()
            newDrinkmeister.user = createUser
            newDrinkmeister.isAllowedToServeDrinks = False
            newDrinkmeister.save()

        if createUser.user_type == "4":
            newManger = Manager()
            newManger.user = createUser
            newManger.yearsWorked = 0
            newManger.mostMoneyHeld = 0
            newManger.drinksSold = 0
            newManger.totalTournamentsMade = 0
            newManger.save()

        return HttpResponseRedirect('login')


def drinkMeister(request):
    if request.method == "POST":
        if request.user.user_type != 3 and request.user.user_type != 4:
            return HttpResponse("Only Drink Meisters can deliver orders")
        order = Order.objects.get(id=request.POST.get('order'))
        order.served = True
        order.save()
        return HttpResponseRedirect('#')
    else:
        if request.user.is_anonymous or request.user.user_type != 3 and request.user.user_type != 4:
            return HttpResponseRedirect('../login')
        orderList = Order.objects.filter(served=False)
        drinkList = Drink.objects.all()
        return render(request, 'drinkMeister.html', {'orderList': orderList, 'drinkList': drinkList})


def events(request):
    tournaments_list = Tournament.objects.all()
    manager_list = Manager.objects.all()
    context = {'tournaments_list': tournaments_list, "manager_list": manager_list}
    return render(request, "events.html", context)


def manager(request):
    if request.user.is_anonymous or request.user.user_type != 4:
        return HttpResponseRedirect('../login')
    return render(request, "manager.html")


def verification(request):
    sponsors_list = Sponsor.objects.all()
    drinkmeisters_list = Drinkmeister.objects.all()
    context = {'sponsors_list': sponsors_list, 'drinkmeisters_list': drinkmeisters_list}
    return render(request, "verification.html", context)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'


def handler404(request, exception):
    return render(request, '404.html', {})


def tournamentInfo(request, tournamentName):
    tourney = Tournament.objects.get(name=tournamentName)
    context = {"tournament": tourney, "holes": tourney.holes.filter(), "numOfHoles": len(tourney.holes.filter())}
    return render(request, 'tournamentInfo.html', context)


def tournamentEdit(request, tournamentName):
    # This functionality is developmental
    if request.method == "POST":
        tournamentUpdate = Tournament.objects.get(name=tournamentName)
        tournamentUpdate.name = request.POST.get('tournamentName')
        tournamentUpdate.date = request.POST.get('date')
        tournamentUpdate.startTime = request.POST.get('startTime')
        tournamentUpdate.endTime = request.POST.get('endTime')
        for hole in Hole.objects.all():
            if request.POST.get(hole.holeNumber):
                tournamentUpdate.holes.add(hole)
            else:
                tournamentUpdate.holes.remove(hole)
    tourney = Tournament.objects.get(name=tournamentName)
    if request.user.user_type == 4 or (request.user.user_type == 2 and request.user.sponsor == tourney.sponsor):
        if request.method == "POST":
            ...
        context = {"tournament": tourney, "holes": Hole.objects.filter(), "tournamentHoles": tourney.holes.filter()}
        return render(request, 'tournamentEdit.html', context)
    return redirect("tournamentInfo")


def addHoles(request):
    context = {}
    return render(request, 'addHoles.html', context)