from django.shortcuts import render
from django.http import (
    Http404, 
    HttpResponse, 
    HttpResponseRedirect, 
    JsonResponse, 
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django import forms
import json
from django.contrib.auth.decorators import login_required

from django.forms import ModelForm
from .models import User, Piano, Comment


# ----------------------------------------------------------------
# Forms
# ----------------------------------------------------------------

# ModelForm class to create a piano
class CreatePianoForm(ModelForm):
    class Meta:
        model = Piano
        fields = ['brand', 'price', 'size', 'imageUrl']

    # Because we can't add styling directly to our form in the HTML
    # we can take care of that here.  You can find this in the Django
    # docs.  Remember our discussions on inheritance.  Well, here it is.
    def __init__(self, *args, **kwargs):
        super(CreatePianoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# Form from 'Form' class
class CreatePianoFormsForm(forms.Form):

    brand = forms.CharField(max_length=48)
    price = forms.DecimalField(max_digits=16, decimal_places=0)
    size = forms.IntegerField(min_value=50)
    imageUrl = forms.URLField(label="Image URL:")

    brand.widget.attrs.update({"class": "form-control"})
    price.widget.attrs.update({"class": "form-control"})
    size.widget.attrs.update({"class": "form-control"})
    imageUrl.widget.attrs.update({"class": "form-control"})

    # def __init__(self, *args, **kwargs):
    #     super(CreatePianoFormsForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs["class"] = "form-control"

  
# ----------------------------------------------------------------
# Views
# ----------------------------------------------------------------

# Listing all pianos
def index(request):
    pianos = Piano.objects.all().order_by("brand")
    return render(request, "piano_app/index.html", {"pianos": pianos})


# Add a piano w/ ModelForm
@login_required
def add_piano(request):
    if request.method == "POST":
        # Get a user object, because there's a foreign key and I don't want to use a hidden field when I can get the user from the request object
        user = User.objects.get(pk=request.user.id)
       
       # Populate the form with the request object
        form = CreatePianoForm(request.POST)
        
        # Server side validation
        if form.is_valid():
            # Don't commit yet because you need to take care of the foreign key
            piano = form.save(commit=False)
            #Add the user object as the foreign key reference
            piano.owner = user
            # Now save form and new model object
            piano.save()

            messages.success(request, "Your piano has been added.")

            # If successful, redirect
            return HttpResponseRedirect(reverse("index"))

        return render(request, "piano_app/add_piano.html", {"form": form})

    return render(request, "piano_app/add_piano.html", {"form": CreatePianoForm()})


# Add a piano Django forms
# Need to create and save the model instance
@login_required
def add_piano2(request):
    if request.method == "POST":
        # Binding data to the form
        form = CreatePianoFormsForm(request.POST)
        # Return user object of logged-in user
        user = User.objects.get(pk=request.user.id)
        # Extract data from bound form for new model object
        if form.is_valid():
            brand = form.cleaned_data["brand"]
            price = form.cleaned_data["price"]
            size = form.cleaned_data["size"]
            image = form.cleaned_data["imageUrl"]
            piano = Piano(brand=brand, price=price, size=size, imageUrl=image, owner=user)
            piano.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "piano_app/add_piano2.html", {"form": CreatePianoFormsForm()})
    

# Add a piano functionality w/ HTML
@login_required
def add_piano1(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        brand = request.POST["brand"]
        price = request.POST["price"]
        size = request.POST["size"]
        url = request.POST["imageUrl"]
        new_piano = Piano(brand=brand, price=price, size=size, imageUrl=url, owner=user)
        try:
            new_piano.save()
        except IntegrityError:
            return render(request, "piano_app/add_piano1.html", {"msg": "Did not save piano"})
        return HttpResponseRedirect(reverse("index"))
    return render(request, "piano_app/add_piano1.html")


#View piano details
def piano_detail(request, piano_id):
    if request.user:
        piano = get_object_or_404(Piano, pk=piano_id)
        # try:
        #     piano = Piano.objects.get(pk=pk)
        # except: Piano.DoesNotExist:
        #     raise Http404("No piano model matches")
        return render(request, "piano_app/piano_detail.html", {"piano": piano})


# Asynchronous voting for a piano
@login_required
def vote(request, piano_id):
    if request.method == "PUT":
        try:
            piano = Piano.objects.get(pk=piano_id)
        except Piano.DoesNotExist:
            return JsonResponse({"error": "Piano not found"})

        if request.user.username == piano.owner.username:
            return JsonResponse({"msg": "Owner can't vote on own item"})
    
        # Update piano post
        # Parse a JSON string and turn it into a Python dictionary
        data = json.loads(request.body)
        # Now we can extract the data like we're used to doing with regular python data types
        vote = data["content"]
        # Change the piano instance vote property
        piano.vote += vote
        # Save the piano instance
        piano.save()
        # Send the updated vote count to the front end
        return JsonResponse({
            "content": piano.vote
        })


@login_required
def delete_piano(request, piano_id):
    if request.method == 'DELETE':
        piano = get_object_or_404(Piano, id=piano_id)

        # Check if the current user is the piano owner
        if piano.owner.id != request.user.id:
            return HttpResponseForbidden("You don't have permission to delete this piano")

        piano.delete()
   
        return JsonResponse({"success": True, "message": "Piano deletion successfull"})
    # Returns a 405 method not allowed
    return HttpResponseNotAllowed(["DELETE"])


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        # email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "piano_app/login.html", {
                "message": "Invalid username and/or password."})
    else:
        return render(request, "piano_app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
       
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "piano_app/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "piano_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "piano_app/register.html")

