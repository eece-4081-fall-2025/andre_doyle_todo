from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDo


def task_list(request):
    # Show all tasks ordered: incomplete first, then by due date, then by name
    tasks = ToDo.objects.order_by("complete", "due_date", "name")
    return render(request, "todo/task_list.html", {"tasks": tasks})


def task_create(request):
    # Handle form submit to create a new task
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        due_date = request.POST.get("due_date") or None

        if name:
            ToDo.objects.create(name=name, due_date=due_date)

        return redirect("task_list")

    # Show the blank form (not used by tests but good for UI)
    return render(request, "todo/task_form.html")


def task_update(request, pk):
    # Optional: edit an existing task
    task = get_object_or_404(ToDo, pk=pk)

    if request.method == "POST":
        task.name = request.POST.get("name", task.name).strip()
        task.due_date = request.POST.get("due_date") or None
        task.save()
        return redirect("task_list")

    return render(request, "todo/task_form.html", {"task": task})


def task_toggle_complete(request, pk):
    # Toggle completion state (this is what URL name `task_toggle` points to)
    task = get_object_or_404(ToDo, pk=pk)
    task.complete = not task.complete
    task.save()
    return redirect("task_list")


def task_delete(request, pk):
    # Delete a task, then redirect
    task = get_object_or_404(ToDo, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "todo/task_confirm_delete.html", {"task": task})
