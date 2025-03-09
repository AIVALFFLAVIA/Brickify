from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Client, Project, Employee, Supplier, Material, Equipment, FinancialTransaction, Task
from django.contrib.auth.decorators import login_required


#Dashboard
def dashboard_view(request):
    return render(request, "dashboard.html")

def is_leader(user):
    return user.groups.filter(name='Company Leaders').exists()

def unauthorized(request):
    return render(request, "unauthorized.html")

@login_required
def leader_dashboard(request):
    # Check if the user is a company leader
    if not is_leader(request.user):
        return redirect('unauthorized')  # Redirect to the unauthorized page if not a leader

    # If the user is a leader, render the leader dashboard
    return render(request, "leader_dashboard.html")

# Helper function to check user authorization
def is_authorized(user, company):
    return company.owner == user

# Company Views
@login_required
def company_list(request):
    companies = Company.objects.filter(owner=request.user)

    # Filtering & Sorting
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')

    if search_query:
        companies = companies.filter(name__icontains=search_query)
    
    companies = companies.order_by(sort_by)

    # return render(request, "company_list.html", {'companies': companies})
    return render(request, "company_list.html", {
        'companies': companies,
        'search_query': search_query,
        'sort_by': sort_by,
    })

@login_required
def company_create(request):
    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        contact_email = request.POST['contact_email']
        contact_phone = request.POST['contact_phone']

        # Assign the logged-in user as the owner
        Company.objects.create(
            name=name, address=address, 
            contact_email=contact_email, contact_phone=contact_phone, 
            owner=request.user
        )
        return redirect('company_list')

    return render(request, "company_form.html")

@login_required
def company_update(request, id):
    company = get_object_or_404(Company, id=id)

    if not is_authorized(request.user, company):
        return render(request, "unauthorized.html")

    if request.method == "POST":
        company.name = request.POST['name']
        company.address = request.POST['address']
        company.contact_email = request.POST['contact_email']
        company.contact_phone = request.POST['contact_phone']
        company.save()
        return redirect('company_list')

    return render(request, "company_form.html", {'company': company})

@login_required
def company_delete(request, id):
    company = get_object_or_404(Company, id=id)

    if not is_authorized(request.user, company):
        return render(request, "unauthorized.html")

    company.delete()
    return redirect('company_list')


# Client Views
@login_required
def client_list(request):
    clients = Client.objects.filter(company__owner=request.user)

    # Filtering & Sorting
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')

    if search_query:
        clients = clients.filter(name__icontains=search_query)
    
    clients = clients.order_by(sort_by)

    return render(request, "client_list.html", {
        'clients': clients,
        'search_query': search_query,
        'sort_by': sort_by,
        })

@login_required
def client_create(request):
    companies = Company.objects.filter(owner=request.user)  # Fetch only user's companies

    if request.method == "POST":
        name = request.POST['name']
        contact_info = request.POST['contact_info']
        email = request.POST['email']
        address = request.POST['address']
        company_id = request.POST['company']
        company = get_object_or_404(Company, id=company_id)

        if not is_authorized(request.user, company):
            return render(request, "unauthorized.html")

        Client.objects.create(
            name=name, contact_info=contact_info, 
            email=email, address=address, company=company
        )
        return redirect('client_list')

    return render(request, "client_form.html", {'companies': companies})

@login_required
def client_update(request, id):
    client = get_object_or_404(Client, id=id)

    if not is_authorized(request.user, client.company):
        return render(request, "unauthorized.html")

    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        client.name = request.POST['name']
        client.contact_info = request.POST['contact_info']
        client.email = request.POST['email']
        client.address = request.POST['address']
        client.company_id = request.POST['company']
        client.save()
        return redirect('client_list')

    return render(request, "client_form.html", {'client': client, 'companies': companies})

@login_required
def client_delete(request, id):
    client = get_object_or_404(Client, id=id)

    if not is_authorized(request.user, client.company):
        return render(request, "unauthorized.html")

    client.delete()
    return redirect('client_list')


# Project Views
@login_required
def project_list(request):
    projects = Project.objects.filter(company__owner=request.user)

    # Filtering & Sorting
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')

    if search_query:
        projects = projects.filter(name__icontains=search_query)
    
    projects = projects.order_by(sort_by)

    return render(request, "project_list.html", {
        'projects': projects,
        'search_query': search_query,
        'sort_by': sort_by,
        })

