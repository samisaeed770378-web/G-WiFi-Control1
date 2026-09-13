from adapters.generic import GenericAdapter


class TPLinkAdapter(GenericAdapter):
    def capabilities(self):
        return super().capabilities()
