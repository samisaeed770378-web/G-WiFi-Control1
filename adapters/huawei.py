from adapters.generic import GenericAdapter


class HuaweiAdapter(GenericAdapter):
    def capabilities(self):
        return super().capabilities()
