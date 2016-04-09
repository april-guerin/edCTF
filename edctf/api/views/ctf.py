from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from edctf.api.models import Ctf, Challengeboard, Scoreboard
from edctf.api.serializers import CtfSerializer
from edctf.api.serializers.admin import CtfSerializer as AdminCtfSerializer
from edctf.api.permissions import CtfPermission, CtfPermissionDetail
from response import error_response
from rest_framework.views import APIView
from rest_framework.response import Response


class CtfView(APIView):
  """
  Manages ctf requests.
  """
  permission_classes = (CtfPermission,)

  def get(self, request, format=None):
    """
    Gets all ctfs gets the online ctf via GET parameter, i.e. online=true
    """
    if 'online' in request.query_params:
      if request.query_params['online'] == 'true':
        ctfs = Ctf.objects.filter(online=True)
      else:
        ctfs = Ctf.objects.filter(online=False)
    else:
      ctfs = Ctf.objects.all()

    if request.user.is_staff:
      serialized_ctfs = AdminCtfSerializer(ctfs, many=True, context={'request': request})
    else:
      serialized_ctfs = CtfSerializer(ctfs, many=True, context={'request': request})
    return Response({
      'ctfs': serialized_ctfs.data,
    })

  def post(self, request, id=None, format=None):
    """
    Create a new ctf
    """
    if 'ctf' not in request.data or not request.data['ctf']:
      return error_response('CTF not given')

    ctf_data = request.data['ctf']
    if 'name' not in ctf_data or not ctf_data['name']:
      return error_response('CTF name not given', errorfields={'name': True})
    if 'online' not in ctf_data:
      return error_response('CTF online status not given', errorfields={'online': True})

    if len(ctf_data['name']) > 100:
      return error_response('CTF name too long, over 100 characters', errorfields={'name': True})
    name = str(ctf_data['name'])
    online = True if ctf_data['online'] else False

    if Ctf.objects.filter(name__iexact=name).exists():
      return error_response('CTF name already taken', errorfields={'name': True})

    # disable all other online ctfs
    if online:
      online_ctfs = Ctf.objects.filter(online=True)
      for _ctf in online_ctfs:
        if _ctf.online:
          _ctf.online = False
          for team in _ctf.scoreboard.teams.all():
            team.user.is_active = False
            team.user.save()
          _ctf.save()

    try:
      ctf = Ctf.objects.create(name=name, online=online)
    except IntegrityError:
      return error_response('CTF name already taken', errorfields={'name': True})
    challengeboard = Challengeboard.objects.create()
    scoreboard = Scoreboard.objects.create()

    ctf.challengeboard = challengeboard
    ctf.scoreboard = scoreboard
    try:
      ctf.save()
    except IntegrityError:
      return error_response('CTF name already taken', errorfields={'name': True})

    serialized_ctf = CtfSerializer(ctf, many=False, context={'request': request})
    return Response({
      'ctf': serialized_ctf.data,
    })


class CtfViewDetail(APIView):
  """
  Manages ctf by id requests.
  """
  permission_classes = (CtfPermissionDetail,)

  def get(self, request, id, format=None):
    """
    Gets individual ctf via id
    """
    try:
      ctf = Ctf.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('CTF not found')

    if request.user.is_staff:
      serialized_ctf = AdminCtfSerializer(ctf, many=False, context={'request': request})
    else:
      serialized_ctf = CtfSerializer(ctf, many=False, context={'request': request})
    return Response({
      'ctf': serialized_ctf.data,
    })

  def put(self, request, id, format=None):
    """
    Edits a ctf
    """
    try:
      ctf = Ctf.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('CTF not found')

    if 'ctf' not in request.data or not request.data['ctf']:
      return error_response('CTF not given')

    ctf_data = request.data['ctf']
    if 'name' not in ctf_data or not ctf_data['name']:
      return error_response('CTF name not given', errorfields={'name': True})
    if 'online' not in ctf_data:
      return error_response('CTF online status not given', errorfields={'online': True})

    if len(ctf_data['name']) > 100:
      return error_response('CTF name too long, over 100 characters', errorfields={'name': True})

    name = str(ctf_data['name'])
    if ctf.name.lower() != name.lower() and Ctf.objects.filter(name__iexact=name).exists():
      return error_response('CTF name already taken', errorfields={'name': True})
    online = True if ctf_data['online'] else False

    # disable all other online ctfs
    if online:
      online_ctfs = Ctf.objects.exclude(id=ctf.id).filter(online=True)
      for _ctf in online_ctfs:
        if _ctf.online:
          _ctf.online = False
          for team in _ctf.scoreboard.teams.all():
            team.user.is_active = False
            team.user.save()
          _ctf.save()

    ctf.name = name
    ctf.online = online
    try:
      ctf.save()
    except IntegrityError:
      return error_response('CTF name already taken', errorfields={'name': True})

    if request.user.is_staff:
      serialized_ctf = AdminCtfSerializer(ctf, many=False, context={'request': request})
    else:
      serialized_ctf = CtfSerializer(ctf, many=False, context={'request': request})
    return Response({
      'ctf': serialized_ctf.data,
    })

  def delete(self, request, id, format=None):
    """
    Deletes a ctf
    """
    try:
      ctf = Ctf.objects.get(id=id)
    except ObjectDoesNotExist:
      return error_response('CTF not found')
    if ctf.online:
      return error_response('Cannot delete a online ctf')

    ctf.delete()
    return Response({})
