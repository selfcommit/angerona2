# vim: set expandtab tabstop=4 shiftwidth=4 autoindent smartindent:

import threading

# stolen from Peter Grace https://github.com/PeterGrace
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

# based on http://stackoverflow.com/questions/8436812/how-to-implement-navigation-selected-item
class ViewController():
    def __init__(self, request, **kwargs):
        self.request = request
        self.navmenudata = [
            { 'txt':'Home',             'rte':'home'},
            { 'txt':'Share',            'rte':'secret'},
        ]

    @property
    def navmenu(self):
        items = []
        for item in self.navmenudata:
            item['url'] = self.request.route_url(item['rte'])
            if self.request.matched_route.name == item['rte']:
                item['active'] = 1
                items.append(item)
            else:
                item['active'] = 0
                items.append(item)

        return items

#adapted from https://wiki.python.org/moin/EscapingHtml
def html_escape(text):
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c,c) for c in text)