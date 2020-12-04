import json
import jwt_utils

from django.views   import View
from django.http    import JsonResponse

from contract.models    import Category, Subcategory, Process, ProcessStatus, Contract
from company.models     import Group,Company,Representative
from employee.models    import Employee

# Create your views here.
class ContractPostView(View):
    def get(self, request):
        subcategory_list = [{'category_name':subcategory.category.name,'subcategory_id':subcategory.id, 'subcategory_name':subcategory.name} 
                            for subcategory in Subcategory.objects.select_related('category').all()]
        employee_list    = [{'id':employee.id, 'name':employee.name} 
                            for employee in Employee.objects.all()]
        company_list     = [{'group_name':company.group.name,'company_id':company.id, 'company_name':company.name, 
                            'representatives':[{'id':repre.id,'name':repre.name} for repre in company.representative_set.all()]} 
                            for company in Company.objects.select_related('group').prefetch_related('representative_set').all()]
        status_list      = [{'process_name':status.process.process,'status_id':status.id, 'status_name':status.status} 
                            for status in ProcessStatus.objects.select_related('process').all()]

        return JsonResponse({
            'subcategories' : subcategory_list,
            'companies' : company_list,
            'employees' : employee_list,
            'statuses' : status_list
        },status=200)

    #@jwt_utils.signin_decorator
    def post(self, request):
        try:
            #employee_id = request.employee.id
            employee_id = 1

            data = json.loads(request.body)

            target_status           = ProcessStatus.objects.get(id = data['status'])
            target_subcategory      = Subcategory.objects.get(id=data['subcategory'])
            target_company          = Company.objects.get(id=data['company'])
            target_representative   = Representative.objects.get(id=data['representative'])

            contract_field_list = [field.name for field in Contract._meta.get_fields()]
            additional_infos    = ['category_content','revenue','issue_date','memo']
            for index in range(0, len(additional_infos)):
                if additional_infos[index] in data:
                    additional_infos[index] = data[additional_infos[index]]
                else:
                    additional_infos[index] = None

            new_contract = Contract(
                status           = target_status,
                subcategory      = target_subcategory,
                company          = target_company,
                representative   = target_representative,
                employee         = Employee.objects.get(id=employee_id),
                category_content = additional_infos[0],
                revenue          = additional_infos[1],
                issue_date       = additional_infos[2],
                memo             = additional_infos[3]
            )

            new_contract.save()

            return JsonResponse(
                {
                    "process": new_contract.status.process.process,
                    "status": new_contract.status.status,
                    "category":new_contract.subcategory.category.name,
                    "subcategory": new_contract.subcategory.name,
                    "category_content": new_contract.category_content,
                    "group": new_contract.company.group.name,
                    "company": new_contract.company.name,
                    "representative": new_contract.representative.name,
                    "representative_phone": new_contract.representative.phone_num,
                    "representative_email": new_contract.representative.email,
                    "employee": new_contract.employee.name,
                    "revenue": new_contract.revenue,
                    "issue_date": new_contract.issue_date,
                    "memo": new_contract.memo
                }, status=201
            )
        
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        
        except ValueError as e:
            return JsonResponse({"message": f"VALUE_ERROR:{e}"}, status=400) 

    
class ContractDetailView(View):
    def get(self, request, contract_id):

        target_contract = Contract.objects.get(id = contract_id)

        return JsonResponse(
            {
                "process": target_contract.status.process.process,
                "status": target_contract.status.status,
                "category":target_contract.subcategory.category.name,
                "subcategory": target_contract.subcategory.name,
                "category_content": target_contract.category_content,
                "group": target_contract.company.group.name,
                "company": target_contract.company.name,
                "representative": target_contract.representative.name,
                "representative_phone": target_contract.representative.phone_num,
                "representative_email": target_contract.representative.email,
                "employee": target_contract.employee.name,
                "revenue": target_contract.revenue,
                "issue_date": target_contract.issue_date,
                "memo": target_contract.memo
            }, status=200
        )


class ContractListView(View):
    
    def get(self, request):
        
        contracts = Contract.objects.select_related(
            'status__process',
            'status',
            'company',
            'company__group',
            'subcategory',
            'subcategory__category',
            'employee',
            'representative'
            ).all()

        return JsonResponse(
            {"contracts":[
                {
                "no":contract.id,
                "status":contract.status.status,
                "group":contract.company.group.name,
                "company":contract.company.name,
                "category":contract.subcategory.category.name,
                "subcategory":contract.subcategory.name,
                "subcategory_content":contract.category_content,
                "employee":contract.employee.name,
                "representative":contract.representative.name,
                "issue_date":contract.issue_date,
                "revenue":contract.revenue,
                "memo":contract.memo
                } for contract in contracts
            ]},status=200
        )
        