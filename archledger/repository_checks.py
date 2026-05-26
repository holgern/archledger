"""Repository-level check orchestration.

Extracted from ``repository.py`` to isolate check logic while
preserving ``ArchitectureRepository.check()`` as the public facade.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
