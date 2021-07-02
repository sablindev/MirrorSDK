# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: E:/Documents/maya/2018/scripts\MirrorSDK.py
# Compiled at: 2018-06-18 08:42:33

# Длязапускаиспользовать
# import MirrorSDKExtended
# MirrorSDK.MirrorSDKUIExtended()


# TODO: сделать копирование всех управляемых ключей

import pymel.core as pm
import maya.cmds as mc
import sys


def MirrorSDKUIExtended():
    TitleWindow = 'MirrorSDK (Extended by EEGames v.1.0)'
    if pm.window(TitleWindow, q=True, ex=True):
        pm.deleteUI(TitleWindow)
    pm.window(TitleWindow)
    pm.showWindow()
    pm.columnLayout(adj=True)
    pm.separator(st=None, h=10)
    pm.text(l=TitleWindow, bgc=(0.1, 0.5, 0.5))
    pm.textFieldGrp('search', l='Search:', tx='_L')
    # pm.radioButtonGrp('selt', nrb=2, l='Type:', la2=(
    #     'Translate', 'BlendShape (not work)'), sl=1, en2=False, cc='changeUI')
    # pm.separator(st=None, h=10)
    pm.text(l='Отметить для исправления поведения', bgc=(0.1, 0.1, 0.1))
    pm.separator(st=None, h=5)
    pm.checkBoxGrp('checkbox2', ncb=3, l='Ось перемещения:',
                   la3=('X', 'Y', 'Z'))
    pm.checkBoxGrp('checkbox3', ncb=3, l='Ось вращения:', la3=('X', 'Y', 'Z'))

    pm.textFieldButtonGrp('getCtrl1', l='Исходный ктрл (откуда):',
                          tx='', bl='Получить значение', bc=getCtrl1c)
    pm.textFieldButtonGrp('getCtrl2', l='Целевой ктрл (куда):',
                          bl='Получить значение', bc=getCtrl2c)
    pm.textFieldButtonGrp(
        'getAttribute1', l='Атрибут управления:', bl='Получить значение', bc=getAttribute1c)
    pm.checkBoxGrp('checkbox4', ncb=1, l='Инверт. поведение:',
                   l1='(изменяет поведение управляющего ключа на противоположное)')
    pm.textFieldButtonGrp('getCtrlgrp1', l='Управляемые объекты:',
                          bl='Получить значение', bc=getCtrlgrp1c)
    pm.floatFieldGrp('getfloat', nf=2, l='Значения для копирования', v1=0, v2=90
                     )
    pm.separator(st=None, h=10)
    pm.button('button1', l='После заполнения полей завершите этот шаг нажатием данной кнопки, затем настройте управляемые объекты.', c=SDK1, bgc=(0.0,
                                                                                                                                                  0.3,
                                                                                                                                                  0.1))
    pm.separator(st=None, h=10)
    pm.button('button2', l='Кликнуть по завершению настройки управляемых объектов.\n Это завершает зеркальную или не зеркальную операцию.', c=SDK2, bgc=(0,
                                                                                                                                                         0.4,
                                                                                                                                                         0.1))
    return


def getCtrl1c():
    getCtrl1c_list = pm.ls(sl=True)
    if len(getCtrl1c_list) > 1:
        pm.error('Only one object can be selected')
    pm.textFieldButtonGrp('getCtrl1', e=True, tx=getCtrl1c_list[0])


def getCtrl2c():
    getCtrl2c_list = pm.ls(sl=True)
    if len(getCtrl2c_list) > 1:
        pm.error('Only one object can be selected')
    pm.textFieldButtonGrp('getCtrl2', e=True, tx=getCtrl2c_list[0])


def getAttribute1c():
    mainChannelBox = pm.channelBox('mainChannelBox', q=True, sma=True)
    if len(mainChannelBox) > 1:
        pm.error('Only one attribute can be selected')
    pm.textFieldButtonGrp('getAttribute1', e=True, tx=mainChannelBox[0])


