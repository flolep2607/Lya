# kalliope-todotxt

Interface to todotxt format todolist file.

## Synopsis

Let you manage todolist via Kalliope. This neuron manage todolist via a a single text file and follow the [todotxt](http://todotxt.com) rules so it can be used in parallèle with other todotxt compatible applications.

More information on [this blog post](https://bacardi55.org/en/blog/2017/todotxt-neuron-manage-todolist-compatible-todotxt-format) about the reasons of this choice.

**Available:**
* List tasks from file
* Filter tasks by project, priority, context, completeness status
* Add tasks
* Delete tasks by filters (priority, project, context, completeness status)

Working example in the up to date [sample directory](https://github.com/bacardi55/kalliope-todotxt/tree/master/samples)

**Todo:**
* Manage taks update (eg status change)
* Manage multiple project in orders (Task Class supports it)
* Manage multiple context in orders (Task Class supports it)
* Get / Delete task based on search text

**Won't do:**
* Send tasks (by email): Will use another script linked to kalliope (I'll write about it)

## Installation
```bash
kalliope install --git-url https://github.com/bacardi55/kalliope-todotxt.git
```

## Options

| parameter    | required | default | choices                   | comments                       |
|--------------|----------|---------|---------------------------|--------------------------------|
| action       | yes      |         | 'get', 'add' or 'del'     | The action to launch           |
| todotxt_file | yes      |         | String                    | The path to the todotxt file   |
| priority     | No       |         | 'A', 'B' or 'C'           | The priority of the task       |
| project      | No       |         | String                    | The project of the task        |
| context      | No       |         | String                    | The context of the task        |
| complete     | No       | False   | Boolean: False or True    | If the task is complete or not |
| content      | No       |         | String                    | The content of the task        |

**Additional notes:**

* If action is 'add': 
  * Content argument is mandatory
  * Priority/context/complete/projects will be added in the raw line in text file
* If action is 'get', adding priority / project / context will filter the results (see brain example below)
* If action is 'del', every tasks that match the given priority/project/context will be deleted.


## Return Values

Only necessary when the neuron use a template to say something

| name       | description                         | type          | sample                  |
|------------|-------------------------------------|---------------|-------------------------|
| action     | The action launched                 | string        | 'get', 'del' or 'add'   |
| task_list  | list of tasks (for get action only) | list of tasks | [task1, taks2, task3].  |
| count      | The number of returned element      | Integer       | 2                       |
| added_task | string value                        | Task object¹  | Task object¹            |

**Additional notes:**

* If action is 'get':
  * Count contains the number of return tasks in tasks_lists 
  * Task_lists contains the list of task object¹
  * add_task is unset
* If action is 'del':
  * Count contains the number of deleted tasks 
  * added_task is unset
  * task_list is unset
* If action is 'add':
  * Count is unset
  * added_task contain a Task object¹
  * task_list is empty


**Task Object:** The task object contains the following properties:

* Task.raw: the raw line representing the task in the todotxt file.
* Task.task_id: The task id (number of line)
* Task.task: The cleaned text of a text
* Task.priority: The priority
* Task.project: A list of project name 
* Task.context = A list of context name
* Task.creation_date: Creation date if precised
* Task.complete: Is the task complete?
* Task.completion_date: Completion date if completed task
* Task.due_date: Due date if precised.

You can reuse all these properties in ```template_file``` or ```file_template``` for each task objects (added_task or each element of task_list).


## Synapses example

Get tasks, no filter.

```yaml
  - name: "Get-all-tasks"
    signals:
      - order: "Get all my tasks"
    neurons:
      - todotxt:
          action: "get"
          todotxt_file: "resources/neurons/todotxt/samples/todo.txt"
          file_template: "templates/en_todotxt.j2"
```

Get tasks with specific filters

```yaml
  - name: "Get-specific-items"
    signals:
      - order: "Get my super list"
    neurons:
      - todotxt:
          action: "get"
          todotxt_file: "resources/neurons/todotxt/samples/todo.txt"
          project: "project"
          priority: "A"
          context: "context"
          complete: False
          file_template: "templates/en_todotxt.j2"
```

Add item to list

```yaml
  - name: "add-item-to-super-list"
    signals:
      - order: "add {{content}} to the super list"
    neurons:
      - todotxt:
          action: "add"
          todotxt_file: "resources/neurons/todotxt/samples/todo.txt"
          project: "project"
          priority: "A"
          context: "context"
          complete: False
          content: "{{content}}"
          say_template: "Task {{added_task.task}} has been added to the super project with priority {{added_task.priority}}"
```

You could also add arguments with value coming from voice order directly:

```yaml
  - name: "add-item-to-super-list"
    signals:
      - order: "add {{content}} to the {{project}} list with priority {{priority}} and context {{context}}"
    neurons:
      - todotxt:
          action: "add"
          todotxt_file: "resources/neurons/todotxt/samples/todo.txt"
          complete: False
          content: "{{content}}"
          project: "{{project}}"
          priority: "{{priority}}"
          context: "{{context}}"
          say_template: "Task {{added_task.task}} has been added to the super project with priority {{added_task.priority}}"
```

Remove items that match filters from global list .

```yaml
  - name: "clear-super-list"
    signals:
      - order: "clear super list"
    neurons:
      - todotxt:
          action: "del"
          todotxt_file: "resources/neurons/todotxt/samples/todo.txt"
          project: "project"
          priority: "A"
          context: "context"
          complete: False
          say_template: "{{count}} items have been deleted"
```

## Templates example 

This template list tasks if any, or indicate that no tasks are in the list.

```
{% if count > 0 %}
    Your list contains:
    {% for task in task_list %}
        {{ task.text }}
    {% endfor %}
{% else %}
    You don't have any item in your list
{% endif %}
```

Refer to the return value part of this page to understand what else you can use in the ```task``` object.


## Additional links

* [A blog post about the todotxt neuron](http://bacardi55.org/2017/02/28/todotxt-a-neuron-to-manage-todolist-compatible-with-todotxt-format.html)
* [A blog post about how I use this neuron to manage grocery list](http://bacardi55.org/2017/03/16/managing-a-shopping-list-with-kalliope.html)
* [My blog posts about Kalliope](http://bacardi55.org/kalliope.html)


## Licence


