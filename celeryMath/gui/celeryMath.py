import sys

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QSystemSemaphore, QSharedMemory

from src.application import CeleryMath
from src.lib.utils.utils import seed_everything

WIN_ID = "celeryMath"
SRE_MEM_ID = "celeryMathMem"


def main():
    app = QApplication(sys.argv)

    semaphore = QSystemSemaphore(WIN_ID, 1)
    semaphore.acquire()
    if sys.platform != "win32":
        nix_fix_shared_mem = QSharedMemory(SRE_MEM_ID)
        if nix_fix_shared_mem.attach():
            nix_fix_shared_mem.detach()
    shared_memory = QSharedMemory(SRE_MEM_ID)
    if shared_memory.attach():
        is_running = True
    else:
        shared_memory.create(1)
        is_running = False
    semaphore.release()
    if is_running:
        QMessageBox.warning(
            None,
            "Application already running",
            "One instance of the application is already running.",
            QMessageBox.Ok,
        )
        return
    mainWindow = CeleryMath()
    # mainWindow.flashSplash()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    seed_everything(241)
    main()
