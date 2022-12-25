# Welcome to The Invoice Take Home Assignement

The invoice test project to make a templete project in Python.
Check the requests in the **[POSTMAN Documentation](https://documenter.getpostman.com/view/7331112/2s8YzZNyUK)**.

## How to Run

To run the project just do the folow:
```
docker compose up -d
```
**NOTE:** In order to use the MongoDB text search feature, The necessary indexes must be applied. To do that, Run the migration command for the first time:
```
docker exec invoice invoice-migrate
```

## How to Run Tests

To run the pre-build tests just run the command below:
```
docker exec invoice python -m unittest discover
```
## The Project Structure

The project has been implemented based on the Three-Tier architecture with the service repository pattern.

There are **three main layers**:
* The controller layer which is responsible to handle the incoming requests.
* The service layer which is responsible to handle the application logic.
* The repository layer which is the data access layer.

