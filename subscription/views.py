from datetime import timedelta
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Subscription, SubscriptionPlan
from .serializers import SubscriptionPlanSerializer, SubscriptionSerializer
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import logging



logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method="post",
    operation_description="Create a new subscription for the authenticated user.",
    request_body=SubscriptionSerializer,
    responses={
        201: "Subscription created successfully.",
        400: "Bad request - Invalid data.",
        409: "Conflict - User already has an active subscription.",
        500: "Internal server error."
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_subscription(request):
    try:
        serializer = SubscriptionSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f'{serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if Subscription.objects.filter(user=request.user, end_date__gte=timezone.now()).exists():
            logger.error("User already has an active subscription")
            return Response(
                {"message": "User already has an active subscription."},
                status=status.HTTP_409_CONFLICT
            )
        
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"An Error Occured while trying to create a subscription for the user. : {str(e)}", exc_info=True)
        return Response(
                {"message": "An Error Occured while trying to create a subscription for the user."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        



@swagger_auto_schema(
    method='get',
    operation_description="Retrieve all subscriptions",
    responses={ 200: SubscriptionSerializer(many=True),
                500: "Internal Server Error"
               },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_all_subscriptions(request):
    try:
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"An Error Occured while trying to get all subscriptions : {str(e)}", exc_info=True)
        return Response({"message": "An Error Occured while trying to get all subscriptions"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


@swagger_auto_schema(
    method="get",
    operation_description="Retrieve a user's subscription by ID.",
    responses={
        200: openapi.Response("Subscription retrieved successfully", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "plan": openapi.Schema(type=openapi.TYPE_INTEGER),
                "start_date": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
                "end_date": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
                "auto_renew": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        )),
        404: openapi.Response("Subscription not found"),
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_subscription_by_id(request, sub_id):
    try:
        subscription = Subscription.objects.get(user=request.user, id=sub_id)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=200)
    except Subscription.DoesNotExist:
        return Response({"error": "Subscription not found"}, status=404)
    except Exception as e:
        logger.error(f"An Error Occured while trying to get the subscription with id {sub_id} : {str(e)}", exc_info=True)
        return Response({"message": "An Error Occured while trying to get the subscription"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
       

@swagger_auto_schema(
    method="get",
    operation_description="Retrieve all available subscription plans.",
    responses={
        200: SubscriptionPlanSerializer(many=True),
        500: "Internal server error"
    }
)

@cache_page(60 * 15, key_prefix="sub_plans")
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_subscription_plans(request):
    try:
        plans = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        
        
        
@swagger_auto_schema(
    method="post",
    operation_description="Renew a user's subscription if it meets renewal conditions.",
    responses={
        200: openapi.Response("Subscription renewed successfully", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING),
                "new_end_date": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
            },
        )),
        400: openapi.Response("Subscription not eligible for renewal yet"),
        404: openapi.Response("Subscription not found"),
    }
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def renew_subscription(request, sub_id):
    
    try:
        user = request.user
        subscription = Subscription.objects.get(user=user, id=sub_id)

        
        time_left = subscription.end_date - timezone.now()

        renewal_conditions = {
            'monthly': timedelta(days=7),
            'quarterly': timedelta(days=30),
            'bi_yearly': timedelta(days=30),
            'yearly': timedelta(days=30),
        }

        renewal_window = renewal_conditions.get(subscription.plan.name.lower())

        
        if time_left > renewal_window:
            return Response({"error": "Subscription not eligible for renewal yet"}, status=status.HTTP_400_BAD_REQUEST)

        subscription.end_date += timedelta(days=subscription.plan.duration_days)
        subscription.save()

        return Response({
            "message": "Subscription renewed successfully",
            "new_end_date": subscription.end_date,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"An Error Occured while trying to renew the subscription with id {sub_id} : {str(e)}", exc_info=True)
        return Response({"message": "An Error Occured while trying to renew the subscription"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@swagger_auto_schema(
    method="delete",
    operation_description="Delete a user's subscription by ID.",
    responses={
        204: openapi.Response("Subscription deleted successfully"),
        404: openapi.Response("Subscription not found"),
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_subscription(request, sub_id):
    try:
        subscription = Subscription.objects.get(user=request.user, id=sub_id)
        subscription.delete()
        return Response({"message": "Subscription deleted successfully"}, status=204)
    except Subscription.DoesNotExist:
        logger.error(f"Subscription with id : {sub_id} not found")
        return Response({"message": "Subscription not found"}, status=404)
    except Exception as e:
        logger.error(f"An Error Occured while trying to delete the subscription with id {sub_id} : {str(e)}", exc_info=True)
        return Response({"message": "An Error Occured while trying to delete the subscription"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
    