from sockpuppet.reflex import Reflex
from lists.models import Item


class ItemCompleteReflex(Reflex):
    def complete(self):
        item = Item.objects.get(pk=self.element.dataset['item_id'])
        item.completed = self.element.dataset['completed'] == 'False'
        item.save()

    def delete(self):
        item = Item.objects.get(pk=self.element.dataset['item_id'])
        item.delete()
