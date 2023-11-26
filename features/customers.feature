Feature: The customer service back-end
    As a Customer Administrator
    I need a RESTful service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | firstName     | lastName      | email                   | address                                              | active |
        | William       | Dixon         | will.dixon@hotmail.com  | PSC 4115, Box 7815\nAPO AA 41945                     | True   |
        | Jonathan      | Richard       | jrich@yahoo.com         | 778 Brown Plaza\nNorth Jenniferfurt, VT 88077        | True   |
        | Megan         | Chang         | mchang@gmail.com        | 398 Wallace Ranch Suite 593\nIvanburgh, AZ 80818     | False  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"
