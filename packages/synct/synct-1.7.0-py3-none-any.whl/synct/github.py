"""
synct reads data and copies in Google or Excel spreadsheet.

    Copyright (C) 2023  Jan Beran <ari3s.git@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.


synct.github: GitHub access and operations
"""

import os
import requests

import synct.logger as log

TIMEOUT = 10    # in seconds

# Debug messages:
GET_GITHUB_TOKEN = 'get GitHub token'
GITHUB_QUERY = 'GitHub query: '

# Error messages:
GITHUB_QUERY_FAILED = 'GitHub query failed in the configuration file for the sheet '

# Warning messages:
INCOMPLETE_RESULTS = 'incomplete_results'

class Github:
    """ GitHub class """

    def __init__(self, url, token_file_name):
        """ Get GitHub access using API key """
        self.get_token(token_file_name)
        self.url = url

    def data_query(self, sheet, query):
        """ Query to GitHub """
        log.debug(GITHUB_QUERY + self.url + query)
        try:
            response = requests.get(self.url+query, headers=self.headers, timeout=TIMEOUT)
        except (AttributeError, TypeError) as exception:
            log.error(GITHUB_QUERY_FAILED + sheet + ':\n' + self.url + query)
            log.fatal_error(exception)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exception:
            log.error(GITHUB_QUERY_FAILED + sheet + ':\n' + self.url + query)
            log.fatal_error(exception)
        if not response.ok:
            log.warning(INCOMPLETE_RESULTS)
        resp = response.json()
        return resp['items']

    def get_token(self, token_file_name):
        """ Get token from the file """
        token = None
        if token_file_name:
            log.debug(GET_GITHUB_TOKEN)
            try:
                with open(os.path.expanduser(token_file_name), 'r', encoding="utf8") as token_file:
                    token = token_file.read().rstrip('\n')
                    token_file.close()
            except OSError as exception:
                log.warning(exception)
        if token:
            self.headers = {'Authorization': 'Token ' + token}
        else:
            self.headers = None
