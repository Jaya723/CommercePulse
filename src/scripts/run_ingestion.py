"""
Wrapper script to run bronze layer ingestion
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from commerce_pulse.ingestion import main

if __name__ == "__main__":
    main()
