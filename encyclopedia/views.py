import random
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django import forms
import markdown2 as md
from fuzzywuzzy import process
import re

from . import util

class NewTaskForm(forms.Form):
	title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Your Title', 'id':'title', 'autocomplete':'off'}))
	discriptions = forms.CharField(label="", widget=forms.Textarea(attrs={'id':'text', 'placeholder': 'Your description'}))

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
	if request.method == "POST":
		form = NewTaskForm(request.POST)
		if form.is_valid():
			userTitle = form.cleaned_data['title']
			userDisrp = form.cleaned_data['discriptions']

			if userTitle in util.list_entries():
				mess = "Title already exits. Pick another title"
				return render(request, "encyclopedia/create.html", {'message':mess, 'form': NewTaskForm()})
			else:
				util.save_entry(userTitle, userDisrp)
				data = util.get_entry(userTitle)
				finalData = md.markdown(data)
				return redirect('tasks:data', id=userTitle)
	return render(request, "encyclopedia/create.html", {'form': NewTaskForm()})

def data(request, id):

	try:
		value = util.get_entry(id)
		request.session['id'] = id
		finalData = md.markdown(value)
		return render(request, "encyclopedia/data.html", {'id':finalData, 'title': id})
	except:
		message = "Page not found "
		return render(request, "encyclopedia/data.html", {'message':message})


def ran(request):
	data = util.list_entries()
	val = random.choice(data)
	return redirect('tasks:data', id=val)

def edit(request):
	if request.method == "POST":
		id_name = request.POST['idd']
		getContent = request.POST['val']
		util.save_entry(id_name, getContent)
		return redirect('tasks:data', id=id_name)
	id = request.session['id']
	content = util.get_entry(id)
	print(content)
	return render(request, "encyclopedia/edit.html", {'id': id, 'content':content})

def check(request):
	if request.method == "POST":
		data = request.POST['q']
		for i in util.list_entries():
			checVal = re.match(data, i)
			print(i)
			if checVal:
				return redirect('tasks:data', id=i)
		result = process.extract(data, util.list_entries(), limit=3)
		newList = []
		for i in result:
			newList.append(i[0])
		return render(request, "encyclopedia/index.html", {'entries':newList})