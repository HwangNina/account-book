from django.urls import path
from contract.views import ContractDetailView, ContractListView

urlpatterns = [
    path('/detail', ContractDetailView.as_view()),
    path('/detail/<int:contract_id>', ContractDetailView.as_view()),
    path('/list', ContractListView.as_view()),
]