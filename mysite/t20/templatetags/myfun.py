#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import template

register = template.Library()
@register.simple_tag
def response_head(head):
    if head[0]=="this is a response":
        print "before",len(head)
        head.pop(0)
        print "after", len(head)
        return "<p class='ret'>this is a response</p>"

    else:
        return ""