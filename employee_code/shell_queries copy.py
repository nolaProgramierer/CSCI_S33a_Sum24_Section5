# 1) Show all employees
employees = Employee.objects.all()
employees

# 2) Show # of employees
employees.count()

# 3) Show # of bosses
 boss_count = Employee.objects.filter(boss=True).count()

# 4)Show bosses
bosses = Employee.objects.filter(boss=True)
bosses

supervisors = Employee.objects.filter(subordinates__isnull=False).distinct()
supervisors

# 5)Find employees who are not assigned to any supervisor
unassigned_employees = Employee.objects.filter(supervisors__isnull=True)
unassigned_employees

# 6) Get all employees who aren’t supervisors
non_supervisors = Employee.objects.filter(subordinates__isnull=True)

# 7) Find # of people who work for Heather Bond
bond = Employee.objects.get(lname="Bond")
bond.boss
bond.subordinates.count()

# 8) Return supervisor of Liam Rees (front-side query)
rees = Employee.objects.get(lname="Rees")
rees.supervisors.all()

# 9) See if Liam has subordinates (reverse-side query) 
rees.subordinates.all()

# 10) Add an employee
e1 = Employee(fname="Howard", lname="Beale")
e1.save()

# 11) Make his boss Gordon Willson (front-side query)
boss1 = Employee.objects.get(lname="Wilson")
boss1
e1.supervisors.count()
e1.supervisors.add(boss1)
e1.save()
e1.supervisors.count()

# 12) Make another employee
e2 = Employee(fname="Kris", lname="Kelly")
e2.save()

# 13)Make this employee’s boss Gordon (reverse-side)
boss1
boss1.subordinates.add(e2)
boss1.save()
boss1.subordinates.count()
boss1.subordinates.all