def getCtrlgrp1c():
    # Вот ради списка выделенных элементов тут подгружена библиотека майки? Ужас.
    pm.textFieldButtonGrp('getCtrlgrp1', e=True, tx=(',').join(mc.ls(sl=True)))


def SDK1(*O0OOOOO00O000O0O0):
    first_controller = pm.textFieldButtonGrp('getCtrl1', q=True, tx=True)
    second_controller = pm.textFieldButtonGrp('getCtrl2', q=True, tx=True)
    text_field_of_list_driven_elems = pm.textFieldButtonGrp(
        'getCtrlgrp1', q=True, tx=True)
    list_driven_elems = text_field_of_list_driven_elems.split(',')
    # TODO: рассмотреть, как добавить тут список управляющих атрибутов
    driver_attribute = pm.textFieldButtonGrp(
        'getAttribute1', q=True, tx=True)
    # TODO: сделать кнопку смены поведения второго управляющего объекта
    driver_attribute_invertation = - \
        1 if pm.checkBoxGrp('checkbox4', q=True, v1=True) else 1
    min_value = pm.floatFieldGrp('getfloat', q=True, v1=True)
    max_value = pm.floatFieldGrp('getfloat', q=True, v2=True)
    list_of_all_attributes = ['tx', 'ty', 'tz',
                              'rx', 'ry', 'rz', 'sx', 'sy', 'sz']

    pm.setAttr(first_controller + '.' +
               driver_attribute, min_value)

    for driven_elem in list_driven_elems:
        for elem_from_list_of_all_attributes in list_of_all_attributes:
            pm.setDrivenKeyframe(driven_elem + '.' + elem_from_list_of_all_attributes,
                                 cd=second_controller + '.' + driver_attribute)
            # NOTE: тут можно заменить управляющий атрибут на несколько

    pm.setAttr(first_controller + '.' +
               driver_attribute, max_value)


