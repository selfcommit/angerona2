# vim: set expandtab tabstop=4 shiftwidth=4 autoindent smartindent:

import threading


# stolen from http://www.alexconrad.org/2012/08/log-unique-request-ids-with-pyramid.html
def hack_thread_name_tween_factory(handler, registry):
    def hack_thread_name_tween(request):
        # Hack in the request ID inside the thread's name
        current_thread = threading.current_thread()
        original_name = current_thread.name
        current_thread.name = "%s][request=%s" % (original_name, request.id)
        try:
            response = handler(request)
        finally:
            # Restore the thread's original name when done
            current_thread.name = original_name
        return response
    return hack_thread_name_tween


#adapted from https://wiki.python.org/moin/EscapingHtml
def html_escape(text):
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in text)