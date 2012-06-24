from Architect import ArchitectUI

import ueSpec

def showArchitect():
        spec = ueSpec.Context().spec
	architect = ArchitectUI.ArchitectUI(spec)
	architect.show()

