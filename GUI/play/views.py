# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from main import game
from utils import common

def index(request):
    template = loader.get_template('play/index.html')
    manager = game()
    state = manager.init_board()
    print state

    context = {'state': state}
    return HttpResponse(template.render(context, request))
