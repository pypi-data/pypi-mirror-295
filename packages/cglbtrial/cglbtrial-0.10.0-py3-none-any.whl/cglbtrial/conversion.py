# -*- coding: utf-8 -*-


def fahrenheit_2_kelvin(fahrenheit):
    '''
    takes a temperature `temp` in fahrenheit and returns it in Kelvin
    '''

    kelvin = 5./9. * (fahrenheit - 32.) + 273.15

    return kelvin


