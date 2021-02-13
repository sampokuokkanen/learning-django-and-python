from sockpuppet import reflex

class ItemCompleteReflex(reflex.Reflex):
    def increment(self, step=1):
        self.session['count'] = self.session.get('count', 1) + step
