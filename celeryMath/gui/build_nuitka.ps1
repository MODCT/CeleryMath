nuitka --mingw64 --standalone --output-dir=build `
--show-progress --show-memory `
--plugin-enable=pyside6 `
--plugin-enable=numpy `
--nofollow-import-to=matplotlib `
--nofollow-import-to=PySide6.QtQml,PySide6.QtQuick `
--nofollow-import-to=black `
--windows-icon-from-ico="resources/icons/logo.ico" `
--windows-company-name="rainyl@MODCT.org" `
--windows-product-name="CeleryMath" `
--windows-file-version="0.1.2.0" `
--windows-product-version="0.1.2.0" `
--windows-file-description="CeleryMath" `
--windows-disable-console `
./celeryMath.py

New-Item build/celeryMath.dist/conf -ItemType Directory -ea 0
New-Item build/celeryMath.dist/log -ItemType Directory -ea 0
