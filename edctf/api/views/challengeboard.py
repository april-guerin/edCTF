from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from edctf.api.models import challengeboard, category, challenge
from edctf.api.serializers import challengeboard_serializer, category_serializer, challenge_serializer


class challengeboard_view(APIView):
  """
  Manages challengeboard requests
  """
  permission_classes = (IsAuthenticated,)

  def get(self, request, id=None, format=None):
    """
    Gets all challengeboards or gets one challengeboard via
    challengeboards/:id.
    """
    # If challengeboard id was requested, return that challengeboard
    # else return list of all challengeboards in the database.
    if id:
      # Retrieve and serialize the requested challengeboard data.
      challengeboards = challengeboard.objects.filter(id=id)
      challengeboards_serializer = challengeboard_serializer(challengeboards, many=True, context={'request': request})

      # Retrieve and serialize the categories in the challengeboard.
      categories = category.objects.filter(challengeboard=challengeboards.first())
      categories_serializer = category_serializer(categories, many=True, context={'request': request})

      # Retrieve and serialize the challenges in each category.
      challenges = []
      for cat in categories:
        challenges += challenge.objects.filter(category=cat)
      challenges_serializer = challenge_serializer(challenges, many=True, context={'request': request})

      # Return the serialized data.
      return Response({
          'challengeboards': challengeboards_serializer.data,
          'categories': categories_serializer.data,
          'challenges': challenges_serializer.data,
      })
    else:
      # Retrieve and serialize the requested challengeboard data.
      challengeboards = challengeboard.objects.all()
      serializer = challengeboard_serializer(challengeboards, many=True, context={'request': request})

      # Return the serialized data.
      return Response({
          'challengeboards': serializer.data,
      })
