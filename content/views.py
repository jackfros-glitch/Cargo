from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Content, Category
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
import logging
from content.serializers import ContentSerializer
# Create your views here.


logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method="post",
    operation_description="Register a new user",
    request_body=ContentSerializer,
    responses={201: "Content Created successfully", 400: "Bad Request", 500: "Internal Server Error"},
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_content(request):
    try:
        serializer = ContentSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Content validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        serializer.save(owner=user)
        return Response({"message": "Content Created successfully"}, status=status.HTTP_201_CREATED) 
    except Exception as e:
        logger.error(f"An Error occurred while trying to create the Contents {str(e)}", exc_info=True)
        return Response({"message": f"An Error occurred while trying to create the Contents {e}"} ,status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@swagger_auto_schema(
    method="get",
    operation_description="Retrieve all content items for the authenticated user.",
    responses={
        200: ContentSerializer(many=True),
        500: "Internal server error."
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_contents(request):

    try:       
        user = request.user
        contents = Content.objects.filter(owner=user)
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"An Error occurred while trying to get the Contents {str(e)}", exc_info=True)
        return Response({"message": f"An Error occurred while trying to get the Contents {e}"} ,status= status.HTTP_500_INTERNAL_SERVER_ERROR)



@swagger_auto_schema(
    method="get",
    operation_description="Retrieve a specific content item by its ID for the authenticated user.",
    responses={
        200: ContentSerializer,
        404: "Content not found or no permission.",
        500: "Internal server error."
    }
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_content_by_id(request, content_id):
    try:
        content = Content.objects.get(id=content_id, owner=request.user)
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Content.DoesNotExist:
        return Response({'message': 'Content not found or you do not have permission to access this content.'}, 
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"An Error occurred while trying to get the Contents {str(e)}", exc_info=True)
        return Response({"message": f"An Error occurred while trying to get the Content {e}"} ,status= status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method="put",
    operation_description="Update an existing content item by its ID.",
    request_body=ContentSerializer,
    responses={
        204: "Content updated successfully.",
        400: "Bad request - Invalid data.",
        404: "Content not found or no permission.",
        500: "Internal server error."
    }
)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_content(request, content_id):
    try:
        content = Content.objects.get(id=content_id, owner=request.user)
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Content.DoesNotExist:
        return Response({'message': 'Content not found or you do not have permission to update this content.'}, 
                        status=status.HTTP_404_NOT_FOUND)
        

@swagger_auto_schema(
    method="delete",
    operation_description="Delete a specific content item by its ID.",
    responses={
        204: "Content deleted successfully.",
        404: "Content not found or no permission.",
        500: "Internal server error."
    }
)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_content(request, content_id):
    try:
        content = Content.objects.get(id=content_id, owner=request.user)
        content.delete()
        return Response({'message': 'Content deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    except Content.DoesNotExist:
        return Response({'message': 'Content not found or you do not have permission to delete this content.'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"An Error occurred while trying to get the Content {e}"} ,status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    
