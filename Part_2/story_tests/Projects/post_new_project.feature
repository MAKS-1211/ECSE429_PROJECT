@Story
  Feature: The user wants to post a new project to the database

    Background: The API is already running on the user's system and has no entries
      Given the API is running
      And the API has no project entries

    # Normal Flow
    Scenario Outline: User wants to Post a valid project with all fields declared
      Given A project with a title <tit>, a description <desc>, an active status <act> and a completed status <comp>
      When The user posts the project
      Then The user receives a CREATED HTTP status code (201)
      And The user receives the project back in the response
      And The project will be in the database

      Examples:
        | tit       | desc            | act   | comp  |
        | Project 1 | Python testing  | False | True  |
        | Project 2 | Gherkin testing | True  | False |


    # Alternate Flow
    Scenario: User wants to Post a project with no fields declared
      Given A project with no title, no description, no active status and no completed status
      When The user posts the project
      Then The user receives a CREATED HTTP status code (201)
      And The user receives a default project back in the response with title = "", description = "", completed = False, active = False
      And The default project will be in the database

    # Error Flow
    Scenario Outline: User wants to Post a project with an id declared
      Given A project with a title <tit>, a description <desc>, an active status <act>, a completed status <comp> and an id <id>
      When The user posts the project
      Then The user will get a Bad Request HTTP status code (400)

      Examples:
        | tit       | desc            | act   | comp  | id |
        | Project 1 | Python testing  | False | True  | 2  |
        | Project 2 | Gherkin testing | True  | False | 47 |
