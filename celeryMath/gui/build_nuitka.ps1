nuitka --mingw64 --standalone --output-dir=build `
--show-progress --show-memory `
--plugin-enable=pyside6 `
--plugin-enable=numpy `
--nofollow-import-to=matplotlib `
--windows-icon-from-ico="resources/icons/logo.ico" `
--windows-company-name="rainyl.com" `
--windows-product-name="CeleryMath" `
--windows-file-version="0.1.0.0" `
--windows-product-version="0.1.0.0" `
--windows-file-description="CeleryMath" `
./celeryMath.py
# --windows-disable-console `

New-Item build/celeryMath.dist/conf -ItemType Directory -ea 0
New-Item build/celeryMath.dist/log -ItemType Directory -ea 0
