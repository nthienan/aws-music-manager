*** Settings ***
Library  SeleniumLibrary

*** Keywords ***
Submit Userame
    [Arguments]  ${USER_NAME}
    Wait Until Page Contains Element  id=username
    Input Text  id=username  ${USER_NAME}


Submit Password
    [Arguments]  ${PASSWORD}
    Wait Until Page Contains Element  id=password
    Input Password  id=password  ${PASSWORD}


Submit Credentials
    Click Button  id=btn-login

Verify Home Page Should Be Opened
    Wait Until Page Contains Element  id=srch-term
