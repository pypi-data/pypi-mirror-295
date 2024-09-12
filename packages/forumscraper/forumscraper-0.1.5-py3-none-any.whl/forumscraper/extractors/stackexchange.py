# by Dominik Stanisław Suchora <suchora.dominik7@gmail.com>
# License: GNU GPLv3

import re
import json
from reliq import reliq

from ..utils import dict_add, get_settings, url_merge_r, url_merge, url_valid
from .common import ItemExtractor, ForumExtractor


class stackexchange(ForumExtractor):
    class User(ItemExtractor):
        def __init__(self, session):
            super().__init__(session)

            self.match = [
                re.compile(r"/users/(\d+)"),
                1,
            ]
            self.path_format = "m-{}"

        def get_first_html(self, url, settings, state, rq=None):
            return reliq(self.session.get_json(url, settings, state)["html"]["content"])

        def get_contents(self, rq, settings, state, url, i_id):
            ret = {"format_version": "stackexchange-user", "url": url, "id": int(i_id)}

            t = json.loads(
                rq.search(
                    r"""
                .background div class=B>"memberProfileBanner memberTooltip-header.*" style=a>"url(" | "%(style)v" / sed "s#.*url(##;s#^//#https://#;s/?.*//;p;q" "n",
                .location a href=b>/misc/location-info | "%i",
                .avatar img src | "%(src)v" / sed "s/?.*//; q",
                .title span .userTitle | "%i",
                .banners.a * .userBanner; strong | "%i\n",
                .name h4 .memberTooltip-name; a; * c@[0] | "%i",
                .forum em; a href | "%(href)v",
                .extras dl .pairs c@[!0]; {
                    .key dt | "%i",
                    .value dd; {
                        time datetime | "%(datetime)v\a",
                        a m@v>"<" | "%i\a",
                        * l@[0] | "%i"
                    } / tr '\n' sed "s/^\a*//;s/\a.*//"
                } |
            """
                )
            )
            t["background"] = url_merge_r(url, t["background"])
            t["avatar"] = url_merge_r(url, t["avatar"])
            dict_add(ret, t)

            return ret

    class Thread(ItemExtractor):
        def __init__(self, session):
            super().__init__(session)

            self.match = [
                r"/questions/(\d+)",
                1,
            ]
            self.trim = True

        def get_post_comments(self, rq, url, postid, settings, state):
            n = rq.search(r'div #b>comments-link-; a .comments-link m@b>"Show " | "t"')
            if len(n) > 0:
                nsettings = get_settings(
                    settings, headers={"x-Requested-With": "XMLHttpRequest"}
                )
                rq = self.session.get_html(
                    "{}/posts/{}/comments".format(url_valid(url, base=True)[0], postid),
                    nsettings,
                    state,
                )

            comments = json.loads(
                rq.search(
                    r"""
                .comments li #E>comment-[0-9]+; {
                    .id.u * self@ | "%(data-comment-id)v",
                    .score.i div .comment-score; * c@[0] | "%i",
                    .content span .comment-copy | "%i",
                    .date span .comment-date; span title | "%(title)v" / sed "s/, L.*//",
                    [0] a .comment-user; {
                        .user * self@ | "%i",
                        .user_link * self@ | "%(href)v",
                        .reputation.u * self@ | "%(title)v" / tr ",."
                    },
                } |
             """
                )
            )["comments"]

            for i in comments:
                i["user_link"] = url_merge(url, i["user_link"])
            return comments

        def get_post(self, rq, url, settings, state):
            post = json.loads(
                rq.search(
                    r"""
                .id.u * self@ | "%(data-answerid)v %(data-questionid)v",
                .rating.i div .js-vote-count data-value | "%(data-value)v",
                .checkmark.b [0] div .js-accepted-answer-indicator | "t",
                .bounty.u [0] div .js-bounty-award | "%i",
                .content div class="s-prose js-post-body" | "%i",

                .s1 div .user-info m@"edited"; {
                    .edited span .relativetime | "%(title)v",
                    .editor {
                        .avatar img .bar-sm src | "%(src)v",
                         div .user-details; {
                            .name [0] * l@[1] c@[0] | "%i",
                            .link div .user-details; a href child@ | "%(href)v",
                            .reputation.u span .reputation-score | "%i" tr ",",
                            .gbadge.u span title=w>gold; span .badgecount | "%i",
                            .sbadge.u span title=w>silver; span .badgecount | "%i",
                            .bbadge.u span title=w>bronze; span .badgecount | "%i"
                        }
                    }
                },

                .s2 div .user-info m@v>"edited"; {
                    .date span .relativetime | "%(title)v",
                    .author {
                        .avatar img .bar-sm src | "%(src)v",
                         div .user-details; {
                            .name [0] * l@[1] c@[0] | "%i",
                            .link div .user-details; a href child@ | "%(href)v",
                            .reputation.u span .reputation-score | "%i" tr ",",
                            .gbadge.u span title=w>gold; span .badgecount | "%i",
                            .sbadge.u span title=w>silver; span .badgecount | "%i",
                            .bbadge.u span title=w>bronze; span .badgecount | "%i"
                        }
                    }
                },
                """
                )
            )
            post["author"] = post["s2"]["author"]
            post["date"] = post["s2"]["date"]
            post["edited"] = post["s1"]["edited"]
            post["editor"] = post["s1"]["editor"]
            post.pop("s1")
            post.pop("s2")
            post["author"]["avatar"] = url_merge(url, post["author"]["avatar"])
            post["author"]["link"] = url_merge(url, post["author"]["link"])
            post["editor"]["avatar"] = url_merge(url, post["editor"]["avatar"])
            post["editor"]["link"] = url_merge(url, post["editor"]["link"])

            post["comments"] = self.get_post_comments(
                rq, url, post["id"], settings, state
            )
            return post

        def get_contents(self, rq, settings, state, url, i_id):
            ret = {
                "format_version": "stackexchange-thread",
                "url": url,
                "id": int(i_id),
            }
            page = 0

            t = json.loads(
                rq.search(
                    r"""
                    .title h1 itemprop="name"; a | "%i",
                    div .flex--item .mb8 .ws-nowrap; {
                        .views.u [0] * self@ m@"Viewed" | "%(title)v" / tr "0-9" "" "c",
                        .asked [0] * self@ m@"Asked"; [0] time itemprop="dateCreated" datetime | "%(datetime)v",
                        .modified [0] * self@ m@"Modified"; [0] a title | "%(title)v"
                    },
                    .tags.a div .ps-relative; a .post-tag | "%i\n"
                    """
                )
            )
            dict_add(ret, t)

            posts = []
            posts.append(
                self.get_post(
                    rq.filter("div #question").self()[0], url, settings, state
                )
            )

            while True:
                for i in rq.filter(r"div #b>answer-").self():
                    posts.append(self.get_post(i, url, settings, state))

                page += 1
                if (
                    settings["thread_pages_max"] != 0
                    and page >= settings["thread_pages_max"]
                ):
                    break
                nexturl = self.get_next(url, rq)
                if nexturl is None:
                    break
                rq = self.session.get_html(nexturl, settings, state)

            ret["posts"] = posts
            return ret

    def __init__(self, session=None, **kwargs):
        super().__init__(session, **kwargs)

        self.thread = self.Thread(self.session)
        self.thread.get_next = self.get_next

        self.forum_threads_expr = reliq.expr(
            r'a .s-link href=a>/questions/ | "%(href)v\n"'
        )

        self.guesslist = [
            {
                "func": "get_thread",
                "exprs": [r"/questions/(\d+)"],
            },
            {
                "func": "get_users",
                "exprs": [r"/users/(\d+)"],
            },
            {"func": "get_forum", "exprs": None},
        ]

    def get_next_page(self, rq):
        return rq.search(r'[0] div .pager-answers; [0] a rel="next" href | "%(href)v"')

    def get_forum_next_page(self, rq):
        return rq.search(r'div .pager; [0] a rel=next href | "%(href)v"')

    def process_forum_r(self, url, rq, settings, state):
        t = json.loads(
            rq.search(
                r"""
                    .threads div #b>question-summary-; {
                        div .s-post-summary--stats; div .s-post-summary--stats-item; {
                            .score.u [0] * self@ title=b>"Score of ",
                            .views.u [0] * self@ title=e>" views" | "%(title)v",
                            [0] span m@f>"answers"; {
                                .answers.u [0] span .e>-number spre@ | "%i",
                                .solved.b * .has-accepted-answer parent@ | "t"
                            },
                            .bounty.u * self@ .has-bounty | "%i"
                        },
                        div .s-post-summary-content; {
                            * .s-post-summary--content-title; [0] a; {
                                .title * self@ | "%i",
                                .link * self@ | "%(href)v"
                            },
                            .excerp * .s-post-summary--content-excerpt | "%i",
                            [0] * .s-post-summary--meta; {
                                .tags.a a .s-tag | "%i\n",
                                .author div .s-user-card; {
                                    .avatar img .s-avatar--image | "%(src)v",
                                    div .s-user-card--info; {
                                        .name [0] * c@[0] | "%i",
                                        .link a | "%(href)v"
                                    },
                                    .reputation.u li s-user-card--rep; [0] span | "%(title)v %i" / tr ","
                                },
                                .date span .relativetime | "%(title)v"
                            }
                        }
                    } |
                """
            )
        )

        threads = t["threads"]

        for i in threads:
            i["link"] = url_merge(url, i["link"])
            i["author"]["link"] = url_merge(url, i["author"]["link"])
            i["author"]["avatar"] = url_merge(url, i["author"]["link"])

        return {
            "format_version": "stackexchange-forum",
            "url": url,
            "threads": threads,
        }