@login_required
def project_create(request):
    clients = Client.objects.filter(company__owner=request.user)
    companies = Company.objects.filter(owner=request.user)
    status_choices = Project.STATUS_CHOICES  

    if request.method == "POST":
        name = request.POST['name']
        client_id = request.POST['client']
        company_id = request.POST['company']
        location = request.POST['location']
        start_date = request.POST['start_date']
        end_date = request.POST.get('end_date', None)
        budget = request.POST['budget']
        status = request.POST['status']

        client = get_object_or_404(Client, id=client_id)
        company = get_object_or_404(Company, id=company_id)

        if not is_authorized(request.user, company):
            return render(request, "unauthorized.html")

        Project.objects.create(
            name=name, client=client, company=company,
            location=location, start_date=start_date, end_date=end_date,
            budget=budget, status=status
        )
        return redirect('project_list')

    return render(request, "project_form.html", {'clients': clients, 'companies': companies, 'status_choices': status_choices})

@login_required
def project_update(request, id):
    project = get_object_or_404(Project, id=id)

    if not is_authorized(request.user, project.company):
        return render(request, "unauthorized.html")

    clients = Client.objects.filter(company__owner=request.user)
    companies = Company.objects.filter(owner=request.user)
    status_choices = Project.STATUS_CHOICES  

    if request.method == "POST":
        project.name = request.POST['name']
        project.client_id = request.POST['client']
        project.company_id = request.POST['company']
        project.location = request.POST['location']
        project.start_date = request.POST['start_date']
        project.end_date = request.POST.get('end_date', None)
        project.budget = request.POST['budget']
        project.status = request.POST['status']
        project.save()
        return redirect('project_list')

    return render(request, "project_form.html", {'project': project, 'clients': clients, 'companies': companies, 'status_choices': status_choices})

@login_required
def project_delete(request, id):
    project = get_object_or_404(Project, id=id)

    if not is_authorized(request.user, project.company):
        return render(request, "unauthorized.html")

    project.delete()
    return redirect('project_list')

# Employee Views
@login_required
def employee_list(request):
    employees = Employee.objects.filter(company__owner=request.user)

    # Filtering & Sorting
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'first_name')

    if search_query:
        employees = employees.filter(first_name__icontains=search_query)

    employees = employees.order_by(sort_by)

    return render(request, "employee_list.html", {
        'employees': employees,
        'position_choices': Employee.POSITION_CHOICES,
        'search_query': search_query,
        'sort_by': sort_by,
    })

@login_required
def employee_create(request):
    projects = Project.objects.filter(company__owner=request.user)
    companies = Company.objects.filter(owner=request.user)
    position_choices = Employee.POSITION_CHOICES  

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        position = request.POST['position']
        salary = request.POST['salary']
        project_id = request.POST.get('project')
        company_id = request.POST['company']

        project = get_object_or_404(Project, id=project_id) if project_id else None
        company = get_object_or_404(Company, id=company_id)

        if not is_authorized(request.user, company):
            return render(request, "unauthorized.html")

        Employee.objects.create(
            first_name=first_name, last_name=last_name, 
            position=position, salary=salary, 
            project=project, company=company
        )

        return redirect('employee_list')

    return render(request, "employee_form.html", {
        "projects": projects, 
        "companies": companies, 
        "position_choices": position_choices
    })

@login_required
def employee_update(request, id):
    employee = get_object_or_404(Employee, id=id)

    if not is_authorized(request.user, employee.company):
        return render(request, "unauthorized.html")

    projects = Project.objects.filter(company__owner=request.user)
    companies = Company.objects.filter(owner=request.user)
    position_choices = Employee.POSITION_CHOICES  

    if request.method == "POST":
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.position = request.POST['position']
        employee.salary = request.POST['salary']
        employee.project_id = request.POST.get('project')
        employee.company_id = request.POST['company']
        employee.save()
        return redirect('employee_list')

    return render(request, "employee_form.html", {
        'employee': employee, 
        'projects': projects, 
        'companies': companies, 
        'position_choices': position_choices
    })

@login_required
def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)

    if not is_authorized(request.user, employee.company):
        return render(request, "unauthorized.html")

    employee.delete()
    return redirect('employee_list')


# Supplier Views
@login_required
def supplier_list(request):
    suppliers = Supplier.objects.filter(company__owner=request.user)

    # Filtering & Sorting
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')

    if search_query:
        suppliers = suppliers.filter(name__icontains=search_query)

    suppliers = suppliers.order_by(sort_by)

    return render(request, "supplier_list.html", {
        'suppliers': suppliers,
        'search_query': search_query,
        'sort_by': sort_by,})

@login_required
def supplier_create(request):
    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        name = request.POST['name']
        contact_info = request.POST['contact_info']
        email = request.POST['email']
        company_id = request.POST['company']
        company = get_object_or_404(Company, id=company_id)

        if not is_authorized(request.user, company):
            return render(request, "unauthorized.html")

        Supplier.objects.create(name=name, contact_info=contact_info, email=email, company=company)
        return redirect('supplier_list')

    return render(request, "supplier_form.html", {'companies': companies})

