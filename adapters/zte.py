from adapters.generic import GenericAdapter


class ZTEAdapter(GenericAdapter):
    def capabilities(self):
        return super().capabilities()
