from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ExpenseModel
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ExpenseListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = ExpenseModel.objects.filter(user = request.user)
        serializer = ExpenseSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class ExpenseRetrieveUpdateDestroyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            expense = ExpenseModel.objects.get(pk=pk,user=request.user)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except ExpenseModel.DoesNotExist:
            return Response({"error":"Expense not found"},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,pk):
        try:
            expense = ExpenseModel.objects.get(pk=pk,user=request.user)
        except ExpenseModel.DoesNotExist:
            return Response({"error":"Expense not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSerializer(expense,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        try:
            expense = ExpenseModel.objects.get(pk=pk,user=request.user)
        except ExpenseModel.DoesNotExist:
            return Response({"error":"Expense not found"},status=status.HTTP_404_NOT_FOUND)
        expense.delete()
        return Response({"message": "Expense deleted successfully"},status=status.HTTP_204_NO_CONTENT)
