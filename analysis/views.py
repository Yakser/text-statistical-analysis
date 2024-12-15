from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from analysis import service


class MakeQuery(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response(
                {"error": "query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = service.process_user_query(user_query)
        return Response(result, status=status.HTTP_200_OK)
