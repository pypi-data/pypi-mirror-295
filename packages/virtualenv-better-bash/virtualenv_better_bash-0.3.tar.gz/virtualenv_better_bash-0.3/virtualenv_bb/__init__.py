
from virtualenv.activation.via_template import ViaTemplateActivator
from pathlib import Path

class BashActivator(ViaTemplateActivator):
    def templates(self):
        yield "activate"

    def as_name(self, template):
        return Path(template).stem
