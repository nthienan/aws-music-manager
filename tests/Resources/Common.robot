*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${BROWSER}  chrome

*** Keywords ***
Open Website
    [Arguments]  ${URL}
    Open Browser  ${URL}  ${BROWSER}
    Maximize Browser Window

