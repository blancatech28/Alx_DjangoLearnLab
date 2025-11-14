# Permissions Setup

## Permissions
- can_view: Allow users to view books
- can_create: Allow users to create books
- can_edit: Allow users to edit books
- can_delete: Allow users to delete books

## Groups
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

## Views
- book_list: requires can_view
- book_detail: requires can_view
- book_create: requires can_create
- book_edit: requires can_edit
- book_delete: requires can_delete