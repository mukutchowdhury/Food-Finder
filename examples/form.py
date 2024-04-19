"""
This module provides the glossary query form
"""

import examples.form_filler as ff

from examples.form_filler import FLD_NM  # for tests

FNAME = 'fname'
LNAME = 'lname'
EMAIL = 'email'
PASSWORD = 'password'

LOGIN_FORM_FLDS = [
    {
        FLD_NM: FNAME,
        ff.QSTN: 'First Name',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
        ff.TYPE: 'text',
    },
    {
        FLD_NM: LNAME,
        ff.QSTN: 'Last Name',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
        ff.TYPE: 'text',
    },
    {
        FLD_NM: EMAIL,
        ff.QSTN: 'Email',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
        ff.TYPE: 'email',
    },
    {
        FLD_NM: PASSWORD,
        ff.QSTN: 'Password',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
        ff.TYPE: 'password',
    },
]


def get_form() -> list:
    return LOGIN_FORM_FLDS


def get_form_descr() -> dict:
    """
    For Swagger!
    """
    return ff.get_form_descr(LOGIN_FORM_FLDS)


def get_fld_names() -> list:
    return ff.get_fld_names(LOGIN_FORM_FLDS)


def main():
    # print(f'Form: {get_form()=}\n\n')
    print(f'Form: {get_form_descr()=}\n\n')
    # print(f'Field names: {get_fld_names()=}\n\n')


if __name__ == "__main__":
    main()