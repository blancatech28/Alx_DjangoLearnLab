Book Management API Views
This documentation provides an overview of the Django REST Framework views implemented for the Book Management system. It details the configuration, permissions, filtering capabilities, and custom behavioral hooks used in the views.


1. Pagination Configuration
CustomPageNumberPagination
To ensure API responses are manageable, a custom pagination class is used instead of the global default.
Default Page Size: 10 records per page.
Customizable Size: Clients can define the number of records returned using the query parameter ?page_size=X.
Maximum Limit: Capped at 100 records to prevent performance issues.



2. API Views
A. List All Books (BooklistView)
Endpoint Type: ListAPIView
Permissions: AllowAny (Publicly accessible)
This view provides a comprehensive list of books with advanced retrieval features.
Key Configurations:
Search: Users can perform partial text searches on the book title or the author__name via ?search=term.
Ordering: Results can be ordered by publication_year or title via ?ordering=publication_year.
Filtering:
Exact match on publication_year.
Custom get_queryset Logic:
author__name: Filters books by author name (case-insensitive partial match).
min_year: Filters books published on or after a specific year.
max_year: Filters books published on or before a specific year.
Usage Example:
GET /books/?min_year=2000&max_year=2020&search=Harry


B. Create a New Book (BookCreateView)
Endpoint Type: CreateAPIView
Permissions: IsAuthenticated (Requires valid token/session)
Handles the creation of new book records.
Custom Behavior (create method override):
Instead of the default DRF response, this view intercepts the creation process to return a consistent JSON envelope containing a success message and the serialized data.
Response Format:
{
    "message": "Book created successfully!",
    "data": { ...book_details... }
}


C. Update an Existing Book (BookUpdateView)
Endpoint Type: UpdateAPIView
Permissions: IsAuthenticated
Lookup Field: id (Expects URL pattern like /books/update/<id>/)
Allows authenticated users to modify existing book records. It supports PATCH requests for partial updates.
Custom Behavior (update method override):
Similar to the create view, the standard update method is overridden to return a custom status message alongside the updated data.
Response Format:
{
    "message": "Book updated successfully!",
    "data": { ...updated_details... }
}


D. Delete a Book (BookDeleteView)
Endpoint Type: DestroyAPIView
Permissions: IsAuthenticated
Lookup Field: id
Allows authenticated users to permanently remove a book record.
Custom Behavior (destroy method override):
Overrides the default deletion logic to return a specific JSON success message before sending the standard 204 No Content status.
Response Format:
{
    "message": "Book deleted successfully!"
}


