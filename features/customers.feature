Feature: The customer service back-end
    As a Customer Administrator
    I need a RESTful service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | firstName     | lastName      | email                   | address                                              | active |               salt               |                             password                             |
        | William       | Dixon         | will.dixon@hotmail.com  | PSC 4115, Box 7815\nAPO AA 41945                     | True   | 6edcc0329c89cb56c6ddfb4dfe451887 | 4f1b60f3fea4f90aacd277108bc646efd7e99ac6590cae4d643da49cc72d174a |
        | Jonathan      | Richard       | jrich@yahoo.com         | 778 Brown Plaza\nNorth Jenniferfurt, VT 88077        | True   | 6edcc0329c89cb56c6ddfb4dfe451887 | 4f1b60f3fea4f90aacd277108bc646efd7e99ac6590cae4d643da49cc72d174a |
        | Megan         | Chang         | mchang@gmail.com        | 398 Wallace Ranch Suite 593\nIvanburgh, AZ 80818     | False  | 6edcc0329c89cb56c6ddfb4dfe451887 | 4f1b60f3fea4f90aacd277108bc646efd7e99ac6590cae4d643da49cc72d174a |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Read a Customer
    When I visit the "Home Page"
    And I set the "Email" to "will.dixon@hotmail.com"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    And the "Salt" field should be empty
    And the "Password" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "William" in the "First Name" field
    And I should see "Dixon" in the "Last Name" field
    And I should see "will.dixon@hotmail.com" in the "Email" field
    And I should see "PSC 4115, Box 7815\nAPO AA 41945" in the "Address" field
    And I should see "6edcc0329c89cb56c6ddfb4dfe451887" in the "Salt" field
    And I should see "4f1b60f3fea4f90aacd277108bc646efd7e99ac6590cae4d643da49cc72d174a" in the "Password" field
    And I should see "True" in the "Active" dropdown

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Katherine"
    And I set the "Last Name" to "Fisher"
    And I set the "Email" to "kfisher@example.org"
    And I set the "Address" to "3513 John Divide Suite 115\nRodriguezside, LA 93111"
    And I set the "Salt" to "6bce3e2226016eb568e822b09f0ee020"
    And I set the "Password" to "888f807d45ff6ce47240c7ed4e884a6f9dc7b4fb"
    And I select "True" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    And the "Salt" field should be empty
    And the "Password" field should be empty
    And the "Active" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Katherine" in the "First Name" field
    And I should see "Fisher" in the "Last Name" field
    And I should see "kfisher@example.org" in the "Email" field
    And I should see "3513 John Divide Suite 115\nRodriguezside, LA 93111" in the "Address" field
    And I should see "6bce3e2226016eb568e822b09f0ee020" in the "Salt" field
    And I should see "888f807d45ff6ce47240c7ed4e884a6f9dc7b4fb" in the "Password" field
    And I should see "True" in the "Active" dropdown

Scenario: List all Customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "William" in the results
    And I should see "Jonathan" in the results
    And I should see "Megan" in the results

Scenario: Query a Customer by email
    When I visit the "Home Page"
    And I set the "Email" to "will.dixon@hotmail.com"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "William" in the "First Name" field
    And I should see "Dixon" in the "Last Name" field
    And I should see "will.dixon@hotmail.com" in the "Email" field
    And I should see "PSC 4115, Box 7815\nAPO AA 41945" in the "Address" field
    And I should see "6edcc0329c89cb56c6ddfb4dfe451887" in the "Salt" field
    And I should see "4f1b60f3fea4f90aacd277108bc646efd7e99ac6590cae4d643da49cc72d174a" in the "Password" field
    And I should see "True" in the "Active" dropdown

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "Email" to "jrich@yahoo.com"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Jonathan" in the "First Name" field
    And I should see "Richard" in the "Last Name" field  
    When I change "First Name" to "Olivia"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Olivia" in the "First Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Olivia" in the results
    And I should not see "Jonathan" in the results

Scenario: Deactivate a Customer
    When I visit the "Home Page"
    And I set the "Email" to "jrich@yahoo.com"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "True" in the "Active" dropdown
    When I press the "Deactivate" button
    Then I should see the message "Customer has been Deactivated!"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    And the "Salt" field should be empty
    And the "Password" field should be empty
    And the "Active" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Jonathan" in the "First Name" field
    And I should see "Richard" in the "Last Name" field
    And I should see "jrich@yahoo.com" in the "Email" field
    And I should see "778 Brown Plaza\nNorth Jenniferfurt, VT 88077" in the "Address" field
    And I should see "6edcc0329c89cb56c6ddfb4dfe451887" in the "Salt" field
    And I should see "4f1b60f3fea4f90aacd277108bc646efd7e99ac6590cae4d643da49cc72d174a" in the "Password" field
    And I should see "False" in the "Active" dropdown

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "Email" to "mchang@gmail.com"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    And the "Salt" field should be empty
    And the "Password" field should be empty
    And the "Active" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"
    
    When I set the "Email" to "will.dixon@hotmail.com"
    And I press the "Search" button
    And I press the "Delete" button
    And I set the "Email" to "jrich@yahoo.com"
    And I press the "Search" button
    And I press the "Delete" button
    And I press the "Search" button
    Then I should not see "William" in the results
    And I should not see "Jonathan" in the results