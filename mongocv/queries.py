#!/usr/bin/python


def normalquery(fieldname, operator, condvalue):
    res = dict()
    insidecond = dict()
    insidecond[operator] = condvalue
    res[fieldname] = insidecond
    return res


def complexquery(fieldname, tuplelst):
    res = dict()
    insidecond = dict()
    for key, value in tuplelst:
        insidecond[key] = value
    res[fieldname] = insidecond
    return res


def lstquery(operator, condlst):
    res = dict()
    res[operator]=condlst
    return res


