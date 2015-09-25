
# based on http://stackoverflow.com/questions/8436812/how-to-implement-navigation-selected-item
class ViewController(object):
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
