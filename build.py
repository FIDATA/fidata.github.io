﻿#!/usr/bin/env python3# -*- coding, utf-8 -*-# Python script to regenerate FIDATA Website whenever new commit is made# Copyright © 2014  Basil Peace# This file is part of code for generation of FIDATA Website.# This work is licensed under the Creative Commons# Attribution-ShareAlike 3.0 Unported License. A copy of this license is# located in LICENSE.code.txt. If you haven't received that file,# visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter# to Creative Commons, 444 Castro Street, Suite 900, Mountain View,# California, 94041, USA.from subprocess import check_call, check_outputimport sys#from os.path import getmtime#from datetime import datetime, timedelta# Getting last commit messagecommitMsg = check_output(['git', 'log',	'--max-count=1',	'--pretty=%B',]).decode()# Testing tags in commit messagedelim = commitMsg.find(':')commitTags = commitMsg[0:delim].split(',')if not ('CODE' in commitTags or 'CONTENT' in commitTags) or 'OUTPUT' in commitTags:	exit(0)# This code tries to find and run Ruby exec depending on platformdef runRubyExecutable(exec_name, args = [], cwd = None):	if sys.platform.startswith('win'):		exec_names = [exec_name + '.bat']	# TODO: I don't know the proper platform name for MinGW/MSYS	#  I make some assumptions	elif sys.platform.startswith('cygwin') or sys.platform.startswith('msys') or sys.platform.startswith('mingw'):		exec_names = [exec_name + '.bat', exec_name]	else:		exec_names = [exec_name]	i = 0	while True:		try:			check_call([exec_names[i]] + args, cwd = cwd)			break		except FileNotFoundError:			i += 1			if i >= len(exec_names): # Nothing was found				raise#bundle_update_threshold = timedelta(days = 1)#try:#	need_bundle_update = (datetime.today() - datetime.fromtimestamp(getmtime('Gemfile.lock'))) > bundle_update_threshold#except OSError:#	need_bundle_update = True##if need_bundle_update:runRubyExecutable('bundle', ['update'])# Running nanocrunRubyExecutable('nanoc', cwd = 'src')# Adding changes to the indexcheck_call(['git', 'add',	'-A',])# CommitingcommitMsg = 'OUTPUT' + commitMsg[delim:]check_call(['git', 'commit',	'-m', commitMsg,])# Pushingcheck_call(['git', 'push'])