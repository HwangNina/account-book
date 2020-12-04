from django.urls import path
from contract.views import ContractDetailView, ContractListView,ContractPostView

urlpatterns = [
    path('/detail/<int:contract_id>', ContractDetailView.as_view()),
    path('/list', ContractListView.as_view()),
    path('/post',ContractPostView.as_view())
]