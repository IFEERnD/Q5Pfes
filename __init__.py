# -*- coding: utf-8 -*-
# --------------------------------------------------------
#    __init__ - Q5PFES init file
#
#    begin                : 01/07/2022
#    copyright            : 2022 by Institute for Forest Ecoglogy and Environment
#    email                : info@ifee.edu.vn
#   
# --------------------------------------------------------

def classFactory(iface):
	from .q5pfes_menu import q5pfes_menu
	return q5pfes_menu(iface)
