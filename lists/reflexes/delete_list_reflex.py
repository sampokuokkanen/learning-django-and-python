from sockpuppet.reflex import Reflex


class DeleteListReflex(Reflex):
    def delete(self, step=1):
        self.count = 1 + step
