# Please update related files if you modified these attributes

# TODO:

# Append char(s) to abbr:
#
# Two words can be separated if someone want convert all abbr. to lowercase
# e.g., HTTPProtocol ---(convert to lowercase)---> httpprotocol
#       (it is difficult to identify the two words)
#
#       HTTPProtocol --- (append '_' to abbr) ---> http_Protocol
#                    ---(convert to lowercase)---> http_protocol


# How can we find an abbr:
#
#   good:
#       HTTP[^A-Za-z]*Response (HTTP)
#
#   bad, the outputs of these names may be wrong below:
#       httpresponse (can't be identified)
#       HTTPresponse (HTT)


# Priority 0 is highest priority
#   origin                    Get_HTTPResponse-Code

# alphabet
#   upper_case                GET_HTTPRESPONSE-CODE
#   lower_case                get_httpresponse-code
#   camel_case                get_HttpResponse-Code
#   pascal_case               Get_HttpResponse-Code

# abbr
#   ignore_abbr               Get_HTTPResponse-Code (with pascal_case)
#                             get_HTTPresponse-code (with lower_case)

# sep
#   dash_to_underscore        Get_HTTPResponse_Code
#   underscore_to_dash        Get-HTTPResponse-Code

FORMATS = {
    'LETTER_CASE': [
        'upper_case',
        'lower_case',
        'camel_case',
        'pascal_case',
        'ignore',
    ],
    'SEP': [
        'dash_to_underscore',
        'underscore_to_dash',
    ],
}

# Default settings
SETTINGS = {
    "CHECK_DIRS": [],
    "INCLUDE_FILES": [],
    "INCLUDE_DIRS": [],
    "IGNORE_FILES": [],
    "IGNORE_DIRS": [],
    "FILE_FORMATS": {
        "LETTER_CASE": "ignore",
        "SEP": [],
    },
    "DIR_FORMATS": {
        "LETTER_CASE": "ignore",
        "SEP": [],
    },
}
