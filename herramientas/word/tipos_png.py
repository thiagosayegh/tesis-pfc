"""Agrega <Default Extension="png"/"jpeg"> a [Content_Types].xml de cada .docx (reescribe el zip)."""
import sys, zipfile, shutil, os
for ruta in sys.argv[1:]:
    tmp = ruta + ".tmp"
    with zipfile.ZipFile(ruta) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml":
                t = data.decode("utf-8")
                for ext, ct in (("png", "image/png"), ("jpeg", "image/jpeg"), ("jpg", "image/jpeg")):
                    if f'Extension="{ext}"' not in t:
                        t = t.replace("<Types ", "<Types ", 1).replace(">", f'><Default Extension="{ext}" ContentType="{ct}"/>', 1) if False else t
                        k = t.find(">", t.find("<Types")) + 1
                        t = t[:k] + f'<Default Extension="{ext}" ContentType="{ct}"/>' + t[k:]
                data = t.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, ruta)
    print("ok", os.path.basename(ruta))
