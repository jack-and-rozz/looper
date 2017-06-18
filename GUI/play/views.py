# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from main import game

def index(request):
    template = loader.get_template('play/index.html')
    print 
    state = game().start_game()


    context = {'state': state}
    return HttpResponse(template.render(context, request))
