# OIDC/SAML Callback URL Validator

## Introduction
This proposal outlines the development of a Python-based software tool designed to validate a list of OpenID Connect (OIDC) or Security Assertion Markup Language (SAML) callback URLs. The primary objective of this tool is to ensure that the provided URLs are accessible and respond with specific HTTP status codes indicating their validity which will be used to audit the callback list settings for each client application within Auth0. This document describes the functionality, components, and specifications required for the tool's implementation.

## Objectives
* Primary Objective: To create a Python tool that takes a client_id, retrieves the client applications callback list, validates each callback URL against specified criteria, and returns their validity status.
* Usability Goal: To provide a straightforward and efficient mechanism for validating multiple OIDC or SAML callback URLs at once, ensuring they meet the necessary criteria for successful interactions.

## Techstack
Python 3.12.3

## Running Tests
Run the command:

```python3 -m unittest```

## Building an executable
Run the commands:

```cd validator```
```pyinstall --onefile validator```

## Running the executable