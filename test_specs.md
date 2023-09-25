## projects
Acceptance Tests
* GET all projects
* POST create project
* POST update project
* DELETE project
* GET project

Functional Tests
* POST create project, verify error when reach limit of projects (Negative)
* POST Update project deleted, verify error when a project has been deleted

## Tasks
Acceptance Test
* GET Get active tasks
* POST Create a new task
* GET Get an active task
* POST Update a task
* POST Close a task
* POST Reopen a task
* DELETE Delete a task

Functional Tests
* POST Update a deleted task (negative)
* POST Update a closed task
* DELETE Delete more than one task at a time
* DELETE Delete a closed task


## Section
* Get all sections
* Create a new section
* Get a single section
* Update a section
* Delete a section

Functional Tests
* POST Update a deleted section (negative)

## Comments
* Get all comments
* Create a new comment
* Get a comment
* Update a comment
* Delete a comment

Functional Tests
* POST Update a deleted comment (negative)
* POST Create a comment with no content (negative)

## Labels


E2E Test 
