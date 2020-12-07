import json
import jwt_utils

from django.views   import View
from django.http    import JsonResponse

from contract.models    import Process, Contract, ContractProcess, Category, ContractCategory
from company.models     import CompanyGroup,Company,Representative
from employee.models    import Employee

# Create your views here.
class ContractPostView(View):
    #@jwt_utils.signin_decorator
    def get(self, request):
        
        company_list = [{'group_name':company.company_group.name if company.company_group != None else '기타','company_name':company.name, 
                                'representatives':[repre.name if repre!=[] else '' for repre in company.representative_set.all()]} 
                            for company in Company.objects.select_related('company_group').prefetch_related('representative_set').all()]
        
        category_list = [{'category':'검사', 'subcategory':['온라인','오프라인'],'category_content':['인성','적성','인적성']},
                        {'category':'교육', 'subcategory':['온라인','오프라인'],'category_content':['면접위원 교육', '감독관 교육']},
                        {'category':'운영', 'subcategory':['온라인','오프라인'],'category_content':['검사','교육']},
                        {'category':'개발', 'subcategory':['선발 Tool', '프로그램'],'category_content':False},
                        {'category':'기타', 'subcategory':False,'category_content':False}]

        return JsonResponse({
            'companies' : company_list,
            'categories' : category_list
            },status=200)

    #@jwt_utils.signin_decorator
    def post(self, request):
        try:
            #employee_id = request.employee.id
            employee_id = 1

            data = json.loads(request.body)


            target_company, create = Company.objects.get_or_create(name=data['company'], company_group_id=CompanyGroup.objects.get(name=data['group']).id)
            target_representative, create = Representative.objects.get_or_create(
                name=data['representative']['name'],phone_num=data['representative']['mobile'],email=data['representative']['email'],company_id=target_company.id)

            if 'memo' in data:
                target_memo = data['memo']
            else:
                target_memo = None

            new_contract = Contract(
                company          = target_company,
                representative   = target_representative,
                employee         = Employee.objects.get(id=employee_id),
                memo             = target_memo,
                )

            new_contract.save()

            for category in data['categories']:
                target_category, flag = Category.objects.get_or_create(category = category['category'], subcategory = category['subcategory'], category_content = category['category_content'])

                ContractCategory(
                    target_contract = new_contract,
                    category = target_category
                ).save()
            
            for process in data['processes']:
                print(process['title'])
                print(process['status'])
                ContractProcess(
                    target_contract = new_contract,
                    process = Process.objects.get(title = process['title'], status=process['status']),
                    revenue = process['income']/1.1,
                    vat = process['income']/11,
                    issue_date = process['issue_date']
                ).save()

            contract_info = Contract.objects.select_related('company','representative','employee').prefetch_related('process','contractprocess_set','category').get(id = new_contract.id)


            return JsonResponse(
                {
                    "employee":contract_info.employee.name,
                    "group":contract_info.company.company_group.name,
                    "company":contract_info.company.name,
                    "representative_info":{'name':contract_info.representative.name,'mobile':contract_info.representative.phone_num,'email':contract_info.representative.email},
                    "process":[{'title':Process.objects.get(id = proc['process_id']).title,
                                "status":Process.objects.get(id = proc['process_id']).status,
                                "revenue":proc['revenue'],
                                "vat":proc['vat'],
                                "issue_date":proc['issue_date']} for proc in contract_info.contractprocess_set.all().values()],
                    "category_list":[{'category':gory.category.category,'subcategory':gory.category.subcategory,'category_content':gory.category.category_content} for gory in contract_info.contractcategory_set.all()],
                    "memo":contract_info.memo
                },status=201
            )
        
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        
        except ValueError as e:
            return JsonResponse({"message": f"VALUE_ERROR:{e}"}, status=400) 

    
