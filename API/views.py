from .serializers import *

from django.shortcuts import get_object_or_404

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

import json

@api_view(["GET"])
def commandRequest(request):
	if request.method == 'GET':
		serializer = CommandSerializer(data=request.GET)
		if serializer.is_valid():
			cmd = request.GET.get('cmd')
			if cmd is None:
				return JsonResponse({'error': 'cmd is blank'}, status=400)
			elif len(cmd) == 0:
				return JsonResponse({'error': 'cmd is blank'}, status=400)

			comandos = cmd.split(' | ')
			## Separacion de direccionamiento >> > < <<
			data = {}
			results = 0
			for command in comandos:
				results += 1
				data_cmd = {}
				## Modo de operacion
				if '&' in command:
					data_cmd['modo'] = 'Subordinated'
					command = command[0:len(command)-2]
				else:
					data_cmd['modo'] = 'Normal'

				## Redireccionamiento de entrada
				redirect_in = False
				if "<<" in command:
					redirect_in = True
					in_redirect = command.split("<<")
					index = command.index("<<")
				elif "<" in command:
					redirect_in = True
					in_redirect = command.split("<")
					index = command.index("<")

				if redirect_in:
					data_cmd['in_redirect'] = True
					data_cmd['in_redirect_to'] = in_redirect.pop().replace(" ", "")
					command = command[0:index-1]
				else:
					data_cmd['in_redirect'] = False
					data_cmd['in_redirect_to'] = None

				## Redireccionamiento de salida
				redirect_out = False
				if ">>" in command:
					redirect_out = True
					out_redirect = command.split(">>")
					index = command.index(">>")
				elif ">" in command:
					redirect_out = True
					out_redirect = command.split(">")
					index = command.index(">")

				if redirect_out:
					data_cmd['out_redirect'] = True
					data_cmd['out_redirect_to'] = out_redirect.pop().replace(" ", "")
					command = command[0:index-1]
				else:
					data_cmd['out_redirect'] = False
					data_cmd['out_redirect_to'] = None

				## Comando principal
				command_space = command.split(" ")
				data_cmd['cmd'] = command_space[0]

				options = {}
				count_options = 0
				parameters = {}
				count_parameters = 0
				for pos in range(1,len(command_space)):
					if "-" in command_space[pos] or "+" in command_space[pos]:
						count_options += 1
						options[count_options] = command_space[pos].replace("-", "").replace("+","").replace(" ","")
					else:
						count_parameters += 1
						parameters[count_parameters] = command_space[pos].replace(" ","")

				## Opciones
				data_cmd['options'] = options
				data_cmd['num_options'] = count_options

				## Parametros
				data_cmd['parameters'] = parameters
				data_cmd['num_parameters'] = count_parameters

				data[results] = data_cmd

			data["results"] = results
			return JsonResponse(data, safe=False)
		return JsonResponse({'error': 'No valid data'}, status=400)
	return JsonResponse({'error': 'No valid method'}, status=400)
