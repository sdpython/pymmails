"""
@file
@brief Helper around POP server
"""

import poplib

from pyquickhelper import noLOG


def retrieve_mails_pop(user, password, server, begin=0, end=-1, fLOG=noLOG):
    """
    retrieves all emails using POP service

    @param      user        user
    @param      password    password
    @param      server      something like ``pop.domain.ext``
    @param      begin       first email to retrieve
    @param      end         last email to retrieve
    @param      fLOG        logging function
    @return                 list of emails
    """
    M = poplib.POP3(server)
    M.user(user)
    M.pass_(password)
    messageList = M.list()
    numMessages = len(messageList[1])
    allemails = []
    stat = M.stat()
    fLOG(stat)
    end = numMessages if end == -1 else end
    for i in range(begin, end):
        mail = M.retr(i + 1)
        size = mail[2]
        #response = mail[0]
        allemails.append(mail[1])
        fLOG(
            "retrieve_mails_pop [mail {0}/{1}, size={2}]".format(i, end, size))
    return allemails
