class Constants(object):
    UNRESOLVED_TICKET_URL = "/rest/api/3/search?expand=names&maxResults=50&" \
                            "jql=assignee%3D%22{}%22 %26 status not in (Resolved,Closed)"
    GET_TICKET_URL = "/rest/api/2/search?jql=assignee%3D%22{}%22&expand=names&maxResults={}"
    GET_COMMENTS_URL = "/rest/api/2/issue/{}/comment"
    UPDATE_COMMENT_URL = "/rest/api/2/issue/{}/comment/{}"
    ADD_ATTACHMENT_URL = "/rest/api/2/issue/{}/attachments"