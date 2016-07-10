#!/usr/bin/env python3

# Name: twts
# Description: A command-line tool to search on Twitter
# Licence: GPLv3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# TODO: Authentication

class bcolors:
    magenta = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    normal = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

if __name__ == '__main__':

    import sys
    import argparse
    import pickle
    import json
    import textwrap
    import twitter

    api = twitter.Api(consumer_key = 'NQeuqJHWOHL8tww1Ibk7JxrgV',
                      consumer_secret = 'ekAjHG01nhtMouDFWoKdWLPuDYxEbTJy8Ef1dUCf7zHBMvxznU',
                      access_token_key = '367414376-UEQwEF6WPjbZOla8zpTwoC1BgyqSDAstgJjXkfLw',
                      access_token_secret = 'kvjnzRv9Mk08B5DhfG3Yy53VZDBt4Aq9sCmjpSo7MupFl')

    parser = argparse.ArgumentParser(description = 'A command-line tool to search on Twitter')
    parser.add_argument('term', nargs='?', help = 'Term to search by')
    parser.add_argument('-a', '--authorize', nargs='?', help = 'authorize application') #TODO: change this description
    parser.add_argument('-g', '--geocode', help = 'geolocation within which to search for tweets')
    parser.add_argument('-p', '--popular', action='store_true',
                        help = 'show popular tweets')
    parser.add_argument('-r', '--recent', action='store_true',
                        help = 'show recent tweets')
    parser.add_argument('-l', '--limit', type=int,
                        help = 'number of results to return')
    parser.add_argument('-s', '--since-id',
                        help = 'returns results with an ID greater than (that is, more recent than) the specified ID')
    parser.add_argument('-M', '--max-id',
                        help = ' returns only statuses with an ID less than (that is, older than) or equal to the specified ID')
    parser.add_argument('-u', '--until',
                        help = 'returns tweets generated before the given date')
    parser.add_argument('-S', '--since',
                        help = 'returns tweets generated since the given date')

    # print help output if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.term or args.geocode:

        params = {
            'term': args.term if args.term else '',
            'geocode': args.geocode if args.geocode else '',
            'since_id': args.since_id if args.since_id else None,
            'max_id': args.max_id if args.max_id else None,
            'until': args.until if args.until else '',
            'since': args.since if args.since else '',
            'count': args.limit if args.limit else 15
        }

        query_result = api.GetSearch(
            term = params['term'],
            geocode = params['geocode'],
            since_id = params['since_id'],
            max_id = params['max_id'],
            until = params['until'],
            since = params['since'],
            count = params['count'],
            result_type = 'popular' if args.popular else 'recent' if args.recent else 'mixed'
        )

        wrapper = textwrap.TextWrapper()
        wrapper.width = 100
        wrapper.initial_indent = ' '
        wrapper.subsequent_indent = '  '

        for public_tweet in query_result:
            print(bcolors.yellow + '  @' + public_tweet.user.screen_name + bcolors.normal +
                  '\n',
                  wrapper.fill(public_tweet.retweeted_status.text)
                  if public_tweet.retweeted_status
                  else wrapper.fill(public_tweet.text),
                  '\n' if not (public_tweet.urls)
                  else bcolors.green + ' (' + public_tweet.urls[0].url + ')' + bcolors.normal + '\n')