class ContractDetailView(View):
    #@jwt_utils.signin_decorator
    def get(self, request, contract_id):

        contract_info = Contract.objects.select_related('company','representative','employee').prefetch_related('process','contractprocess_set','category').get(id = contract_id)

        return JsonResponse(
                {
                    "employee":contract_info.employee.name,
                    "group":contract_info.company.company_group.name,
                    "company":contract_info.company.name,
                    "representative_info":{'name':contract_info.representative.name,'mobile':contract_info.representative.phone_num,'email':contract_info.representative.email},
                    "process":[{'title':Process.objects.get(id = proc['process_id']).title,
                                "status":Process.objects.get(id = proc['process_id']).status,
                                "revenue":proc['revenue'],
                                "vat":proc['vat'],
                                "issue_date":proc['issue_date']} for proc in contract_info.contractprocess_set.all().values()],
                    "category_list":[{'category':gory.category.category,'subcategory':gory.category.subcategory,'category_content':gory.category.category_content} for gory in contract_info.contractcategory_set.all()],
                    "memo":contract_info.memo
                },status=200
            )

    #@jwt_utils.signin_decorator
    def patch(self, request, contract_id):
        try:
            #employee_id = request.employee.id
            employee_id = 1

            data = json.loads(request.body)
            target_contract = Contract.objects.prefetch_related('process','contractprocess_set','category').get(id=contract_id)


            if 'company' in data and 'group' in data:
                target_company, create = Company.objects.get_or_create(name=data['company'], company_group_id=CompanyGroup.objects.get(name=data['group']).id)
                target_contract.company = target_company

            if 'representative' in data:
                target_representative, create = Representative.objects.get_or_create(
                    name=data['representative']['name'],phone_num=data['representative']['mobile'],email=data['representative']['email'],company_id=target_company.id)
                target_contract.representative = target_representative

            if 'memo' in data:
                target_contract.memo = data['memo']
            else:
                target_contract.memo = None

            target_contract.save()

            if 'categories' in data:
                ContractCategory.objects.filter(target_contract_id = contract_id).delete()
                for category in data['categories']:
                    target_category, flag = Category.objects.get_or_create(category = category['category'], subcategory = category['subcategory'], category_content = category['category_content'])


                    ContractCategory(
                        target_contract = target_contract,
                        category = target_category
                    ).save()

            if 'processes' in data:
                print(target_contract.process.all())
                ContractProcess.objects.filter(target_contract_id = contract_id).delete()
                for process in data['processes']:
                    ContractProcess(
                        target_contract = target_contract,
                        process = Process.objects.get(title = process['title'], status=process['status']),
                        revenue = process['income']/1.1,
                        vat = process['income']/11,
                        issue_date = process['issue_date']
                    ).save()
           
            contract_info = Contract.objects.select_related('company','representative','employee').prefetch_related('contractcategory_set','contractprocess_set').get(id = target_contract.id)

           
            return JsonResponse(
                {
                    "employee":contract_info.employee.name,
                    "group":contract_info.company.company_group.name,
                    "company":contract_info.company.name,
                    "representative_info":{'name':contract_info.representative.name,'mobile':contract_info.representative.phone_num,'email':contract_info.representative.email},
                    "process":[{'title':Process.objects.get(id = proc['process_id']).title,
                                "status":Process.objects.get(id = proc['process_id']).status,
                                "revenue":proc['revenue'],
                                "vat":proc['vat'],
                                "issue_date":proc['issue_date']} for proc in contract_info.contractprocess_set.all().values()],
                    "category_list":[{'category':gory.category.category,'subcategory':gory.category.subcategory,'category_content':gory.category.category_content} for gory in contract_info.contractcategory_set.all()],
                    "memo":contract_info.memo
                },status=201
            )
        
        except KeyError as e :
            return JsonResponse({'MESSAGE': f'KEY_ERROR:{e}'}, status=400)
        
        except ValueError as e:
            return JsonResponse({"message": f"VALUE_ERROR:{e}"}, status=400)

    #@jwt_utils.signin_decorator
    def delete(self, request, contract_id):
        #employee_id = request.employee.id
        employee_id = 1

        target_contract = Contract.objects.prefetch_related('process','contractprocess_set','category').get(id=contract_id)
        if target_contract.employee.id != employee_id and Employee.objects.get(id=employee_id).is_admin != 1:
            return JsonResponse({'message':'ACCESS_DENIED'},status=403)

        target_contract.contractprocess_set.all().delete()
        target_contract.contractcategory_set.all().delete()
        target_contract.delete()

        return JsonResponse({'message':'삭제완료!'},status=200)



class ContractListView(View):
    #@jwt_utils.signin_decorator
    def get(self, request):
        
        contracts = Contract.objects.select_related(
                'company',
                'company__company_group',
                'representative'
            ).prefetch_related(
                'contractprocess_set',
                'contractcategory_set'
            ).all()

        return JsonResponse(
            {"contracts":[
                {
                "no":contract.id,
                "employee":contract.employee.name,
                "group":contract.company.company_group.name,
                "company":contract.company.name,
                "representative_info":{'name':contract.representative.name,'mobile':contract.representative.phone_num,'email':contract.representative.email},
                "process":[{'title':Process.objects.get(id = proc['process_id']).title,
                            "status":Process.objects.get(id = proc['process_id']).status,
                            "revenue":proc['revenue'],
                            "vat":proc['vat'],
                            "issue_date":proc['issue_date']} for proc in contract.contractprocess_set.all().values()],
                "category_list":[{'category':gory.category.category,'subcategory':gory.category.subcategory,'category_content':gory.category.category_content} for gory in contract.contractcategory_set.all()],
                "memo":contract.memo
                } for contract in contracts
            ]},status=200
        )
        