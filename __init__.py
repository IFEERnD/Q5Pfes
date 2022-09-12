# -*- coding: utf-8 -*-
# --------------------------------------------------------
#    __init__ - V5PFES init file
#
#    begin                : 20/03/2020
#    copyright            : 2020 by Institute for Forest Ecoglogy and Environment
#    email                : info@ifee.edu.vn
#   
# --------------------------------------------------------

def classFactory(iface):
	from .v5pfes_menu import v5pfes_menu
	return v5pfes_menu(iface)