def SDK2(*OO000OOO000OO0000):
    first_controller = pm.textFieldButtonGrp('getCtrl1', q=True, tx=True)
    second_controller = pm.textFieldButtonGrp('getCtrl2', q=True, tx=True)
    text_field_of_list_driven_elems = pm.textFieldButtonGrp(
        'getCtrlgrp1', q=True, tx=True)
    text_field_of_list_driven_elems = text_field_of_list_driven_elems.split(
        ',')
    driver_attribute = pm.textFieldButtonGrp(
        'getAttribute1', q=True, tx=True)
    min_value = pm.floatFieldGrp('getfloat', q=True, v1=True)
    max_value = pm.floatFieldGrp('getfloat', q=True, v2=True)
    list_of_all_attributes = ['tx', 'ty', 'tz',
                              'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    text_from_search_field = pm.textFieldGrp('search', q=True, tx=True)

    l2r_or_r2l_replacer = text_from_search_field.replace('L', 'R') if ('_L_').find(
        text_from_search_field) >= 0 else text_from_search_field.replace('R', 'L')

    mirored_first_controller = first_controller.replace(text_from_search_field, l2r_or_r2l_replacer) if first_controller.find(
        text_from_search_field) >= 0 else first_controller.replace(l2r_or_r2l_replacer, text_from_search_field)

    mirrored_second_controller = second_controller.replace(text_from_search_field, l2r_or_r2l_replacer) if first_controller.find(
        text_from_search_field) >= 0 else second_controller.replace(l2r_or_r2l_replacer, text_from_search_field)

    mirrored_driver_attribute = driver_attribute.replace(text_from_search_field, l2r_or_r2l_replacer) if first_controller.find(
        text_from_search_field) >= 0 else driver_attribute.replace(l2r_or_r2l_replacer, text_from_search_field)

    if pm.objExists(mirored_first_controller):
        extx = - \
            1 if pm.checkBoxGrp('checkbox2', q=True, v1=True) else 1
        exty = - \
            1 if pm.checkBoxGrp('checkbox2', q=True, v2=True) else 1
        extz = - \
            1 if pm.checkBoxGrp('checkbox2', q=True, v3=True) else 1
        exrx = - \
            1 if pm.checkBoxGrp('checkbox3', q=True, v1=True) else 1
        exry = - \
            1 if pm.checkBoxGrp('checkbox3', q=True, v2=True) else 1
        exrz = - \
            1 if pm.checkBoxGrp('checkbox3', q=True, v3=True) else 1

        pm.setAttr(mirored_first_controller + '.' +
                   mirrored_driver_attribute, min_value)

        for elem_from_text_field_of_list_driven_elems in text_field_of_list_driven_elems:
            mirrored_elem_from_text_field_of_list_driven_elems = elem_from_text_field_of_list_driven_elems.replace(text_from_search_field, l2r_or_r2l_replacer) if first_controller.find(
                text_from_search_field) >= 0 else elem_from_text_field_of_list_driven_elems.replace(l2r_or_r2l_replacer, text_from_search_field)
            for elem_from_list_of_all_attributes in list_of_all_attributes:
                pm.setDrivenKeyframe(mirrored_elem_from_text_field_of_list_driven_elems + '.' + elem_from_list_of_all_attributes,
                                     cd=mirrored_second_controller + '.' + mirrored_driver_attribute)

        pm.setAttr(mirored_first_controller + '.' +
                   mirrored_driver_attribute, max_value)

        for elem_from_text_field_of_list_driven_elems in text_field_of_list_driven_elems:
            mirrored_elem_from_text_field_of_list_driven_elems = elem_from_text_field_of_list_driven_elems.replace(text_from_search_field, l2r_or_r2l_replacer) if first_controller.find(
                text_from_search_field) >= 0 else elem_from_text_field_of_list_driven_elems.replace(l2r_or_r2l_replacer, text_from_search_field)

            mirrored_first_controller_translate = pm.getAttr(
                elem_from_text_field_of_list_driven_elems + '.translate')
            mirrored_first_controller_rotate = pm.getAttr(
                elem_from_text_field_of_list_driven_elems + '.rotate')
            mirrored_first_controller_scale = pm.getAttr(
                elem_from_text_field_of_list_driven_elems + '.scale')

            pm.setAttr(mirrored_elem_from_text_field_of_list_driven_elems + '.translate', (extx *
                       mirrored_first_controller_translate[0], exty * mirrored_first_controller_translate[1], extz * mirrored_first_controller_translate[2]))
            pm.setAttr(mirrored_elem_from_text_field_of_list_driven_elems + '.rotate', (exrx *
                       mirrored_first_controller_rotate[0], exry * mirrored_first_controller_rotate[1], exrz * mirrored_first_controller_rotate[2]))
            pm.setAttr(mirrored_elem_from_text_field_of_list_driven_elems + '.scale', (
                       mirrored_first_controller_scale[0],  mirrored_first_controller_scale[1], mirrored_first_controller_scale[2]))

        for elem_from_text_field_of_list_driven_elems in text_field_of_list_driven_elems:
            mirrored_elem_from_text_field_of_list_driven_elems = elem_from_text_field_of_list_driven_elems.replace(text_from_search_field, l2r_or_r2l_replacer) if first_controller.find(
                text_from_search_field) >= 0 else elem_from_text_field_of_list_driven_elems.replace(l2r_or_r2l_replacer, text_from_search_field)
            for elem_from_list_of_all_attributes in list_of_all_attributes:
                pm.setDrivenKeyframe(mirrored_elem_from_text_field_of_list_driven_elems + '.' + elem_from_list_of_all_attributes,
                                     cd=mirrored_second_controller + '.' + mirrored_driver_attribute)

        print('Mirror SDK completion!!!')

    else:
        for elem_from_text_field_of_list_driven_elems in text_field_of_list_driven_elems:
            for elem_from_list_of_all_attributes in list_of_all_attributes:
                pm.setDrivenKeyframe(elem_from_text_field_of_list_driven_elems + '.' + elem_from_list_of_all_attributes,
                                     cd=second_controller + '.' + driver_attribute)

        print('Non mirror drive completion!!!')