@login_required
def supplier_update(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if not is_authorized(request.user, supplier.company):
        return render(request, "unauthorized.html")

    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        supplier.name = request.POST['name']
        supplier.contact_info = request.POST['contact_info']
        supplier.email = request.POST['email']
        supplier.company_id = request.POST['company']
        supplier.save()
        return redirect('supplier_list')

    return render(request, "supplier_form.html", {'supplier': supplier, 'companies': companies})

@login_required
def supplier_delete(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if not is_authorized(request.user, supplier.company):
        return render(request, "unauthorized.html")

    supplier.delete()
    return redirect('supplier_list')


# Material Views
from django.db.models import Q

@login_required
def material_list(request):
    # Fetch materials related to the user's company
    materials = Material.objects.filter(company__owner=request.user)

    # Get search query and sort options from request parameters
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')

    # Apply filtering based on search query
    if search_query:
        materials = materials.filter(
            Q(name__icontains=search_query) |
            Q(supplier__name__icontains=search_query) |
            Q(quantity__icontains=search_query)
        )

    # Apply sorting based on the selected sorting option
    materials = materials.order_by(sort_by)

    # Render the template with the filtered and sorted materials
    return render(request, "material_list.html", {
        'materials': materials,
        'suppliers': Supplier.objects.filter(company__owner=request.user),
        'search_query': search_query,
        'sort_by': sort_by,
    })


@login_required
def material_create(request):
    suppliers = Supplier.objects.filter(company__owner=request.user)
    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        unit_price = request.POST['unit_price']
        supplier_id = request.POST['supplier']
        company_id = request.POST['company']

        supplier = get_object_or_404(Supplier, id=supplier_id)
        company = get_object_or_404(Company, id=company_id)

        if not is_authorized(request.user, company):
            return render(request, "unauthorized.html")

        Material.objects.create(name=name, quantity=quantity, unit_price=unit_price, supplier=supplier, company=company)
        return redirect('material_list')

    return render(request, "material_form.html", {'suppliers': suppliers, 'companies': companies})

@login_required
def material_update(request, id):
    material = get_object_or_404(Material, id=id)

    if not is_authorized(request.user, material.company):
        return render(request, "unauthorized.html")

    suppliers = Supplier.objects.filter(company__owner=request.user)
    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        material.name = request.POST['name']
        material.quantity = request.POST['quantity']
        material.unit_price = request.POST['unit_price']
        material.supplier_id = request.POST['supplier']
        material.company_id = request.POST['company']
        material.save()
        return redirect('material_list')

    return render(request, "material_form.html", {'material': material, 'suppliers': suppliers, 'companies': companies})

@login_required
def material_delete(request, id):
    material = get_object_or_404(Material, id=id)

    if not is_authorized(request.user, material.company):
        return render(request, "unauthorized.html")

    material.delete()
    return redirect('material_list')



# Equipment Views
@login_required
def equipment_list(request):
    equipments = Equipment.objects.filter(company__owner=request.user)

    # Filtering & Sorting
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', 'name')

    # Apply search filter
    if search_query:
        equipments = equipments.filter(name__icontains=search_query)
    
    # Apply status filter
    if status_filter:
        equipments = equipments.filter(status=status_filter)

    # Apply sorting
    equipments = equipments.order_by(sort_by)

    return render(request, "equipment_list.html", {
        'equipments': equipments,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
    })

@login_required
def equipment_create(request):
    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        name = request.POST['name']
        status = request.POST['status']
        purchase_date = request.POST['purchase_date']
        company_id = request.POST['company']
        company = get_object_or_404(Company, id=company_id)

        if not is_authorized(request.user, company):
            return render(request, "unauthorized.html")

        Equipment.objects.create(name=name, status=status, purchase_date=purchase_date, company=company)
        return redirect('equipment_list')

    return render(request, "equipment_form.html", {'companies': companies})

@login_required
def equipment_update(request, id):
    equipment = get_object_or_404(Equipment, id=id)

    if not is_authorized(request.user, equipment.company):
        return render(request, "unauthorized.html")

    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        equipment.name = request.POST['name']
        equipment.status = request.POST['status']
        equipment.purchase_date = request.POST['purchase_date']
        equipment.company_id = request.POST['company']
        equipment.save()
        return redirect('equipment_list')

    return render(request, "equipment_form.html", {'equipment': equipment, 'companies': companies})

@login_required
def equipment_delete(request, id):
    equipment = get_object_or_404(Equipment, id=id)

    if not is_authorized(request.user, equipment.company):
        return render(request, "unauthorized.html")

    equipment.delete()
    return redirect('equipment_list')



# Financial Transaction Views
@login_required
def financial_transaction_list(request):
    transactions = FinancialTransaction.objects.filter(company__owner=request.user)

    # Filtering & Sorting
    search_query = request.GET.get('search', '')
    transaction_type_filter = request.GET.get('transaction_type', '')
    sort_by = request.GET.get('sort', 'date')

    # Apply search filter
    if search_query:
        transactions = transactions.filter(description__icontains=search_query)
    
    # Apply transaction type filter
    if transaction_type_filter:
        transactions = transactions.filter(transaction_type=transaction_type_filter)

    # Apply sorting
    transactions = transactions.order_by(sort_by)

    return render(request, "financial_transaction_list.html", {
        'transactions': transactions,
        'search_query': search_query,
        'transaction_type_filter': transaction_type_filter,
        'sort_by': sort_by,
    })

@login_required
def financial_transaction_create(request):
    projects = Project.objects.filter(company__owner=request.user)
    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        project_id = request.POST['project']
        amount = request.POST['amount']
        transaction_type = request.POST['transaction_type']
        date = request.POST['date']
        description = request.POST['description']
        company_id = request.POST['company']

        project = get_object_or_404(Project, id=project_id)
        company = get_object_or_404(Company, id=company_id)

        if not is_authorized(request.user, company):
            return render(request, "unauthorized.html")

        FinancialTransaction.objects.create(
            project=project, amount=amount, transaction_type=transaction_type,
            date=date, description=description, company=company
        )

        return redirect('financial_transaction_list')

    return render(request, "financial_transaction_form.html", {'projects': projects, 'companies': companies})

@login_required
def financial_transaction_update(request, id):
    transaction = get_object_or_404(FinancialTransaction, id=id)

    if not is_authorized(request.user, transaction.company):
        return render(request, "unauthorized.html")

    projects = Project.objects.filter(company__owner=request.user)
    companies = Company.objects.filter(owner=request.user)

    if request.method == "POST":
        transaction.project_id = request.POST['project']
        transaction.amount = request.POST['amount']
        transaction.transaction_type = request.POST['transaction_type']
        transaction.date = request.POST['date']
        transaction.description = request.POST['description']
        transaction.company_id = request.POST['company']
        transaction.save()
        return redirect('financial_transaction_list')

    return render(request, "financial_transaction_form.html", {
        'transaction': transaction, 
        'projects': projects, 
        'companies': companies
    })

@login_required
def financial_transaction_delete(request, id):
    transaction = get_object_or_404(FinancialTransaction, id=id)

    if not is_authorized(request.user, transaction.company):
        return render(request, "unauthorized.html")

    transaction.delete()
    return redirect('financial_transaction_list')


# Task Views
@login_required
def task_list(request):
    tasks = Task.objects.filter(project__company__owner=request.user)

    # Filtering & Sorting
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'deadline')

    if search_query:
        tasks = tasks.filter(task_name__icontains=search_query)

    tasks = tasks.order_by(sort_by)

    return render(request, "task_list.html", {
        'tasks': tasks,
        'search_query': search_query,
        'sort_by': sort_by,
    })

@login_required
def task_create(request):
    projects = Project.objects.filter(company__owner=request.user)
    employees = Employee.objects.filter(company__owner=request.user)

    if request.method == "POST":
        project_id = request.POST['project']
        task_name = request.POST['task_name']
        assigned_to_id = request.POST['assigned_to']
        status = request.POST['status']
        deadline = request.POST['deadline']

        project = get_object_or_404(Project, id=project_id)
        assigned_to = get_object_or_404(Employee, id=assigned_to_id)

        if not is_authorized(request.user, project.company):
            return render(request, "unauthorized.html")

        Task.objects.create(
            project=project, task_name=task_name, 
            assigned_to=assigned_to, status=status, deadline=deadline
        )

        return redirect('task_list')

    return render(request, "task_form.html", {'projects': projects, 'employees': employees})

@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id)

    if not is_authorized(request.user, task.project.company):
        return render(request, "unauthorized.html")

    projects = Project.objects.filter(company__owner=request.user)
    employees = Employee.objects.filter(company__owner=request.user)

    if request.method == "POST":
        task.project_id = request.POST['project']
        task.task_name = request.POST['task_name']
        task.assigned_to_id = request.POST['assigned_to']
        task.status = request.POST['status']
        task.deadline = request.POST['deadline']
        task.save()
        return redirect('task_list')

    return render(request, "task_form.html", {'task': task, 'projects': projects, 'employees': employees})

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)

    if not is_authorized(request.user, task.project.company):
        return render(request, "unauthorized.html")

    task.delete()
    return redirect('task_list')
